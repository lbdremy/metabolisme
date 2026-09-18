"""Pure transforms for the housing FLOW cross (article 3, 2026-09-18).

The proposal P-01 detends a STOCK (194 488 dwellings, R-07) while
households keep forming (L-19/L-32). This module asks, per zone
d'emploi, whether new construction keeps pace with household formation
— and where it does not:

- household formation per year from the census vintages 2016 → 2022
  (S-11: P16_MEN, P22_MEN — six years between vintages, D-05);
- dwellings STARTED per year from Sitadel (S-54, « Tous Logements »,
  date de prise en compte, D-24) over the same window;
- the dwellings NEEDED per household formed to keep the ZE's observed
  structure (share of secondary residences and vacancy in 2022)
  constant: Δparc = Δménages / (1 − part_rs − part_vac);
- the resulting yearly surplus or deficit, its geography (tense ZE vs
  others, cost gradient), and what it means for the detente stock: the
  years the stock would last if the flow deficit of the tense ZE ate it.

Descriptive arithmetic; no behavioural model, no new hypothesis — the
« needed » dwellings use each ZE's own 2022 structure, never a norm.
No I/O, no clock — reads happen in the shell.
"""

from __future__ import annotations

import pandas as pd

from logement.core import stats
from logement.core.lovac import plm_parent

CENSUS_FLOW_COLS = (
    "P11_MEN",
    "P16_MEN",
    "P22_MEN",
    "P11_LOG",
    "P16_LOG",
    "P22_LOG",
    "P22_RP",
    "P22_RSECOCC",
    "P22_LOGVAC",
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
# Census vintages are centred on their survey window (2016 = 2014-2018,
# 2022 = 2020-2024): six years between the two centres.
VINTAGE_YEARS = 6
# Construction window aligned on the census window (D-24: date de prise
# en compte, so the last months of 2022 events fall in 2023 — a
# multi-year mean absorbs it); the long window is published beside it.
WINDOW = (2017, 2022)
LONG_WINDOW = (2013, 2024)
# Ranking floor: a ZE forming fewer households per year than this stays
# in the frame and the medians but out of the published rankings.
MIN_FORMATION_PER_YEAR = 200.0


class FluxError(Exception):
    """A flow payload does not have the expected shape."""


# ---------------------------------------------------------------- parsing


def parse_census_vintages(raw: pd.DataFrame) -> pd.DataFrame:
    """Parse the S-11 commune rows into the three-vintage counts (PLM → parent)."""
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
    """Reduce Sitadel monthly rows to « Tous Logements » sums per commune × year.

    The acquisition step (`logement acquire-sitadel`, S-54): the other
    TYPE_LGT rows are components of « Tous Logements » and would double
    count. Communes keep their published code (PLM arrondissements are
    mapped later, at parse time).
    """
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


def parse_sitadel_annual(raw: pd.DataFrame) -> pd.DataFrame:
    """Parse the frozen annual extract (S-54) into starts per commune × year.

    PLM arrondissements are summed into their parent commune; a missing
    count is a definite reject at the row level (dropped), never zero.
    """
    for col in ("CODE_INSEE", "ANNEE", "LOG_COM", "LOG_AUT"):
        if col not in raw.columns:
            raise FluxError(f"missing Sitadel column {col}")
    frame = pd.DataFrame(
        {
            "code": raw["CODE_INSEE"].astype("string").str.strip().map(plm_parent),
            "annee": pd.to_numeric(raw["ANNEE"], errors="coerce"),
            "log_com": pd.to_numeric(raw["LOG_COM"], errors="coerce"),
            "log_aut": pd.to_numeric(raw["LOG_AUT"], errors="coerce"),
        }
    ).dropna()
    if frame.empty:
        raise FluxError("no usable row in the Sitadel extract")
    frame["annee"] = frame["annee"].astype(int)
    return frame.groupby(["code", "annee"], as_index=False)[["log_com", "log_aut"]].sum()


# ------------------------------------------------------------------ per ZE


def _window_mean(
    annual: pd.DataFrame, commune_ze: pd.DataFrame, window: tuple[int, int]
) -> pd.Series:
    first, last = window
    rows = annual[(annual["annee"] >= first) & (annual["annee"] <= last)]
    if rows.empty:
        raise FluxError(f"no Sitadel row in window {window}")
    years = last - first + 1
    merged = rows.merge(commune_ze, on="code", how="inner")
    return merged.groupby("ze")["log_com"].sum() / years


def flux_by_ze(
    census: pd.DataFrame,
    sitadel_annual: pd.DataFrame,
    commune_ze: pd.DataFrame,
) -> pd.DataFrame:
    """Cross household formation, stock growth and starts into the per-ZE flow frame."""
    merged = census.merge(commune_ze, on="code", how="inner")
    if merged.empty:
        raise FluxError("no commune joined between census and membership table")
    frame = merged.groupby("ze")[list(CENSUS_FLOW_COLS)].sum()
    frame["formation_menages_an"] = (frame["P22_MEN"] - frame["P16_MEN"]) / VINTAGE_YEARS
    frame["formation_menages_an_2011_2016"] = (frame["P16_MEN"] - frame["P11_MEN"]) / (2016 - 2011)
    frame["croissance_parc_an"] = (frame["P22_LOG"] - frame["P16_LOG"]) / VINTAGE_YEARS
    frame["part_rs_2022"] = frame["P22_RSECOCC"] / frame["P22_LOG"]
    frame["part_vac_2022"] = frame["P22_LOGVAC"] / frame["P22_LOG"]
    # Dwellings needed per household formed to keep the 2022 structure.
    denominator = 1 - frame["part_rs_2022"] - frame["part_vac_2022"]
    if (denominator <= 0).any():
        raise FluxError("a ZE has no primary-residence share left")
    frame["logements_par_menage_forme"] = 1 / denominator
    frame["besoin_flux_an"] = (
        frame["formation_menages_an"].clip(lower=0) * frame["logements_par_menage_forme"]
    )
    frame["commences_an"] = _window_mean(sitadel_annual, commune_ze, WINDOW).reindex(frame.index)
    frame["commences_an_long"] = _window_mean(sitadel_annual, commune_ze, LONG_WINDOW).reindex(
        frame.index
    )
    # Variant WITHOUT the secondary-residence flow: only the vacancy share
    # is kept constant (a touristic ZE's 2022 structure would otherwise
    # require building secondary residences for each household formed).
    frame["besoin_flux_hors_rs_an"] = frame["formation_menages_an"].clip(lower=0) / (
        1 - frame["part_vac_2022"]
    )
    frame["solde_flux_an"] = frame["commences_an"] - frame["besoin_flux_an"]
    frame["solde_flux_hors_rs_an"] = frame["commences_an"] - frame["besoin_flux_hors_rs_an"]
    frame["ratio_production"] = frame["commences_an"] / frame["besoin_flux_an"]
    frame.loc[frame["besoin_flux_an"] <= 0, "ratio_production"] = float("nan")
    frame["commences_pour_1000_logements"] = frame["commences_an"] / frame["P22_LOG"] * 1000
    # Internal consistency: starts minus observed stock growth = dwellings
    # that left the stock (demolitions, mergers, changes of use) — or
    # starts not yet delivered; published, never assumed.
    frame["disparitions_implicites_an"] = frame["commences_an"] - frame["croissance_parc_an"]
    return frame


# -------------------------------------------------------------- summary


def _quantiles(series: pd.Series, digits: int = 2) -> dict[str, float]:
    clean = series.dropna()
    quantiles = clean.quantile([0, 0.25, 0.5, 0.75, 1])
    keys = ("min", "p25", "median", "p75", "max")
    return {k: round(float(v), digits) for k, v in zip(keys, quantiles, strict=True)}


def _entry(row: pd.Series) -> dict[str, object]:
    ratio = row["ratio_production"]
    return {
        "ze": str(row.name),
        "name": row["ze_name"] if pd.notna(row["ze_name"]) else None,
        "formation_menages_an": round(float(row["formation_menages_an"])),
        "besoin_flux_an": round(float(row["besoin_flux_an"])),
        "commences_an": round(float(row["commences_an"])),
        "solde_flux_an": round(float(row["solde_flux_an"])),
        "solde_flux_hors_rs_an": round(float(row["solde_flux_hors_rs_an"])),
        "part_rs_2022_pct": round(float(row["part_rs_2022"]) * 100, 1),
        "ratio_production": None if pd.isna(ratio) else round(float(ratio), 2),
        "tendue": bool(row["tendue"]),
    }


def build_summary(
    frame: pd.DataFrame,
    tendue: pd.Series,
    cost_index: pd.Series,
    ze_names: pd.Series,
    besoin_detente: float,
    tendue_variants: dict[str, pd.Series] | None = None,
) -> dict[str, object]:
    """Assemble the R-18 payload: national, tense vs others, gradient, rankings."""
    if besoin_detente <= 0:
        raise FluxError("non-positive detente need")
    full = (
        frame.join(tendue.rename("tendue"), how="left")
        .join(cost_index.rename("indice_cout_pct"), how="left")
        .join(ze_names.rename("ze_name"), how="left")
    )
    full["tendue"] = full["tendue"].fillna(False).astype(bool)
    known = full.dropna(subset=["commences_an"])
    if known.empty:
        raise FluxError("no ZE with Sitadel starts")

    def national(sub: pd.DataFrame) -> dict[str, object]:
        formation = float(sub["formation_menages_an"].sum())
        besoin = float(sub["besoin_flux_an"].sum())
        commences = float(sub["commences_an"].sum())
        deficit = float((-sub["solde_flux_an"]).clip(lower=0).sum())
        return {
            "n_ze": len(sub),
            "menages_2016": round(float(sub["P16_MEN"].sum())),
            "menages_2022": round(float(sub["P22_MEN"].sum())),
            "formation_menages_an": round(formation),
            "croissance_parc_an": round(float(sub["croissance_parc_an"].sum())),
            "besoin_flux_an": round(besoin),
            "commences_an": round(commences),
            "commences_an_long": round(float(sub["commences_an_long"].sum())),
            "solde_flux_an": round(commences - besoin),
            "besoin_flux_hors_rs_an": round(float(sub["besoin_flux_hors_rs_an"].sum())),
            "solde_flux_hors_rs_an": round(commences - float(sub["besoin_flux_hors_rs_an"].sum())),
            "deficit_hors_rs_des_ze_deficitaires_an": round(
                float((-sub["solde_flux_hors_rs_an"]).clip(lower=0).sum())
            ),
            "ratio_production": round(commences / besoin, 2) if besoin > 0 else None,
            "deficit_des_ze_deficitaires_an": round(deficit),
            "n_ze_deficitaires": int((sub["solde_flux_an"] < 0).sum()),
            "n_ze_menages_en_baisse": int((sub["formation_menages_an"] < 0).sum()),
            "disparitions_implicites_an": round(float(sub["disparitions_implicites_an"].sum())),
        }

    tense = known[known["tendue"]]
    others = known[~known["tendue"]]
    tense_deficit = float((-tense["solde_flux_an"]).clip(lower=0).sum())
    tense_deficit_hors_rs = float((-tense["solde_flux_hors_rs_an"]).clip(lower=0).sum())
    tense_solde = float(tense["solde_flux_an"].sum())
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
    ranked = known[known["formation_menages_an"] >= MIN_FORMATION_PER_YEAR]
    rho = stats.spearman_by_perimeter(known, "ratio_production", "indice_cout_pct")
    mw = stats.mann_whitney_p(
        tense["ratio_production"].dropna(), others["ratio_production"].dropna()
    )
    variants = {}
    for label, flag in (tendue_variants or {}).items():
        sub = known.join(flag.rename("t"), how="left")
        sub["t"] = sub["t"].fillna(False).astype(bool)
        t_sub, o_sub = sub[sub["t"]], sub[~sub["t"]]
        variants[label] = {
            "n_ze_tendues": len(t_sub),
            "ratio_median_tendues": round(float(t_sub["ratio_production"].median()), 2),
            "ratio_median_autres": round(float(o_sub["ratio_production"].median()), 2),
            "solde_flux_tendues_an": round(float(t_sub["solde_flux_an"].sum())),
        }
    return {
        "fenetres": {
            "menages": "2016 → 2022 (millésimes censitaires, 6 ans)",
            "commences": f"{WINDOW[0]}-{WINDOW[1]} (moyenne annuelle, date de prise en compte)",
            "commences_long": f"{LONG_WINDOW[0]}-{LONG_WINDOW[1]}",
        },
        "modele": (
            "besoin de flux = ménages formés / (1 − part RS 2022 − part vacants 2022) ; "
            "variante hors RS = ménages formés / (1 − part vacants 2022) ; "
            "solde = commencés − besoin ; pas d'hypothèse nouvelle"
        ),
        "national": national(known),
        "tendues": national(tense),
        "autres": national(others),
        "parts_des_ze_tendues": shares,
        "ratio_production": {
            "toutes": _quantiles(known["ratio_production"]),
            "tendues": _quantiles(tense["ratio_production"]),
            "autres": _quantiles(others["ratio_production"]),
            "mann_whitney_p_tendues_vs_autres": mw,
        },
        "logements_par_menage_forme": _quantiles(known["logements_par_menage_forme"], 3),
        "commences_pour_1000_logements": {
            "toutes": _quantiles(known["commences_pour_1000_logements"]),
            "tendues": _quantiles(tense["commences_pour_1000_logements"]),
            "autres": _quantiles(others["commences_pour_1000_logements"]),
        },
        "spearman_ratio_vs_cout": rho,
        "stock_vs_flux": {
            "besoin_detente": round(besoin_detente),
            "solde_flux_tendues_an": round(tense_solde),
            "deficit_des_ze_tendues_deficitaires_an": round(tense_deficit),
            "annees_avant_absorption_par_le_deficit": (
                round(besoin_detente / tense_deficit, 1) if tense_deficit > 0 else None
            ),
            "deficit_hors_rs_des_ze_tendues_deficitaires_an": round(tense_deficit_hors_rs),
            "annees_avant_absorption_hors_rs": (
                round(besoin_detente / tense_deficit_hors_rs, 1)
                if tense_deficit_hors_rs > 0
                else None
            ),
            "formation_menages_tendues_an": round(float(tense["formation_menages_an"].sum())),
            "annees_de_formation_equivalentes": round(
                besoin_detente / float(tense["formation_menages_an"].sum()), 2
            )
            if float(tense["formation_menages_an"].sum()) > 0
            else None,
        },
        "seuil_classement_formation_an": MIN_FORMATION_PER_YEAR,
        "n_ze_sous_seuil_classement": int(len(known) - len(ranked)),
        "n_ze_sans_sitadel": int(full["commences_an"].isna().sum()),
        "sensibilite_h08": variants,
        "plus_gros_deficits": [
            _entry(r)
            for _, r in ranked.sort_values(["solde_flux_an", "ze_name"], kind="stable")
            .head(12)
            .iterrows()
        ],
        "plus_gros_surplus": [
            _entry(r)
            for _, r in ranked.sort_values(
                ["solde_flux_an", "ze_name"], ascending=[False, True], kind="stable"
            )
            .head(8)
            .iterrows()
        ],
        "deficits_tendues": [
            _entry(r)
            for _, r in ranked[ranked["tendue"] & (ranked["solde_flux_an"] < 0)]
            .sort_values(["solde_flux_an", "ze_name"], kind="stable")
            .head(12)
            .iterrows()
        ],
    }
