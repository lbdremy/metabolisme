"""Pure transforms for the secondary-residences cross (stabilized from
notebooks/exploration/05_residences_secondaires.py).

Computes the secondary-residence share by zone d'emploi from the census
housing base (S-11) and crosses it with the LOVAC structural-vacancy rate
and the cost-pressure index. No I/O, no clock; reads happen in the shell.
"""

from __future__ import annotations

import pandas as pd

from logement.core.lovac import plm_parent

CENSUS_COLS = ("P22_LOG", "P22_RP", "P22_RSECOCC", "P22_LOGVAC")
TOURISTIC_RS_THRESHOLD_PCT = 20.0


class RsError(Exception):
    """A census payload does not have the expected shape."""


def parse_census_housing(raw: pd.DataFrame) -> pd.DataFrame:
    """Parse the base-cc-logement commune rows into numeric counts.

    The base lists both PLM parent communes and their arrondissements: codes
    are mapped to the parent and the duplicated arrondissement rows dropped
    (keeping the parent totals, which come first).
    """
    for col in ("CODGEO", *CENSUS_COLS):
        if col not in raw.columns:
            raise RsError(f"missing census column {col}")
    out = pd.DataFrame({"code": raw["CODGEO"].astype("string").str.strip().map(plm_parent)})
    for col in CENSUS_COLS:
        out[col] = pd.to_numeric(raw[col], errors="coerce")
    return out.drop_duplicates(subset="code", keep="first")


def rs_by_ze(census: pd.DataFrame, commune_ze: pd.DataFrame) -> pd.DataFrame:
    """Aggregate the census housing counts by ZE and derive category shares."""
    merged = census.merge(commune_ze, on="code", how="inner")
    if merged.empty:
        raise RsError("no commune joined between census and membership table")
    per_ze = merged.groupby("ze")[list(CENSUS_COLS)].sum()
    per_ze["part_rs_pct"] = per_ze["P22_RSECOCC"] / per_ze["P22_LOG"] * 100
    per_ze["part_vac_rp_pct"] = per_ze["P22_LOGVAC"] / per_ze["P22_LOG"] * 100
    return per_ze


def build_summary(
    rs_ze: pd.DataFrame, cost_ze: pd.DataFrame, ze_names: pd.Series
) -> dict[str, object]:
    """Assemble the R-05 payload: RS shares, correlations, touristic-group stats."""
    frame = rs_ze.join(cost_ze, how="inner").join(ze_names.rename("ze_name"), how="left")
    if frame.empty:
        raise RsError("no ZE joined between census and cost frames")
    touristic = frame["part_rs_pct"] > TOURISTIC_RS_THRESHOLD_PCT

    def entry(row: pd.Series) -> dict[str, object]:
        return {
            "ze": str(row.name),
            "name": row["ze_name"] if pd.notna(row["ze_name"]) else None,
            "part_rs_pct": round(float(row["part_rs_pct"]), 1),
            "indice_cout_pct": round(float(row["indice_cout_pct"]), 2),
            "taux_structurelle_pct": round(float(row["taux_structurelle_pct"]), 2),
        }

    top_rs = frame.sort_values(["part_rs_pct", "ze_name"], ascending=[False, True], kind="stable")
    rs_and_vacant = frame[touristic & (frame["taux_structurelle_pct"] > 5)]
    return {
        "n_ze": len(frame),
        "national_rs_share_pct": round(
            float(frame["P22_RSECOCC"].sum() / frame["P22_LOG"].sum() * 100), 1
        ),
        "median_ze_rs_share_pct": round(float(frame["part_rs_pct"].median()), 1),
        "spearman_rs_vs_structural_vacancy": round(
            float(frame["part_rs_pct"].rank().corr(frame["taux_structurelle_pct"].rank())), 2
        ),
        "spearman_rs_vs_cost_index": round(
            float(frame["part_rs_pct"].rank().corr(frame["indice_cout_pct"].rank())), 2
        ),
        "touristic_ze": {
            "threshold_rs_pct": TOURISTIC_RS_THRESHOLD_PCT,
            "n": int(touristic.sum()),
            "median_structural_vacancy_pct": round(
                float(frame.loc[touristic, "taux_structurelle_pct"].median()), 1
            ),
            "others_median_structural_vacancy_pct": round(
                float(frame.loc[~touristic, "taux_structurelle_pct"].median()), 1
            ),
            "median_cost_index_pct": round(
                float(frame.loc[touristic, "indice_cout_pct"].median()), 2
            ),
            "others_median_cost_index_pct": round(
                float(frame.loc[~touristic, "indice_cout_pct"].median()), 2
            ),
        },
        "top_rs_share": [entry(r) for _, r in top_rs.head(8).iterrows()],
        "rs_and_vacancy_outliers": [entry(r) for _, r in rs_and_vacant.iterrows()],
    }
