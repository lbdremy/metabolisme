"""Pure transforms for the zones-d'emploi cross (stabilized from
notebooks/exploration/03_vacance_emploi.py).

Crosses LOVAC structural vacancy (S-05) aggregated by zone d'emploi 2020 —
via the commune-membership table (S-06) — with ZE employment dynamics
1998-2018 (S-07). No I/O, no clock; the reads happen in the shell.
"""

from __future__ import annotations

import pandas as pd

from logement.core.lovac import REFERENCE_MILLESIME, plm_parent


class ZeError(Exception):
    """A ZE payload does not have the expected shape."""


def parse_commune_ze(raw: pd.DataFrame) -> pd.DataFrame:
    """Parse the membership table's COM sheet (header on the code row) to code -> ZE2020.

    The COM sheet does NOT list PLM arrondissements (they live in the ARM
    sheet) — callers joining LOVAC communes must map arrondissements to their
    parent commune first (`lovac.plm_parent`).
    """
    for col in ("CODGEO", "ZE2020"):
        if col not in raw.columns:
            raise ZeError(f"missing membership column {col}")
    out = raw[["CODGEO", "ZE2020"]].dropna()
    return pd.DataFrame(
        {
            "code": out["CODGEO"].astype("string").str.strip(),
            "ze": out["ZE2020"].astype("string").str.strip(),
        }
    )


def parse_emploi_ze(raw: pd.DataFrame, *, start: str = "1998", end: str = "2018") -> pd.DataFrame:
    """Parse the 'Emploi total - ZE' sheet into per-ZE employment and mean growth.

    ZE labels arrive as '0051 - Alençon'; the 4-digit code becomes the index.
    """
    df = raw.rename(columns={"Zone d'emploi": "ze"})
    for col in ("ze", start, end):
        if col not in df.columns:
            raise ZeError(f"missing employment column {col}")
    parts = df["ze"].astype("string").str.extract(r"^(\d{4}) - (.*)$")
    out = df.assign(ze_code=parts[0], ze_name=parts[1]).dropna(subset=["ze_code"])
    out = out.set_index("ze_code")[["ze_name", start, end]]
    out[[start, end]] = out[[start, end]].apply(pd.to_numeric, errors="coerce")
    out = out.dropna()
    years = int(end) - int(start)
    out["growth_pct_per_year"] = ((out[end] / out[start]) ** (1 / years) - 1) * 100
    return out.rename(columns={start: "emploi_start", end: "emploi_end"})


def aggregate_vacancy_by_ze(
    lovac_communes: pd.DataFrame, commune_ze: pd.DataFrame
) -> tuple[pd.DataFrame, list[str]]:
    """Aggregate LOVAC structural vacancy by ZE (PLM mapped to parent communes).

    Returns the per-ZE frame and the list of LOVAC commune codes that found
    no ZE (recorded as a limit, never silently dropped).
    """
    ref = REFERENCE_MILLESIME
    cols = [f"pp_vacant_plus_2ans_{ref}", f"ff_pp_total_{ref}"]
    for col in cols:
        if col not in lovac_communes.columns:
            raise ZeError(f"missing LOVAC column {col}")
    frame = lovac_communes.copy()
    frame["code"] = frame["code"].map(plm_parent)
    merged = frame.merge(commune_ze, on="code", how="left")
    unmatched = sorted(merged.loc[merged["ze"].isna(), "code"].unique())
    per_ze = (
        merged.dropna(subset=["ze"])
        .groupby("ze")
        .agg(structural=(cols[0], "sum"), private_stock=(cols[1], "sum"))
    )
    per_ze["structural_rate_pct"] = per_ze["structural"] / per_ze["private_stock"] * 100
    return per_ze, [str(c) for c in unmatched]


def build_summary(
    vacancy_ze: pd.DataFrame, emploi_ze: pd.DataFrame, unmatched: list[str]
) -> dict[str, object]:
    """Assemble the R-03 payload: correlation, declining-ZE shares, top lists."""
    cross = vacancy_ze.join(emploi_ze, how="inner")
    if cross.empty:
        raise ZeError("no ZE joined between vacancy and employment")
    # Spearman as Pearson-on-ranks (no scipy dependency).
    spearman = float(cross["structural_rate_pct"].rank().corr(cross["growth_pct_per_year"].rank()))
    declining = cross["growth_pct_per_year"] < 0

    def ze_entry(row: pd.Series) -> dict[str, object]:
        return {
            "ze": str(row.name),
            "name": row["ze_name"],
            "structural": int(row["structural"]),
            "rate_pct": round(float(row["structural_rate_pct"]), 2),
            "emploi_pct_per_year": round(float(row["growth_pct_per_year"]), 2),
        }

    def top(frame: pd.DataFrame, n: int = 8) -> list[dict[str, object]]:
        ranked = frame.sort_values(
            ["structural", "ze_name"], ascending=[False, True], kind="stable"
        )
        return [ze_entry(r) for _, r in ranked.head(n).iterrows()]

    return {
        "reference_millesime": REFERENCE_MILLESIME,
        "n_ze": len(cross),
        "unmatched_communes": unmatched,
        "spearman_rate_vs_growth": round(spearman, 2),
        "declining_ze": {
            "n": int(declining.sum()),
            "structural_share_pct": round(
                float(cross.loc[declining, "structural"].sum() / cross["structural"].sum() * 100), 1
            ),
            "private_stock_share_pct": round(
                float(
                    cross.loc[declining, "private_stock"].sum() / cross["private_stock"].sum() * 100
                ),
                1,
            ),
            "emploi_share_pct": round(
                float(cross.loc[declining, "emploi_end"].sum() / cross["emploi_end"].sum() * 100), 1
            ),
            "median_rate_pct": round(
                float(cross.loc[declining, "structural_rate_pct"].median()), 1
            ),
        },
        "growing_ze_median_rate_pct": round(
            float(cross.loc[~declining, "structural_rate_pct"].median()), 1
        ),
        "top_declining_by_volume": top(cross[declining]),
        "top_growing_by_volume": top(cross[~declining]),
    }
