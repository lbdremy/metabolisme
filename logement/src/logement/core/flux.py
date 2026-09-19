"""Pure transforms for the housing FLOW cross (article 3, 2026-09-18 —
reworked by the adversarial review of R-18 the same day).

The proposal P-01 detends a STOCK (194 488 dwellings, R-07) while
households keep forming (L-19/L-32). This module measures, per zone
d'emploi, how the stock grew and how much was built:

- household formation per year from the census vintages 2016 → 2022
  (S-11: P16_MEN, P22_MEN — six years between vintages, D-05) and the
  DECOMPOSITION of the stock growth (primary residences, secondary
  residences, vacants) over the same years;
- dwellings STARTED per year from the SDES communal series IN REAL DATE
  (S-56, « Tous Logements », closed years 2013-2024, D-24), with the
  event-date commune codes mapped to the 2026 COG through the INSEE
  movements table (S-59) so merged communes keep their starts;
- the UNDERCOUNT of the communal series (~15 % of site-opening
  declarations never reach Sitadel, S-58): the yearly ratio of the
  SDES estimated national series (S-57) to the communal one is the
  parameter H-21, and every flow figure is published in two readings
  — « déclaré » (factor 1) and « estimé » (factor H-21);
- the dwellings NEEDED per household formed, under three affectation
  conventions of the new stock to secondary residences (none / the
  share OBSERVED in the ZE's own stock growth 2016-2022 / the 2022
  structure), the vacancy share of 2022 being kept in all three;
- the balance per ZE, its geography, four windows, the annual series
  2013-2024, and what it means for the detente stock: per ZE, the
  years the R-07 need would last against the ZE's own flow deficit —
  on the 2017-2022 window and on the closed years 2023-2024.

What the ratio measures (HD-1 of the review): households ≡ primary
residences in the census, so « need at constant structure » is close to
the observed stock growth — the ratio says how much construction it
took to produce the growth the census recorded, NOT whether a larger
formation of households was prevented. Descriptive arithmetic; no
behavioural model. No I/O, no clock — reads happen in the shell.
"""

from __future__ import annotations

import pandas as pd

from logement.core import stats
from logement.core.lovac import plm_parent
from logement.models import HypothesisRecord

CENSUS_FLOW_COLS = (
    "P11_MEN",
    "P16_MEN",
    "P22_MEN",
    "P11_LOG",
    "P16_LOG",
    "P22_LOG",
    "P22_RP",
    "P16_RP",
    "P22_RSECOCC",
    "P16_RSECOCC",
    "P22_LOGVAC",
    "P16_LOGVAC",
)
SITADEL_MONTHLY_COLS = (
    "ANNEE",
    "MOIS",
    "CODE_INSEE",
    "TYPE_LGT",
    "LOG_AUT",
    "LOG_COM",
    "SDP_AUT",
    "SDP_COM",
)
SITADEL_ALL_TYPES = "Tous Logements"
NATIONAL_SERIES_RAW = "Brute"
# Census vintages are centred on their survey window (2016 = 2014-2018,
# 2022 = 2020-2024): six years between the two centres.
VINTAGE_YEARS = 6
# Windows: aligned on the census vintages (central), aligned on
# delivery (starts ~2 years before completion), and the two later
# windows that include the closed post-2022 years (HD-4).
WINDOW = (2017, 2022)
WINDOWS = ((2015, 2020), (2017, 2022), (2018, 2023), (2019, 2024))
LONG_WINDOW = (2013, 2024)
RECENT_YEARS = (2023, 2024)
# Ranking floor: a ZE forming fewer households per year than this stays
# in the frame but out of rankings AND of the published correlation
# (HD-9/ST-1: below it the ratio is degenerate).
MIN_FORMATION_PER_YEAR = 200.0
# COG movement codes whose « après » commune absorbs the « avant » code
# (fusions, changes of code) — S-59, v_mvt_commune.
COG_ABSORBING_MODS = ("31", "32", "33", "34", "41", "50", "70")
COG_MAX_HOPS = 8
AFFECTATION_VARIANTS = ("sans_rs", "rs_observee", "structure_2022")


class FluxError(Exception):
    """A flow payload does not have the expected shape."""


# ---------------------------------------------------------------- parsing


def parse_census_vintages(raw: pd.DataFrame) -> pd.DataFrame:
    """Parse the S-11 commune rows into the vintage counts (PLM → parent).

    The base lists PLM parents before their arrondissements: the parent
    row is kept and the arrondissement rows dropped (a NaN count on a
    commune is kept as NaN and counted by the caller, never zeroed).
    """
    for col in ("CODGEO", *CENSUS_FLOW_COLS):
        if col not in raw.columns:
            raise FluxError(f"missing census column {col}")
    out = pd.DataFrame({"code": raw["CODGEO"].astype("string").str.strip().map(plm_parent)})
    for col in CENSUS_FLOW_COLS:
        out[col] = pd.to_numeric(raw[col], errors="coerce")
    out = out.drop_duplicates(subset="code", keep="first")
    if out.empty:
        raise FluxError("no commune row in the census base")
    return out


def aggregate_sitadel_monthly(raw: pd.DataFrame) -> pd.DataFrame:
    """Reduce Sitadel monthly rows to « Tous Logements » sums per commune × year (S-54)."""
    for col in SITADEL_MONTHLY_COLS:
        if col not in raw.columns:
            raise FluxError(f"missing Sitadel column {col}")
    rows = raw[raw["TYPE_LGT"].astype("string").str.strip() == SITADEL_ALL_TYPES]
    if rows.empty:
        raise FluxError(f"no '{SITADEL_ALL_TYPES}' row in the Sitadel file")
    out = pd.DataFrame(
        {
            "CODE_INSEE": rows["CODE_INSEE"].astype("string").str.strip(),
            "ANNEE": pd.to_numeric(rows["ANNEE"], errors="coerce"),
        }
    )
    for col in ("LOG_AUT", "LOG_COM", "SDP_AUT", "SDP_COM"):
        out[col] = pd.to_numeric(rows[col], errors="coerce")
    out = out.dropna(subset=["CODE_INSEE", "ANNEE"])
    out["ANNEE"] = out["ANNEE"].astype(int)
    return out.groupby(["CODE_INSEE", "ANNEE"], as_index=False)[
        ["LOG_AUT", "LOG_COM", "SDP_AUT", "SDP_COM"]
    ].sum()


def parse_sitadel_annual(raw: pd.DataFrame, code_col: str = "CODE_INSEE") -> pd.DataFrame:
    """Parse an annual commune × year Sitadel table (S-54 extract or S-56).

    Keeps the « Tous Logements » rows when a TYPE_LGT column is present
    (S-56 lists the components too). Arrondissement rows are DROPPED
    when their parent commune is listed (S-56 carries Paris both ways —
    summing would double it, SA-2); otherwise mapped to the parent. A
    missing count (S-56: 2025 starts) is dropped, never zero.
    """
    for col in (code_col, "ANNEE", "LOG_COM", "LOG_AUT"):
        if col not in raw.columns:
            raise FluxError(f"missing Sitadel column {col}")
    rows = raw
    if "TYPE_LGT" in raw.columns:
        rows = raw[raw["TYPE_LGT"].astype("string").str.strip() == SITADEL_ALL_TYPES]
        if rows.empty:
            raise FluxError(f"no '{SITADEL_ALL_TYPES}' row in the Sitadel file")
    codes = rows[code_col].astype("string").str.strip()
    parents = codes.map(plm_parent)
    listed = set(codes.dropna())
    is_arrondissement = ((parents != codes) & parents.isin(listed)).to_numpy()
    frame = pd.DataFrame(
        {
            "code": parents,
            "annee": pd.to_numeric(rows["ANNEE"], errors="coerce"),
            "log_com": pd.to_numeric(rows["LOG_COM"], errors="coerce"),
            "log_aut": pd.to_numeric(rows["LOG_AUT"], errors="coerce"),
        }
    )[~is_arrondissement].dropna()
    if frame.empty:
        raise FluxError("no usable row in the Sitadel table")
    frame["annee"] = frame["annee"].astype(int)
    return frame.groupby(["code", "annee"], as_index=False)[["log_com", "log_aut"]].sum()


def parse_national_estimated(raw: pd.DataFrame) -> pd.Series:
    """Yearly starts of the SDES estimated national series (S-57, raw, all types)."""
    for col in ("ANNEE", "TYPE_LGT", "NAT_SERIES", "LOG_COM"):
        if col not in raw.columns:
            raise FluxError(f"missing national series column {col}")
    rows = raw[
        (raw["TYPE_LGT"].astype("string").str.strip() == SITADEL_ALL_TYPES)
        & (raw["NAT_SERIES"].astype("string").str.strip() == NATIONAL_SERIES_RAW)
    ]
    if rows.empty:
        raise FluxError("no raw 'Tous Logements' row in the national series")
    out = pd.DataFrame(
        {
            "annee": pd.to_numeric(rows["ANNEE"], errors="coerce"),
            "log_com": pd.to_numeric(rows["LOG_COM"], errors="coerce"),
        }
    ).dropna()
    out["annee"] = out["annee"].astype(int)
    return out.groupby("annee")["log_com"].sum()


def undercount_ratios(national_estimated: pd.Series, communal: pd.DataFrame) -> pd.Series:
    """Yearly ratio estimated / communal starts (the H-21 evidence), closed years only."""
    communal_by_year = communal.groupby("annee")["log_com"].sum()
    years = [y for y in communal_by_year.index if y in national_estimated.index]
    if not years:
        raise FluxError("no common year between the national and communal series")
    ratios = national_estimated.loc[years] / communal_by_year.loc[years]
    return ratios[(ratios > 0) & ratios.notna()]


def cog_successor_map(mvt: pd.DataFrame) -> dict[str, str]:
    """Old commune code → absorbing commune code, from the COG movements (S-59)."""
    for col in ("MOD", "COM_AV", "COM_AP", "TYPECOM_AP"):
        if col not in mvt.columns:
            raise FluxError(f"missing COG movement column {col}")
    rows = mvt[
        mvt["MOD"].astype("string").str.strip().isin(COG_ABSORBING_MODS)
        & (mvt["TYPECOM_AP"].astype("string").str.strip() == "COM")
    ]
    mapping: dict[str, str] = {}
    for before, after in zip(rows["COM_AV"], rows["COM_AP"], strict=True):
        before_code, after_code = str(before).strip(), str(after).strip()
        if before_code != after_code:
            mapping.setdefault(before_code, after_code)
    return mapping


def remap_to_membership(
    annual: pd.DataFrame, known_codes: set[str], successors: dict[str, str]
) -> tuple[pd.DataFrame, dict[str, int]]:
    """Map event-date commune codes absent from the membership table to their successor.

    Follows the COG movements up to COG_MAX_HOPS; codes still unknown
    are kept in the frame and their starts are COUNTED as lost, never
    silently dropped (ST-3/HD-6).
    """
    out = annual.copy()

    def resolve(code: str) -> str:
        current = code
        for _ in range(COG_MAX_HOPS):
            if current in known_codes:
                return current
            nxt = successors.get(current)
            if nxt is None or nxt == current:
                return current
            current = nxt
        return current

    unknown = ~out["code"].isin(known_codes)
    out.loc[unknown, "code"] = out.loc[unknown, "code"].map(resolve)
    still_unknown = ~out["code"].isin(known_codes)
    report = {
        "codes_remappes": int(annual.loc[unknown & ~still_unknown, "code"].nunique()),
        "lignes_remappees": int((unknown & ~still_unknown).sum()),
        "commences_remappes_total": round(
            float(out.loc[unknown & ~still_unknown, "log_com"].sum())
        ),
        "codes_sans_ze": int(out.loc[still_unknown, "code"].nunique()),
        "commences_sans_ze_total": round(float(out.loc[still_unknown, "log_com"].sum())),
    }
    grouped = out.groupby(["code", "annee"], as_index=False)[["log_com", "log_aut"]].sum()
    return grouped, report


# ------------------------------------------------------------------ per ZE


def starts_by_ze_year(annual: pd.DataFrame, commune_ze: pd.DataFrame) -> pd.DataFrame:
    """Pivot starts to ZE × year (sum of the joined communes)."""
    merged = annual.merge(commune_ze, on="code", how="inner")
    if merged.empty:
        raise FluxError("no Sitadel commune joined with the membership table")
    return merged.pivot_table(index="ze", columns="annee", values="log_com", aggfunc="sum")


def _window_mean(by_year: pd.DataFrame, window: tuple[int, int]) -> pd.Series:
    first, last = window
    cols = [y for y in by_year.columns if first <= int(y) <= last]
    if len(cols) != last - first + 1:
        raise FluxError(f"Sitadel years missing in window {window}")
    return by_year[cols].sum(axis=1) / len(cols)


def flux_by_ze(
    census: pd.DataFrame,
    by_year: pd.DataFrame,
    commune_ze: pd.DataFrame,
    undercount_factor: float,
) -> pd.DataFrame:
    """Cross household formation, stock decomposition and starts into the per-ZE frame."""
    if undercount_factor < 1:
        raise FluxError(f"undercount factor below 1: {undercount_factor}")
    merged = census.merge(commune_ze, on="code", how="inner")
    if merged.empty:
        raise FluxError("no commune joined between census and membership table")
    frame = merged.groupby("ze")[list(CENSUS_FLOW_COLS)].sum(min_count=1)
    frame["formation_menages_an"] = (frame["P22_MEN"] - frame["P16_MEN"]) / VINTAGE_YEARS
    frame["croissance_parc_an"] = (frame["P22_LOG"] - frame["P16_LOG"]) / VINTAGE_YEARS
    frame["croissance_rp_an"] = (frame["P22_RP"] - frame["P16_RP"]) / VINTAGE_YEARS
    frame["croissance_rs_an"] = (frame["P22_RSECOCC"] - frame["P16_RSECOCC"]) / VINTAGE_YEARS
    frame["croissance_vac_an"] = (frame["P22_LOGVAC"] - frame["P16_LOGVAC"]) / VINTAGE_YEARS
    frame["part_rs_2022"] = frame["P22_RSECOCC"] / frame["P22_LOG"]
    frame["part_vac_2022"] = frame["P22_LOGVAC"] / frame["P22_LOG"]
    # Share of the observed stock growth that went to secondary residences
    # (the ZE's own affectation, 2016-2022); undefined when the stock did
    # not grow → falls back to the 2022 structure.
    growth = frame["croissance_parc_an"]
    observed = (frame["croissance_rs_an"] / growth).where(growth > 0)
    # Bounded so that at least 5 % of the new stock can be primary
    # residences (a ZE whose RS grew faster than its stock would
    # otherwise have no primary-residence share left).
    ceiling = (0.95 - frame["part_vac_2022"]).clip(lower=0)
    frame["part_rs_neuf_observee"] = (
        observed.clip(lower=0).fillna(frame["part_rs_2022"]).clip(upper=ceiling)
    )
    shares = {
        "sans_rs": pd.Series(0.0, index=frame.index),
        "rs_observee": frame["part_rs_neuf_observee"],
        "structure_2022": frame["part_rs_2022"],
    }
    formation = frame["formation_menages_an"].clip(lower=0)
    for label, share in shares.items():
        denominator = 1 - share - frame["part_vac_2022"]
        if (denominator <= 0).any():
            raise FluxError(f"a ZE has no primary-residence share left ({label})")
        frame[f"besoin_{label}_an"] = formation / denominator
    frame["besoin_flux_an"] = frame["besoin_rs_observee_an"]
    frame["logements_par_menage_forme"] = frame["besoin_flux_an"] / formation.where(formation > 0)

    by_year = by_year.reindex(frame.index)
    for first, last in WINDOWS:
        frame[f"commences_{first}_{last}_an"] = _window_mean(by_year, (first, last))
    frame["commences_an"] = frame[f"commences_{WINDOW[0]}_{WINDOW[1]}_an"]
    frame["commences_an_long"] = _window_mean(by_year, LONG_WINDOW)
    for year in RECENT_YEARS:
        if year not in by_year.columns:
            raise FluxError(f"Sitadel year {year} missing")
        frame[f"commences_{year}"] = by_year[year]
    frame["commences_recent_an"] = frame[[f"commences_{y}" for y in RECENT_YEARS]].mean(axis=1)
    frame["commences_estimes_an"] = frame["commences_an"] * undercount_factor
    frame["commences_recent_estimes_an"] = frame["commences_recent_an"] * undercount_factor
    for reading, col in (("declare", "commences_an"), ("estime", "commences_estimes_an")):
        frame[f"solde_{reading}_an"] = frame[col] - frame["besoin_flux_an"]
        frame[f"ratio_{reading}"] = (frame[col] / frame["besoin_flux_an"]).where(
            frame["besoin_flux_an"] > 0
        )
    for label in AFFECTATION_VARIANTS:
        frame[f"solde_estime_{label}_an"] = (
            frame["commences_estimes_an"] - frame[f"besoin_{label}_an"]
        )
    frame["solde_recent_estime_an"] = frame["commences_recent_estimes_an"] - frame["besoin_flux_an"]
    frame["commences_pour_1000_logements"] = frame["commences_estimes_an"] / frame["P22_LOG"] * 1000
    return frame


# -------------------------------------------------------------- summary


def _quantiles(series: pd.Series, digits: int = 2) -> dict[str, float | None]:
    clean = series.dropna()
    keys = ("min", "p25", "median", "p75", "max")
    if clean.empty:
        return dict.fromkeys(keys)
    quantiles = clean.quantile([0, 0.25, 0.5, 0.75, 1])
    return {k: round(float(v), digits) for k, v in zip(keys, quantiles, strict=True)}


def _opt(value: float, digits: int) -> float | None:
    return None if pd.isna(value) else round(float(value), digits)


def _entry(row: pd.Series) -> dict[str, object]:
    return {
        "ze": str(row.name),
        "name": row["ze_name"] if pd.notna(row["ze_name"]) else None,
        "tendue": bool(row["tendue"]),
        "formation_menages_an": round(float(row["formation_menages_an"])),
        "besoin_flux_an": round(float(row["besoin_flux_an"])),
        "commences_declares_an": round(float(row["commences_an"])),
        "commences_estimes_an": round(float(row["commences_estimes_an"])),
        "solde_estime_an": round(float(row["solde_estime_an"])),
        "solde_estime_sans_rs_an": round(float(row["solde_estime_sans_rs_an"])),
        "solde_estime_structure_2022_an": round(float(row["solde_estime_structure_2022_an"])),
        "ratio_estime": _opt(row["ratio_estime"], 2),
        "part_rs_2022_pct": round(float(row["part_rs_2022"]) * 100, 1),
        "part_rs_neuf_observee_pct": round(float(row["part_rs_neuf_observee"]) * 100, 1),
        "commences_2023_2024_estimes_an": _opt(row["commences_recent_estimes_an"], 0),
        "solde_2023_2024_estime_an": _opt(row["solde_recent_estime_an"], 0),
        "besoin_detente": _opt(row["besoin_detente"], 0),
        "annees_absorption_2017_2022": _opt(row["annees_absorption"], 1),
        "annees_absorption_2023_2024": _opt(row["annees_absorption_recent"], 1),
    }


def _ratio(numerator: float, denominator: float) -> float | None:
    return round(numerator / denominator, 2) if denominator > 0 else None


def _block(sub: pd.DataFrame) -> dict[str, object]:
    formation = float(sub["formation_menages_an"].sum())
    besoin = float(sub["besoin_flux_an"].sum())
    besoin_sans_rs = float(sub["besoin_sans_rs_an"].sum())
    besoin_structure = float(sub["besoin_structure_2022_an"].sum())
    declare = float(sub["commences_an"].sum())
    estime = float(sub["commences_estimes_an"].sum())
    recent = float(sub["commences_recent_estimes_an"].sum())
    growth = float(sub["croissance_parc_an"].sum())
    return {
        "n_ze": len(sub),
        "menages_2016": round(float(sub["P16_MEN"].sum())),
        "menages_2022": round(float(sub["P22_MEN"].sum())),
        "formation_menages_an": round(formation),
        "croissance_parc_an": round(growth),
        "dont_rp_an": round(float(sub["croissance_rp_an"].sum())),
        "dont_rs_an": round(float(sub["croissance_rs_an"].sum())),
        "dont_vacants_an": round(float(sub["croissance_vac_an"].sum())),
        "part_rs_neuf_observee_pct": (
            round(float(sub["croissance_rs_an"].sum()) / growth * 100, 1) if growth > 0 else None
        ),
        "besoin_flux_an": round(besoin),
        "besoin_sans_rs_an": round(besoin_sans_rs),
        "besoin_structure_2022_an": round(besoin_structure),
        "commences_declares_an": round(declare),
        "commences_estimes_an": round(estime),
        "commences_declares_2013_2024_an": round(float(sub["commences_an_long"].sum())),
        "ratio_declare": _ratio(declare, besoin),
        "ratio_estime": _ratio(estime, besoin),
        "ratio_estime_sans_rs": _ratio(estime, besoin_sans_rs),
        "ratio_estime_structure_2022": _ratio(estime, besoin_structure),
        "solde_declare_an": round(declare - besoin),
        "solde_estime_an": round(estime - besoin),
        "solde_estime_sans_rs_an": round(estime - besoin_sans_rs),
        "solde_estime_structure_2022_an": round(estime - besoin_structure),
        "n_ze_deficitaires_estime": int((sub["solde_estime_an"] < 0).sum()),
        "deficit_des_ze_deficitaires_estime_an": round(
            float((-sub["solde_estime_an"]).clip(lower=0).sum())
        ),
        "n_ze_menages_en_baisse": int((sub["formation_menages_an"] < 0).sum()),
        "commences_2023_2024_estimes_an": round(recent),
        "solde_2023_2024_estime_an": round(recent - besoin),
        "n_ze_deficitaires_2023_2024": int((sub["solde_recent_estime_an"] < 0).sum()),
        "deficit_2023_2024_des_ze_deficitaires_an": round(
            float((-sub["solde_recent_estime_an"]).clip(lower=0).sum())
        ),
        "commences_estimes_moins_croissance_parc_an": round(estime - growth),
    }


def build_summary(
    frame: pd.DataFrame,
    tendue: pd.Series,
    cost_index: pd.Series,
    ze_names: pd.Series,
    besoin_detente: pd.Series,
    h21: HypothesisRecord,
    yearly: dict[str, pd.Series],
    cog_report: dict[str, int],
    tendue_variants: dict[str, pd.Series] | None = None,
) -> dict[str, object]:
    """Assemble the R-18 payload: two readings, three affectations, per-ZE stock vs flow."""
    full = (
        frame.join(tendue.rename("tendue"), how="left")
        .join(cost_index.rename("indice_cout_pct"), how="left")
        .join(ze_names.rename("ze_name"), how="left")
        .join(besoin_detente.rename("besoin_detente"), how="left")
    )
    full["tendue"] = full["tendue"].fillna(False).astype(bool)
    known = full.dropna(subset=["commences_an"])
    if known.empty:
        raise FluxError("no ZE with Sitadel starts")
    # Per-ZE stock vs flow (SE-2): a ZE's own detente need against its own deficit.
    deficit = (-known["solde_estime_an"]).clip(lower=0)
    deficit_recent = (-known["solde_recent_estime_an"]).clip(lower=0)
    known = known.assign(
        annees_absorption=(known["besoin_detente"] / deficit).where(deficit > 0),
        annees_absorption_recent=(known["besoin_detente"] / deficit_recent).where(
            deficit_recent > 0
        ),
    )
    tense = known[known["tendue"]]
    others = known[~known["tendue"]]
    ranked = known[known["formation_menages_an"] >= MIN_FORMATION_PER_YEAR]
    ranked_tense = ranked[ranked["tendue"]]
    ranked_others = ranked[~ranked["tendue"]]
    besoin_total = float(tense["besoin_detente"].fillna(0).sum())

    def absorption_block(sub: pd.DataFrame, years_col: str, solde_col: str) -> dict[str, object]:
        need = float(sub["besoin_detente"].fillna(0).sum())
        deficit_sum = float((-sub[solde_col]).clip(lower=0).sum())
        return {
            "n_ze": len(sub),
            "part_du_besoin_detente_pct": (
                round(need / besoin_total * 100, 1) if besoin_total > 0 else None
            ),
            "besoin_detente_porte": round(need),
            "deficit_an": round(deficit_sum),
            "annees_mediane_par_ze": _opt(sub[years_col].median(), 1) if len(sub) else None,
            "annees_agregees": round(need / deficit_sum, 1) if deficit_sum > 0 else None,
        }

    shares = {
        "part_formation_menages_pct": round(
            float(tense["formation_menages_an"].clip(lower=0).sum())
            / float(known["formation_menages_an"].clip(lower=0).sum())
            * 100,
            1,
        ),
        "part_besoin_flux_pct": round(
            float(tense["besoin_flux_an"].sum()) / float(known["besoin_flux_an"].sum()) * 100, 1
        ),
        "part_commences_pct": round(
            float(tense["commences_an"].sum()) / float(known["commences_an"].sum()) * 100, 1
        ),
        "part_parc_2022_pct": round(
            float(tense["P22_LOG"].sum()) / float(known["P22_LOG"].sum()) * 100, 1
        ),
    }
    windows = {}
    for first, last in WINDOWS:
        col = f"commences_{first}_{last}_an"
        est_all = float(known[col].sum()) * h21.central_value
        est_tense = float(tense[col].sum()) * h21.central_value
        windows[f"{first}-{last}"] = {
            "commences_estimes_an": round(est_all),
            "ratio_estime_national": _ratio(est_all, float(known["besoin_flux_an"].sum())),
            "solde_estime_tendues_an": round(est_tense - float(tense["besoin_flux_an"].sum())),
        }
    variants = {}
    for label, flag in (tendue_variants or {}).items():
        sub = known.join(flag.rename("t"), how="left")
        sub["t"] = sub["t"].fillna(False).astype(bool)
        t_sub = sub[sub["t"]]
        variants[label] = {
            "n_ze_tendues": len(t_sub),
            "solde_estime_tendues_an": round(float(t_sub["solde_estime_an"].sum())),
            "solde_estime_sans_rs_tendues_an": round(float(t_sub["solde_estime_sans_rs_an"].sum())),
        }

    def ranked_entries(
        sub: pd.DataFrame, key: str, ascending: bool, n: int
    ) -> list[dict[str, object]]:
        ordered = sub.sort_values([key, "ze_name"], ascending=[ascending, True], kind="stable")
        return [_entry(r) for _, r in ordered.head(n).iterrows()]

    return {
        "fenetres": {
            "menages": "2016 → 2022 (millésimes censitaires, 6 ans)",
            "commences_central": f"{WINDOW[0]}-{WINDOW[1]} (moyenne annuelle, date réelle, S-56)",
            "commences_recent": "2023-2024 (années closes, moyenne)",
            "fenetres_publiees": [f"{a}-{b}" for a, b in WINDOWS],
        },
        "lectures": {
            "declare": "série communale S-56 telle quelle",
            "estime": f"× H-21 ({h21.central_value}) — sous-compte des DOC (S-57/S-58)",
        },
        "affectation_rs": {
            "centrale": "rs_observee (part des RS dans la croissance du parc 2016-2022 de la ZE)",
            "bornes": ["sans_rs", "structure_2022"],
            "part_rs_neuf_observee_pct": _quantiles(known["part_rs_neuf_observee"] * 100, 1),
        },
        "hypothese_h21": {
            "id": h21.id,
            "central": h21.central_value,
            "plausible_range": list(h21.plausible_range),
        },
        "series_annuelles": {
            name: {
                str(k): (round(float(v), 3) if name.startswith("ratio") else round(float(v)))
                for k, v in series.items()
            }
            for name, series in yearly.items()
        },
        "cog": cog_report,
        "national": _block(known),
        "tendues": _block(tense),
        "autres": _block(others),
        "parts_des_ze_tendues": shares,
        "ratio_estime": {
            "toutes_au_plancher": _quantiles(ranked["ratio_estime"]),
            "tendues_au_plancher": _quantiles(ranked_tense["ratio_estime"]),
            "autres_au_plancher": _quantiles(ranked_others["ratio_estime"]),
            "mann_whitney_p_tendues_vs_autres_au_plancher": stats.mann_whitney_p(
                ranked_tense["ratio_estime"].dropna(), ranked_others["ratio_estime"].dropna()
            ),
            "toutes_sans_plancher": _quantiles(known["ratio_estime"]),
            "n_ze_besoin_nul": int((known["besoin_flux_an"] <= 0).sum()),
            "n_ze_besoin_nul_tendues": int((tense["besoin_flux_an"] <= 0).sum()),
        },
        "logements_par_menage_forme": _quantiles(known["logements_par_menage_forme"], 3),
        "commences_pour_1000_logements_estimes": {
            "toutes": _quantiles(known["commences_pour_1000_logements"]),
            "tendues": _quantiles(tense["commences_pour_1000_logements"]),
            "autres": _quantiles(others["commences_pour_1000_logements"]),
            "spearman_vs_cout": stats.spearman_by_perimeter(
                known, "commences_pour_1000_logements", "indice_cout_pct"
            ),
        },
        "spearman_ratio_estime_vs_cout": {
            "au_plancher": stats.spearman_by_perimeter(ranked, "ratio_estime", "indice_cout_pct"),
            "sans_plancher": stats.spearman_by_perimeter(known, "ratio_estime", "indice_cout_pct"),
        },
        "stock_vs_flux": {
            "besoin_detente_tendues": round(besoin_total),
            "formation_menages_tendues_an": round(float(tense["formation_menages_an"].sum())),
            "annees_de_formation_equivalentes": _ratio(
                besoin_total, float(tense["formation_menages_an"].sum())
            ),
            "fenetre_2017_2022": absorption_block(
                tense[tense["solde_estime_an"] < 0], "annees_absorption", "solde_estime_an"
            ),
            "annees_2023_2024": absorption_block(
                tense[tense["solde_recent_estime_an"] < 0],
                "annees_absorption_recent",
                "solde_recent_estime_an",
            ),
        },
        "fenetres_sensibilite": windows,
        "sensibilite_h08": variants,
        "seuil_classement_formation_an": MIN_FORMATION_PER_YEAR,
        "n_ze_sous_seuil_classement": int(len(known) - len(ranked)),
        "n_ze_sans_sitadel": int(full["commences_an"].isna().sum()),
        "n_ze_census_incomplet": int((full["P22_MEN"].isna() | full["P16_MEN"].isna()).sum()),
        "plus_gros_deficits_estimes": ranked_entries(ranked, "solde_estime_an", True, 12),
        "plus_gros_surplus_estimes": ranked_entries(ranked, "solde_estime_an", False, 8),
        "deficits_tendues_estimes": ranked_entries(
            ranked[ranked["tendue"] & (ranked["solde_estime_an"] < 0)], "solde_estime_an", True, 12
        ),
        "deficits_tendues_2023_2024": ranked_entries(
            ranked[ranked["tendue"] & (ranked["solde_recent_estime_an"] < 0)],
            "solde_recent_estime_an",
            True,
            12,
        ),
    }
