"""Pure transforms for the relocation effort-rate cross (stabilized from
notebooks/exploration/07_taux_effort_relocation.py).

Turns the R-04 abstract cost index into a gross effort rate at relocation
(D-09, gross variant): advert rents mixed house/apartment by the ZE's
primary-residence composition (C-05), Filosofi median standard of living
with the observed persons-per-consumption-unit ratio (C-04), and the H-07
surface-per-person hypothesis. The effort rate is linear in H-07, so the
ZE ranking is invariant — only levels carry the plausible range. No I/O,
no clock; reads happen in the shell.
"""

from __future__ import annotations

import pandas as pd

from logement.core import stats
from logement.core.lovac import REFERENCE_MILLESIME, plm_parent
from logement.models import HypothesisRecord


class EffortError(Exception):
    """An effort payload does not have the expected shape."""


CENSUS_MIX_COLS = ("P22_RPMAISON", "P22_RPAPPART")


def parse_census_mix(raw: pd.DataFrame) -> pd.DataFrame:
    """Parse census house/apartment counts of primary residences per commune.

    PLM arrondissements are summed into their parent commune.
    """
    for col in ("CODGEO", *CENSUS_MIX_COLS):
        if col not in raw.columns:
            raise EffortError(f"missing census column {col}")
    out = pd.DataFrame(
        {
            "code": raw["CODGEO"].astype("string").str.strip().map(plm_parent),
            "rp_maison": pd.to_numeric(raw["P22_RPMAISON"], errors="coerce"),
            "rp_appart": pd.to_numeric(raw["P22_RPAPPART"], errors="coerce"),
        }
    ).dropna()
    return out.groupby("code", as_index=False).sum()


def household_frame(niveau_vie: pd.Series, num_per: pd.Series, num_cu: pd.Series) -> pd.DataFrame:
    """Combine Filosofi ZE series into median income + observed persons/UC.

    The persons/UC ratio is what makes the effort rate independent of any
    reference-household choice (C-04).
    """
    frame = pd.concat(
        [
            niveau_vie.rename("niveau_vie_median"),
            num_per.rename("num_per"),
            num_cu.rename("num_cu"),
        ],
        axis=1,
        join="inner",
    ).dropna()
    if frame.empty:
        raise EffortError("no ZE with all three Filosofi measures")
    if (frame["num_cu"] <= 0).any() or (frame["niveau_vie_median"] <= 0).any():
        raise EffortError("non-positive consumption units or income")
    frame["pers_per_uc"] = frame["num_per"] / frame["num_cu"]
    return frame[["niveau_vie_median", "pers_per_uc"]]


def _weighted_rent_by_ze(
    loyers_commune: pd.DataFrame, parc: pd.DataFrame, commune_ze: pd.DataFrame
) -> pd.Series:
    """Average commune rents per ZE, weighted by the LOVAC private stock."""
    com = (
        loyers_commune.merge(parc, on="code", how="inner")
        .merge(commune_ze, on="code", how="left")
        .dropna(subset=["ze", "loyer_m2", "parc_prive"])
    )
    sums = (
        com.assign(weighted=com["loyer_m2"] * com["parc_prive"])
        .groupby("ze")[["weighted", "parc_prive"]]
        .sum()
    )
    return sums["weighted"] / sums["parc_prive"]


def effort_by_ze(
    loyers_appart: pd.DataFrame,
    loyers_maison: pd.DataFrame,
    census_mix: pd.DataFrame,
    lovac_communes: pd.DataFrame,
    commune_ze: pd.DataFrame,
    households: pd.DataFrame,
    surface_per_person_m2: float,
) -> pd.DataFrame:
    """Cross rents, stock mix, incomes and vacancy into the per-ZE effort frame.

    effort = 12 × rent_mix (€/m²) × H-07 (m²/person) × persons/UC / MED_SL.
    Vacancy is aggregated over all LOVAC communes of the ZE (min_count keeps
    all-secret groups as missing instead of silently zero).
    """
    if surface_per_person_m2 <= 0:
        raise EffortError(f"non-positive surface {surface_per_person_m2}")
    ref = REFERENCE_MILLESIME
    vac_col, stock_col = f"pp_vacant_plus_2ans_{ref}", f"ff_pp_total_{ref}"
    for col in (vac_col, stock_col):
        if col not in lovac_communes.columns:
            raise EffortError(f"missing LOVAC column {col}")
    lovac = lovac_communes.copy()
    lovac["code"] = lovac["code"].map(plm_parent)
    parc = lovac.groupby("code", as_index=False).agg(
        parc_prive=(stock_col, "sum"), structurelle=(vac_col, "sum")
    )

    frame = pd.DataFrame(
        {
            "loyer_appart_m2": _weighted_rent_by_ze(loyers_appart, parc, commune_ze),
            "loyer_maison_m2": _weighted_rent_by_ze(loyers_maison, parc, commune_ze),
        }
    ).dropna()

    mix = (
        census_mix.merge(commune_ze, on="code", how="left")
        .dropna(subset=["ze"])
        .groupby("ze")[["rp_maison", "rp_appart"]]
        .sum()
    )
    total = mix["rp_maison"] + mix["rp_appart"]
    frame = frame.join((mix["rp_maison"] / total).rename("part_maison"), how="inner")
    frame = frame.join(households, how="inner")
    if frame.empty:
        raise EffortError("no ZE joined between rents, census mix and incomes")

    frame["loyer_mix_m2"] = (
        frame["part_maison"] * frame["loyer_maison_m2"]
        + (1 - frame["part_maison"]) * frame["loyer_appart_m2"]
    )
    frame["surface_per_uc"] = surface_per_person_m2 * frame["pers_per_uc"]
    annual_per_uc = 12 * frame["surface_per_uc"] / frame["niveau_vie_median"] * 100
    frame["effort_brut_pct"] = frame["loyer_mix_m2"] * annual_per_uc
    frame["effort_appart_pct"] = frame["loyer_appart_m2"] * annual_per_uc

    vacancy = (
        lovac.merge(commune_ze, on="code", how="left")
        .dropna(subset=["ze"])
        .groupby("ze")[[vac_col, stock_col]]
        .sum(min_count=1)
        .rename(columns={vac_col: "structurelle", stock_col: "parc_prive"})
    )
    vacancy["taux_structurelle_pct"] = vacancy["structurelle"] / vacancy["parc_prive"] * 100
    return frame.join(vacancy, how="inner")


def _quantiles_pct(series: pd.Series) -> dict[str, float]:
    quantiles = series.quantile([0, 0.1, 0.25, 0.5, 0.75, 0.9, 1])
    keys = ("min", "p10", "p25", "median", "p75", "p90", "max")
    return {k: round(float(v), 1) for k, v in zip(keys, quantiles, strict=True)}


def build_summary(
    effort_ze: pd.DataFrame, ze_names: pd.Series, h07: HypothesisRecord
) -> dict[str, object]:
    """Assemble the R-06 payload: distribution, sensitivities, extremes, vacancy."""
    frame = effort_ze.join(ze_names.rename("ze_name"), how="left")
    central = h07.central_value
    low, high = h07.plausible_range
    effort = frame["effort_brut_pct"]
    perimetres = stats.spearman_by_perimeter(frame, "effort_brut_pct", "taux_structurelle_pct")
    high_effort = effort > effort.median()

    def entry(row: pd.Series) -> dict[str, object]:
        return {
            "ze": str(row.name),
            "name": row["ze_name"] if pd.notna(row["ze_name"]) else None,
            "loyer_mix_m2": round(float(row["loyer_mix_m2"]), 2),
            "part_maison_pct": round(float(row["part_maison"]) * 100, 1),
            "niveau_vie_median": int(row["niveau_vie_median"]),
            "pers_per_uc": round(float(row["pers_per_uc"]), 2),
            "effort_brut_pct": round(float(row["effort_brut_pct"]), 1),
            "effort_range_pct": [
                round(float(row["effort_brut_pct"]) * low / central, 1),
                round(float(row["effort_brut_pct"]) * high / central, 1),
            ],
            "taux_structurelle_pct": round(float(row["taux_structurelle_pct"]), 2),
        }

    def extremes(ascending: bool, count: int) -> list[dict[str, object]]:
        ranked = frame.sort_values(
            ["effort_brut_pct", "ze_name"], ascending=[ascending, True], kind="stable"
        )
        return [entry(r) for _, r in ranked.head(count).iterrows()]

    return {
        "reference_millesime": REFERENCE_MILLESIME,
        "hypothesis": {
            "id": h07.id,
            "name": h07.name,
            "central_value_m2_per_person": central,
            "plausible_range": [low, high],
        },
        "n_ze": len(frame),
        "effort_brut_pct_quantiles": _quantiles_pct(effort),
        "median_effort_by_h07_pct": {
            "low": round(float(effort.median()) * low / central, 1),
            "central": round(float(effort.median()), 1),
            "high": round(float(effort.median()) * high / central, 1),
        },
        "appart_only": {
            "median_effort_pct": round(float(frame["effort_appart_pct"].median()), 1),
            "spearman_vs_mix": round(
                float(effort.rank().corr(frame["effort_appart_pct"].rank())), 3
            ),
        },
        "spearman_effort_vs_vacancy": perimetres["france_entiere"]["rho"],
        "spearman_perimetres": perimetres,
        "median_vacancy_rate_pct": {
            "high_effort_half": round(
                float(frame.loc[high_effort, "taux_structurelle_pct"].median()), 1
            ),
            "low_effort_half": round(
                float(frame.loc[~high_effort, "taux_structurelle_pct"].median()), 1
            ),
        },
        "part_maison_pct": {
            "min": round(float(frame["part_maison"].min()) * 100, 1),
            "median": round(float(frame["part_maison"].median()) * 100, 1),
            "max": round(float(frame["part_maison"].max()) * 100, 1),
        },
        "pers_per_uc": {
            "min": round(float(frame["pers_per_uc"].min()), 2),
            "median": round(float(frame["pers_per_uc"].median()), 2),
            "max": round(float(frame["pers_per_uc"].max()), 2),
        },
        "top_effort": extremes(ascending=False, count=8),
        "bottom_effort": extremes(ascending=True, count=5),
    }
