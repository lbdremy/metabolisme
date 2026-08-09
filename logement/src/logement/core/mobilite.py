"""Pure transforms for the residential-rotation cross (stabilized from
notebooks/exploration/12_mobilite_anem.py).

First instruction of the framing hypothesis H-04 (mobilités empêchées):
the observable trace of blocked household moves is the effective rotation
of the stock, measured by the move-in duration of primary residences
(D-16, dimension L_STAY of the RP2023 Melodi dataset S-27). Computes the
recent-mover share by zone d'emploi over the three comparable vintages
(2012, 2017, 2023) and crosses its level and its 2012→2023 drop with the
R-07 tension flag, the LOVAC structural-vacancy rate and the R-04 cost
index. No I/O, no clock; reads happen in the shell.
"""

from __future__ import annotations

import pandas as pd

from logement.core import stats

# Ordered European L_STAY classes of S-27 (D-16): years since the first
# occupant moved in. The published headline share is the "moins de 2 ans"
# class; "moins de 5 ans" (Y_LT2 + Y2T4) is carried as a robustness view.
LSTAY_CLASSES = ("Y_LT2", "Y2T4", "Y5T9", "Y10T19", "Y20T29", "Y_GE30")
LSTAY_TOTAL = "_T"
# France hors Mayotte — the S-27 perimeter; FM (métropole) also exists in
# the file but national figures are published on F only (périmètre unique).
NATIONAL_GEO = "F"
VINTAGES = (2012, 2017, 2023)
# The six classes must re-sum to the diffused total: the weighted census
# counts are consistent by construction, so any drift is a parsing error.
CLASS_SUM_RTOL = 1e-6

REQUIRED_COLUMNS = ("GEO_OBJECT", "GEO", "TIME_PERIOD", "L_STAY", "OBS_VALUE")


class MobiliteError(Exception):
    """An S-27 rotation payload does not have the expected shape."""


def parse_lstay(raw: pd.DataFrame) -> pd.DataFrame:
    """Pivot the Melodi long cut into a (level, geo, year) × L_STAY wide frame.

    Expects the shell's slice of S-27: measure DWELLINGS, primary
    residences (OCS=DW_MAIN), every other dimension at its total, with
    the L_STAY detail AND its `_T` total. Rejects a frame whose class
    sums drift from the diffused totals (parse error, not data noise).
    """
    for col in REQUIRED_COLUMNS:
        if col not in raw.columns:
            raise MobiliteError(f"missing L_STAY column {col}")
    out = raw[list(REQUIRED_COLUMNS)].copy()
    for col in ("GEO_OBJECT", "GEO", "L_STAY"):
        out[col] = out[col].astype("string").str.strip()
    out["annee"] = pd.to_datetime(out["TIME_PERIOD"]).dt.year
    out["OBS_VALUE"] = pd.to_numeric(out["OBS_VALUE"], errors="coerce")
    wide = out.pivot_table(
        index=["GEO_OBJECT", "GEO", "annee"],
        columns="L_STAY",
        values="OBS_VALUE",
        aggfunc="first",
    )
    for col in (*LSTAY_CLASSES, LSTAY_TOTAL):
        if col not in wide.columns:
            raise MobiliteError(f"missing L_STAY class {col}")
    wide = wide[[*LSTAY_CLASSES, LSTAY_TOTAL]].dropna()
    if wide.empty:
        raise MobiliteError("no complete (geo, year) row in the L_STAY cut")
    drift = (wide[list(LSTAY_CLASSES)].sum(axis=1) - wide[LSTAY_TOTAL]).abs() / wide[LSTAY_TOTAL]
    if float(drift.max()) > CLASS_SUM_RTOL:
        raise MobiliteError(f"L_STAY classes drift from totals (max rel {float(drift.max()):.2e})")
    return wide


def rotation_parts(wide: pd.DataFrame) -> pd.DataFrame:
    """Derive per-class shares (%) plus the recent-mover aggregates."""
    parts = wide[list(LSTAY_CLASSES)].div(wide[LSTAY_TOTAL], axis=0) * 100
    parts["moins_2_ans_pct"] = parts["Y_LT2"]
    parts["moins_5_ans_pct"] = parts["Y_LT2"] + parts["Y2T4"]
    parts["rp_total"] = wide[LSTAY_TOTAL]
    return parts


def national_rotation(parts: pd.DataFrame) -> dict[str, object]:
    """National (France hors Mayotte) shares per vintage and the 2012→2023 drop."""
    try:
        fr = parts.loc[("FRANCE", NATIONAL_GEO)]
    except KeyError as exc:
        raise MobiliteError("national FRANCE/F rows missing from the L_STAY cut") from exc
    for year in VINTAGES:
        if year not in fr.index:
            raise MobiliteError(f"national vintage {year} missing from the L_STAY cut")
    first, last = VINTAGES[0], VINTAGES[-1]
    delta_lt2 = float(fr.loc[last, "moins_2_ans_pct"] - fr.loc[first, "moins_2_ans_pct"])
    rp_last = float(fr.loc[last, "rp_total"])
    return {
        "parts_par_millesime": {
            str(year): {
                "moins_2_ans_pct": round(float(fr.loc[year, "moins_2_ans_pct"]), 2),
                "moins_5_ans_pct": round(float(fr.loc[year, "moins_5_ans_pct"]), 2),
                "rp_total": round(float(fr.loc[year, "rp_total"])),
            }
            for year in VINTAGES
        },
        "delta_moins_2_ans_pts": round(delta_lt2, 2),
        "delta_moins_5_ans_pts": round(
            float(fr.loc[last, "moins_5_ans_pct"] - fr.loc[first, "moins_5_ans_pct"]), 2
        ),
        # Descriptive order of magnitude, NOT an annual flow: the recent
        # move-ins "missing" from the 2023 stock had rotation stayed at
        # its 2012 share.
        "emmenagements_recents_manquants": round(-delta_lt2 / 100 * rp_last),
    }


def rotation_by_ze(parts: pd.DataFrame) -> pd.DataFrame:
    """Per-ZE recent-mover level (last vintage) and 2012→2023 drop."""
    try:
        ze = parts.loc["ZE2020"]
    except KeyError as exc:
        raise MobiliteError("ZE2020 rows missing from the L_STAY cut") from exc
    first, last = VINTAGES[0], VINTAGES[-1]
    p_first = ze.xs(first, level="annee")
    p_last = ze.xs(last, level="annee")
    frame = pd.DataFrame(
        {
            "part_recents_debut_pct": p_first["moins_2_ans_pct"],
            "part_recents_pct": p_last["moins_2_ans_pct"],
            "part_moins_5_ans_pct": p_last["moins_5_ans_pct"],
            "rp_total": p_last["rp_total"],
        }
    )
    frame = frame.dropna(subset=["part_recents_pct"])
    if frame.empty:
        raise MobiliteError("no ZE with a recent-mover share")
    frame["delta_pts"] = frame["part_recents_pct"] - frame["part_recents_debut_pct"]
    # Relative view added by the 2026-08-09 review (SE-1): a drop in
    # points is mechanically larger where the initial level is higher.
    frame["delta_rel_pct"] = frame["delta_pts"] / frame["part_recents_debut_pct"] * 100
    return frame


def tension_contrast(
    frame: pd.DataFrame, column: str, tendue: pd.Series, suffix: str
) -> dict[str, object]:
    """Median contrast of `column` between tense and other ZE.

    2026-08-09 review (HD-2): an unknown tension status stays unknown —
    the ZE is excluded from BOTH medians and its count is published,
    instead of being silently filled as « autres ».
    """
    aligned = tendue.reindex(frame.index)
    known = aligned.notna()
    tendues = known & aligned.fillna(False).astype(bool)
    autres = known & ~aligned.fillna(True).astype(bool)

    def median_or_none(mask: pd.Series) -> float | None:
        value = frame.loc[mask, column].median()
        return None if pd.isna(value) else round(float(value), 2)

    return {
        f"tendues_{suffix}": median_or_none(tendues),
        f"autres_{suffix}": median_or_none(autres),
        "n_tendues": int(tendues.sum()),
        "n_tension_inconnue": int((~known).sum()),
        "mann_whitney_p": stats.mann_whitney_p(
            frame.loc[tendues, column], frame.loc[autres, column]
        ),
    }


def build_summary(
    ze_frame: pd.DataFrame,
    national: dict[str, object],
    tendue: pd.Series,
    structural_rate_pct: pd.Series,
    indice_cout_pct: pd.Series,
    ze_names: pd.Series,
    tendue_variants: dict[str, pd.Series] | None = None,
) -> dict[str, object]:
    """Assemble the R-11 payload: national slowdown, ZE distribution, crosses."""
    frame = (
        ze_frame.join(tendue.rename("tendue"), how="left")
        .join(structural_rate_pct.rename("taux_structurelle_pct"), how="left")
        .join(indice_cout_pct.rename("indice_cout_pct"), how="left")
        .join(ze_names.rename("ze_name"), how="left")
    )

    def entry(row: pd.Series) -> dict[str, object]:
        return {
            "ze": str(row.name),
            "name": row["ze_name"] if pd.notna(row["ze_name"]) else None,
            "part_recents_pct": round(float(row["part_recents_pct"]), 2),
            "delta_pts": round(float(row["delta_pts"]), 2),
        }

    def ranked(by: str, ascending: bool) -> pd.DataFrame:
        return frame.sort_values([by, "ze_name"], ascending=[ascending, True], kind="stable")

    en_baisse = frame["delta_pts"] < 0
    quantiles = frame["part_recents_pct"].quantile([0.25, 0.5, 0.75])
    return {
        "millesimes": list(VINTAGES),
        "national": national,
        "n_ze": len(frame),
        "distribution_part_recents_pct": {
            "min": round(float(frame["part_recents_pct"].min()), 2),
            "q25": round(float(quantiles.loc[0.25]), 2),
            "mediane": round(float(quantiles.loc[0.5]), 2),
            "q75": round(float(quantiles.loc[0.75]), 2),
            "max": round(float(frame["part_recents_pct"].max()), 2),
        },
        "n_ze_en_baisse": int(en_baisse.sum()),
        "rotation_la_plus_faible": [
            entry(r) for _, r in ranked("part_recents_pct", True).head(8).iterrows()
        ],
        "rotation_la_plus_forte": [
            entry(r) for _, r in ranked("part_recents_pct", False).head(8).iterrows()
        ],
        "plus_fortes_baisses": [entry(r) for _, r in ranked("delta_pts", True).head(8).iterrows()],
        "ze_en_hausse": [
            entry(r) for _, r in ranked("delta_pts", False).iterrows() if r["delta_pts"] > 0
        ],
        "mediane_delta_par_tension": tension_contrast(frame, "delta_pts", frame["tendue"], "pts"),
        # The three views of the drop demanded by the 2026-08-09 review
        # (SE-1): points, relative, and cost gradient at controlled
        # initial level — interpretations may only lean on what is
        # invariant across the three.
        "mediane_delta_rel_par_tension": tension_contrast(
            frame, "delta_rel_pct", frame["tendue"], "rel_pct"
        ),
        "sensibilite_h08": {
            label: tension_contrast(frame, "delta_pts", variant, "pts")
            for label, variant in (tendue_variants or {}).items()
        },
        "spearman_niveau_vs_vacance": stats.spearman_by_perimeter(
            frame, "part_recents_pct", "taux_structurelle_pct"
        ),
        "spearman_niveau_vs_cout": stats.spearman_by_perimeter(
            frame, "part_recents_pct", "indice_cout_pct"
        ),
        "spearman_delta_vs_cout": stats.spearman_by_perimeter(
            frame, "delta_pts", "indice_cout_pct"
        ),
        "spearman_delta_vs_vacance": stats.spearman_by_perimeter(
            frame, "delta_pts", "taux_structurelle_pct"
        ),
        "spearman_delta_vs_niveau_2012": stats.spearman_by_perimeter(
            frame, "delta_pts", "part_recents_debut_pct"
        ),
        "spearman_delta_rel_vs_cout": stats.spearman_by_perimeter(
            frame, "delta_rel_pct", "indice_cout_pct"
        ),
        "partial_delta_vs_cout_controle_niveau_2012": stats.partial_spearman_by_perimeter(
            frame, "delta_pts", "indice_cout_pct", "part_recents_debut_pct"
        ),
        "partial_delta_rel_vs_cout_controle_niveau_2012": stats.partial_spearman_by_perimeter(
            frame, "delta_rel_pct", "indice_cout_pct", "part_recents_debut_pct"
        ),
    }
