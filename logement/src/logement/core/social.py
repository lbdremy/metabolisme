"""Pure transforms for the social-housing mobility cross (stabilized from
notebooks/exploration/13_mobilite_parc_social.py).

Second instruction of the framing hypothesis H-04 (mobilités empêchées):
the RPLS mobility rate (D-17) measures the rotation OFFERED by the
social stock. S-28 publishes the rate as a per-commune RATIO without its
two terms, so the ZE aggregation is a stock-weighted mean — an approved
convention (C-09) CONTROLLED against the published national totals: the
parse refuses to proceed if the weighted commune aggregate drifts from
the France-entière row beyond tolerance. No I/O, no clock.
"""

from __future__ import annotations

import pandas as pd

from logement.core import stats
from logement.core.lovac import plm_parent

# Vintages published as full commune series in S-28 that the study uses:
# the latest (2025), the SDES headline reference (2019) and the first
# published (2013).
RPLS_VINTAGES = (
    ("2025", "tx_mob", "nb_ls"),
    ("2019", "tx_mob_2019", "nb_ls2019"),
    ("2013", "tx_mob_2013", "nb_ls2013"),
)
COMMUNE_COLUMNS = (
    "DEPCOM_ARM",
    "nb_ls",
    "nb_ls2019",
    "nb_ls2013",
    "tx_mob",
    "tx_mob_2019",
    "tx_mob_2013",
    "tx_vac",
    "tx_vac3",
)
# The commune-weighted aggregate must reproduce the published national
# rate: the observed drift of convention C-09 is ≤ 0.011 pt on the three
# vintages — a larger drift means the parse (or the file) broke.
AGGREGATION_TOLERANCE_PT = 0.05
# ZE with a minuscule social stock have unstable rates; they stay in the
# frame but out of rankings and correlations (published threshold).
MIN_PARC_SOCIAL = 500
NATIONAL_ROW = "Total France entière"


class SocialError(Exception):
    """An RPLS payload does not have the expected shape."""


def parse_rpls_communes(raw: pd.DataFrame) -> pd.DataFrame:
    """Parse the S-28 COMMUNE sheet: PLM to parent, numeric rates/stocks.

    The "secret_donnees" variant publishes masked counts as missing
    values (no textual marker): missing stays missing (unknown keeps),
    a missing required column is a definite reject.
    """
    for col in COMMUNE_COLUMNS:
        if col not in raw.columns:
            raise SocialError(f"missing RPLS column {col}")
    out = pd.DataFrame({"code": raw["DEPCOM_ARM"].astype("string").str.strip().map(plm_parent)})
    for col in COMMUNE_COLUMNS[1:]:
        out[col] = pd.to_numeric(raw[col], errors="coerce")
    out = out.dropna(subset=["code"])
    if out.empty:
        raise SocialError("no commune row in the RPLS sheet")
    return out


def parse_rpls_national(raw: pd.DataFrame) -> dict[str, object]:
    """Extract the published France-entière reference row from the REGION sheet."""
    labels = raw.iloc[:, 1].astype("string").str.strip()
    match = raw[labels == NATIONAL_ROW]
    if len(match) != 1:
        raise SocialError(f"expected one '{NATIONAL_ROW}' row, found {len(match)}")
    row = match.iloc[0]
    serie = {}
    for year in range(2013, 2025):
        serie[str(year)] = round(float(row[f"tx_mob_{year}"]), 2)
    serie["2025"] = round(float(row["tx_mob"]), 2)
    return {
        "serie_mobilite_pct": serie,
        "vacance_pct": round(float(row["tx_vac"]), 2),
        "vacance_plus_3_mois_pct": round(float(row["tx_vac3"]), 2),
        "parc_social": int(row["nb_ls"]),
    }


def control_aggregation(communes: pd.DataFrame, national: dict[str, object]) -> dict[str, float]:
    """Check convention C-09 against the published national rates (hard error).

    Returns the per-vintage drift (weighted commune aggregate minus the
    published France-entière rate, in points) for publication.
    """
    serie_obj = national["serie_mobilite_pct"]
    if not isinstance(serie_obj, dict):
        raise SocialError("national reference must carry serie_mobilite_pct")
    serie: dict[str, float] = {}
    for year, rate in serie_obj.items():
        if not isinstance(rate, (int, float)):
            raise SocialError(f"national rate for {year} is not numeric")
        serie[str(year)] = float(rate)
    drifts: dict[str, float] = {}
    for vintage, rate_col, weight_col in RPLS_VINTAGES:
        weights = communes[weight_col]
        approx = float((communes[rate_col] * weights).sum() / weights.sum())
        published = serie[vintage]
        drift = approx - published
        if abs(drift) > AGGREGATION_TOLERANCE_PT:
            raise SocialError(
                f"C-09 aggregation drifts {drift:+.3f} pt from the published "
                f"{vintage} national rate (tolerance {AGGREGATION_TOLERANCE_PT})"
            )
        drifts[vintage] = round(drift, 3)
    return drifts


def _weighted_rate(frame: pd.DataFrame, rate: str, weight: str) -> pd.Series:
    num = (frame[rate] * frame[weight]).groupby(frame["ze"]).sum()
    den = frame.groupby("ze")[weight].sum()
    return num / den


def social_by_ze(communes: pd.DataFrame, commune_ze: pd.DataFrame) -> pd.DataFrame:
    """Aggregate the RPLS rates by ZE (C-09: stock-weighted per vintage)."""
    merged = communes.merge(commune_ze, on="code", how="inner")
    if merged.empty:
        raise SocialError("no commune joined between RPLS and membership table")
    frame = pd.DataFrame(
        {
            "tx_mob_2025": _weighted_rate(merged, "tx_mob", "nb_ls"),
            "tx_mob_2019": _weighted_rate(merged, "tx_mob_2019", "nb_ls2019"),
            "tx_mob_2013": _weighted_rate(merged, "tx_mob_2013", "nb_ls2013"),
            "tx_vac_2025": _weighted_rate(merged, "tx_vac", "nb_ls"),
            "tx_vac3_2025": _weighted_rate(merged, "tx_vac3", "nb_ls"),
            "parc_social": merged.groupby("ze")["nb_ls"].sum(),
        }
    )
    frame["delta_2019_2025"] = frame["tx_mob_2025"] - frame["tx_mob_2019"]
    frame["delta_2013_2025"] = frame["tx_mob_2025"] - frame["tx_mob_2013"]
    # Relative view added by the 2026-08-09 review (SE-4): the flat
    # point-drop across territories hides a proportionally LARGER drop
    # where the 2019 level was already minimal (expensive markets).
    frame["delta_rel_2019_2025_pct"] = frame["delta_2019_2025"] / frame["tx_mob_2019"] * 100
    return frame


def build_summary(
    social: pd.DataFrame,
    national: dict[str, object],
    aggregation_drift: dict[str, float],
    tendue: pd.Series,
    structural_rate_pct: pd.Series,
    indice_cout_pct: pd.Series,
    rotation: pd.DataFrame,
    ze_names: pd.Series,
    tendue_variants: dict[str, pd.Series] | None = None,
) -> dict[str, object]:
    """Assemble the R-12 payload: national fall, ZE geography, segment crosses."""
    small = social["parc_social"] < MIN_PARC_SOCIAL
    frame = (
        social[~small]
        .join(tendue.rename("tendue"), how="left")
        .join(structural_rate_pct.rename("taux_structurelle_pct"), how="left")
        .join(indice_cout_pct.rename("indice_cout_pct"), how="left")
        .join(
            rotation[["part_recents_pct", "delta_pts"]].rename(
                columns={
                    "part_recents_pct": "rotation_rp_pct",
                    "delta_pts": "delta_rotation_rp_pts",
                }
            ),
            how="left",
        )
        .join(ze_names.rename("ze_name"), how="left")
    )
    if frame.empty:
        raise SocialError("no ZE above the social-stock threshold")

    def entry(row: pd.Series) -> dict[str, object]:
        return {
            "ze": str(row.name),
            "name": row["ze_name"] if pd.notna(row["ze_name"]) else None,
            "tx_mob_2025_pct": round(float(row["tx_mob_2025"]), 2),
            "tx_mob_2019_pct": round(float(row["tx_mob_2019"]), 2),
            "delta_2019_2025_pts": round(float(row["delta_2019_2025"]), 2),
            "parc_social": int(row["parc_social"]),
        }

    def ranked(by: str, ascending: bool) -> pd.DataFrame:
        return frame.sort_values([by, "ze_name"], ascending=[ascending, True], kind="stable")

    # 2026-08-09 review (HD-2): an unknown tension status (Mayotte, out
    # of the census-based T-08 frame) is excluded from BOTH medians and
    # counted, instead of being silently filled as « autres ».
    known = frame["tendue"].notna()
    tendues = known & frame["tendue"].fillna(False).astype(bool)
    autres = known & ~frame["tendue"].fillna(True).astype(bool)
    quantiles = frame["tx_mob_2025"].quantile([0.25, 0.5, 0.75])

    def median_or_none(mask: pd.Series, column: str) -> float | None:
        value = frame.loc[mask, column].median()
        return None if pd.isna(value) else round(float(value), 2)

    def tension_block(mask: pd.Series) -> dict[str, float | None]:
        return {
            "tx_mob_2025_pct": median_or_none(mask, "tx_mob_2025"),
            "delta_2019_2025_pts": median_or_none(mask, "delta_2019_2025"),
            "delta_rel_2019_2025_pct": median_or_none(mask, "delta_rel_2019_2025_pct"),
            "tx_vac_2025_pct": median_or_none(mask, "tx_vac_2025"),
        }

    def variant_block(variant: pd.Series) -> dict[str, object]:
        aligned = variant.reindex(frame.index)
        v_known = aligned.notna()
        v_tendues = v_known & aligned.fillna(False).astype(bool)
        v_autres = v_known & ~aligned.fillna(True).astype(bool)
        return {
            "tendues_tx_mob_2025_pct": median_or_none(v_tendues, "tx_mob_2025"),
            "autres_tx_mob_2025_pct": median_or_none(v_autres, "tx_mob_2025"),
            "n_tendues": int(v_tendues.sum()),
        }

    return {
        "national": {**national, "controle_agregation_c09_pt": aggregation_drift},
        "seuil_parc_social": MIN_PARC_SOCIAL,
        "n_ze_total": len(social),
        "n_ze_sous_seuil": int(small.sum()),
        "n_ze": len(frame),
        "distribution_tx_mob_2025_pct": {
            "min": round(float(frame["tx_mob_2025"].min()), 2),
            "q25": round(float(quantiles.loc[0.25]), 2),
            "mediane": round(float(quantiles.loc[0.5]), 2),
            "q75": round(float(quantiles.loc[0.75]), 2),
            "max": round(float(frame["tx_mob_2025"].max()), 2),
        },
        "n_ze_en_baisse_2019_2025": int((frame["delta_2019_2025"] < 0).sum()),
        "n_ze_en_baisse_2013_2025": int((frame["delta_2013_2025"] < 0).sum()),
        "mediane_par_tension": {
            "tendues": tension_block(tendues),
            "autres": tension_block(autres),
            "n_tendues": int(tendues.sum()),
            "n_tension_inconnue": int((~known).sum()),
            "mann_whitney_p_delta": stats.mann_whitney_p(
                frame.loc[tendues, "delta_2019_2025"], frame.loc[autres, "delta_2019_2025"]
            ),
        },
        "sensibilite_h08": {
            label: variant_block(variant) for label, variant in (tendue_variants or {}).items()
        },
        "mobilite_la_plus_faible": [
            entry(r) for _, r in ranked("tx_mob_2025", True).head(8).iterrows()
        ],
        "mobilite_la_plus_forte": [
            entry(r) for _, r in ranked("tx_mob_2025", False).head(8).iterrows()
        ],
        "plus_fortes_baisses": [
            entry(r) for _, r in ranked("delta_2019_2025", True).head(8).iterrows()
        ],
        "spearman_niveau_vs_cout": stats.spearman_by_perimeter(
            frame, "tx_mob_2025", "indice_cout_pct"
        ),
        # SE-5 (2026-08-09 review): the market-mirror gradient predates
        # the study window — publish it at the three vintages so the
        # NEW part (the −0.68 → −0.80 deepening) is visible.
        "spearman_niveau_vs_cout_par_millesime": {
            "2013": stats.spearman_by_perimeter(frame, "tx_mob_2013", "indice_cout_pct"),
            "2019": stats.spearman_by_perimeter(frame, "tx_mob_2019", "indice_cout_pct"),
            "2025": stats.spearman_by_perimeter(frame, "tx_mob_2025", "indice_cout_pct"),
        },
        "spearman_niveau_vs_vacance_privee": stats.spearman_by_perimeter(
            frame, "tx_mob_2025", "taux_structurelle_pct"
        ),
        "spearman_niveau_vs_rotation_rp": stats.spearman_by_perimeter(
            frame, "tx_mob_2025", "rotation_rp_pct"
        ),
        "spearman_delta_vs_delta_rotation_rp": stats.spearman_by_perimeter(
            frame, "delta_2019_2025", "delta_rotation_rp_pts"
        ),
        "spearman_delta_vs_cout": stats.spearman_by_perimeter(
            frame, "delta_2019_2025", "indice_cout_pct"
        ),
        "spearman_niveau_vs_vacance_sociale": stats.spearman_by_perimeter(
            frame, "tx_mob_2025", "tx_vac_2025"
        ),
        "spearman_delta_vs_niveau_2019": stats.spearman_by_perimeter(
            frame, "delta_2019_2025", "tx_mob_2019"
        ),
        "spearman_delta_rel_vs_cout": stats.spearman_by_perimeter(
            frame, "delta_rel_2019_2025_pct", "indice_cout_pct"
        ),
        "partial_delta_vs_cout_controle_niveau_2019": stats.partial_spearman_by_perimeter(
            frame, "delta_2019_2025", "indice_cout_pct", "tx_mob_2019"
        ),
        "partial_delta_rel_vs_cout_controle_niveau_2019": stats.partial_spearman_by_perimeter(
            frame, "delta_rel_2019_2025_pct", "indice_cout_pct", "tx_mob_2019"
        ),
        # SE-6: the raw −0.20 segment cross is manufactured by the two
        # opposite cost gradients — at controlled cost the segments
        # co-vary positively; both figures are published together.
        "partial_niveau_vs_rotation_rp_controle_cout": stats.partial_spearman_by_perimeter(
            frame, "tx_mob_2025", "rotation_rp_pct", "indice_cout_pct"
        ),
    }
