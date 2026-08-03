"""Pure transforms for the residential-cost cross (stabilized from
notebooks/exploration/04_cout_residentiel.py).

Builds the ZE cost-pressure index — stock-weighted advert rent per m² (S-09)
over Filosofi median standard of living (S-10) — and crosses it with LOVAC
structural vacancy. No I/O, no clock; reads happen in the shell.
"""

from __future__ import annotations

import pandas as pd

from logement.core.lovac import REFERENCE_MILLESIME, plm_parent


class CoutError(Exception):
    """A cost payload does not have the expected shape."""


def parse_loyers(raw: pd.DataFrame) -> pd.DataFrame:
    """Parse a Carte des loyers file: commune code + predicted rent €/m².

    French decimal commas; PLM arrondissements mapped to parent communes and
    averaged (the source predicts at arrondissement level).
    """
    for col in ("INSEE_C", "loypredm2"):
        if col not in raw.columns:
            raise CoutError(f"missing rent column {col}")
    out = pd.DataFrame(
        {
            "code": raw["INSEE_C"].astype("string").str.strip().map(plm_parent),
            "loyer_m2": pd.to_numeric(
                raw["loypredm2"].astype("string").str.replace(",", "."), errors="coerce"
            ),
        }
    ).dropna()
    return out.groupby("code", as_index=False).agg(loyer_m2=("loyer_m2", "mean"))


def parse_filosofi(raw: pd.DataFrame, *, geo_object: str, measure: str) -> pd.Series:
    """Extract one Filosofi measure at one geographic level from the long table."""
    for col in ("GEO", "GEO_OBJECT", "FILOSOFI_MEASURE", "OBS_VALUE"):
        if col not in raw.columns:
            raise CoutError(f"missing Filosofi column {col}")
    sub = raw[(raw["GEO_OBJECT"] == geo_object) & (raw["FILOSOFI_MEASURE"] == measure)]
    if sub.empty:
        raise CoutError(f"no Filosofi rows for {geo_object}/{measure}")
    series = pd.Series(
        pd.to_numeric(sub["OBS_VALUE"], errors="coerce").values,
        index=sub["GEO"].astype("string").str.strip().values,
        name=measure,
    )
    return series.dropna()


def cost_index_by_ze(
    loyers_commune: pd.DataFrame,
    lovac_communes: pd.DataFrame,
    commune_ze: pd.DataFrame,
    niveau_vie: pd.Series,
) -> pd.DataFrame:
    """Cross rents, stock, vacancy and incomes into the per-ZE cost frame.

    Rent is weighted by the LOVAC private stock (the rent "seen by the
    stock"); the index is the annual rent of one m² as % of the median
    standard of living.
    """
    ref = REFERENCE_MILLESIME
    vac_col, stock_col = f"pp_vacant_plus_2ans_{ref}", f"ff_pp_total_{ref}"
    for col in (vac_col, stock_col):
        if col not in lovac_communes.columns:
            raise CoutError(f"missing LOVAC column {col}")
    lovac = lovac_communes.copy()
    lovac["code"] = lovac["code"].map(plm_parent)
    parc = lovac.groupby("code", as_index=False).agg(
        parc_prive=(stock_col, "sum"), structurelle=(vac_col, "sum")
    )
    com = (
        loyers_commune.merge(parc, on="code", how="inner")
        .merge(commune_ze, on="code", how="left")
        .dropna(subset=["ze", "loyer_m2", "parc_prive"])
    )
    grouped = com.groupby("ze").apply(
        lambda g: pd.Series(
            {
                "loyer_m2": (g["loypredm2"] if "loypredm2" in g else g["loyer_m2"])
                .mul(g["parc_prive"])
                .sum()
                / g["parc_prive"].sum(),
                "parc_prive": g["parc_prive"].sum(),
                "structurelle": g["structurelle"].sum(),
            }
        ),
        include_groups=False,
    )
    grouped["taux_structurelle_pct"] = grouped["structurelle"] / grouped["parc_prive"] * 100
    joined = grouped.join(niveau_vie.rename("niveau_vie_median"), how="inner")
    if joined.empty:
        raise CoutError("no ZE joined between rents and incomes")
    joined["indice_cout_pct"] = joined["loyer_m2"] * 12 / joined["niveau_vie_median"] * 100
    return joined


def build_summary(cost_ze: pd.DataFrame, ze_names: pd.Series) -> dict[str, object]:
    """Assemble the R-04 payload: correlation, halves, extreme ZE lists."""
    frame = cost_ze.join(ze_names.rename("ze_name"), how="left")
    spearman = float(frame["indice_cout_pct"].rank().corr(frame["taux_structurelle_pct"].rank()))
    expensive = frame["indice_cout_pct"] > frame["indice_cout_pct"].median()

    def entry(row: pd.Series) -> dict[str, object]:
        return {
            "ze": str(row.name),
            "name": row["ze_name"] if pd.notna(row["ze_name"]) else None,
            "loyer_m2": round(float(row["loyer_m2"]), 2),
            "niveau_vie_median": int(row["niveau_vie_median"]),
            "indice_cout_pct": round(float(row["indice_cout_pct"]), 2),
            "taux_structurelle_pct": round(float(row["taux_structurelle_pct"]), 2),
        }

    def extremes(ascending: bool) -> list[dict[str, object]]:
        ranked = frame.sort_values(
            ["indice_cout_pct", "ze_name"], ascending=[ascending, True], kind="stable"
        )
        return [entry(r) for _, r in ranked.head(6).iterrows()]

    return {
        "reference_millesime": REFERENCE_MILLESIME,
        "n_ze": len(frame),
        "spearman_cost_vs_vacancy": round(spearman, 2),
        "median_vacancy_rate_pct": {
            "expensive_half": round(
                float(frame.loc[expensive, "taux_structurelle_pct"].median()), 1
            ),
            "cheap_half": round(float(frame.loc[~expensive, "taux_structurelle_pct"].median()), 1),
        },
        "loyer_m2_range": {
            "min": round(float(frame["loyer_m2"].min()), 1),
            "median": round(float(frame["loyer_m2"].median()), 1),
            "max": round(float(frame["loyer_m2"].max()), 1),
        },
        "top_cost_index": extremes(ascending=False),
        "bottom_cost_index": extremes(ascending=True),
    }
