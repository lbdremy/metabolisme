"""Pure transforms for the building-condition cross (stabilized from
notebooks/exploration/09_etat_bati_vacance.py).

First instruction of the framing hypothesis H-05 (property-level
blockages): crosses the age of the stock (census share of pre-1946
primary residences, S-11), the DOM-only sanitary-discomfort share (the
census bathroom/toilet question is only asked in the DOM — verified:
P22_RP_BDWC sums to zero over the whole métropole), and the F+G share of
ADEME-diagnosed dwellings (S-16, transaction-biased sample) with the
LOVAC structural-vacancy rate per ZE. Territorial correlations, not
dwelling-level causes. No I/O, no clock; reads happen in the shell.
"""

from __future__ import annotations

import pandas as pd

from logement.core import stats
from logement.core.lovac import plm_parent

DOM_ZE_PREFIXES = stats.DOM_ZE_PREFIXES
CENSUS_BATI_COLS = ("P22_RP", "P22_RP_ACHTOT", "P22_RP_ACH1919", "P22_RP_ACH1945", "P22_RP_BDWC")
DPE_LABELS = ("A", "B", "C", "D", "E", "F", "G")


class BatiError(Exception):
    """A building-condition payload does not have the expected shape."""


def parse_census_bati(raw: pd.DataFrame) -> pd.DataFrame:
    """Parse the census age/comfort counts per commune (PLM parents kept first)."""
    for col in ("CODGEO", *CENSUS_BATI_COLS):
        if col not in raw.columns:
            raise BatiError(f"missing census column {col}")
    out = pd.DataFrame({"code": raw["CODGEO"].astype("string").str.strip().map(plm_parent)})
    for col in CENSUS_BATI_COLS:
        out[col] = pd.to_numeric(raw[col], errors="coerce")
    return out.drop_duplicates(subset="code", keep="first")


def bati_by_ze(census_bati: pd.DataFrame, commune_ze: pd.DataFrame) -> pd.DataFrame:
    """Aggregate the census age/comfort counts per ZE and derive the shares.

    The discomfort share is kept for DOM ZE only (prefixes 01-04 — the
    ZE 00xx codes are metropolitan multi-region zones, not DOM); it is
    missing elsewhere because the underlying census question is not asked
    in métropole.
    """
    merged = census_bati.merge(commune_ze, on="code", how="inner")
    if merged.empty:
        raise BatiError("no commune joined between census and membership table")
    frame = merged.groupby("ze")[list(CENSUS_BATI_COLS)].sum()
    frame["part_avant_1946_pct"] = (
        (frame["P22_RP_ACH1919"] + frame["P22_RP_ACH1945"]) / frame["P22_RP_ACHTOT"] * 100
    )
    frame["dom"] = frame.index.astype(str).str.startswith(DOM_ZE_PREFIXES)
    frame["part_inconfort_pct"] = (1 - frame["P22_RP_BDWC"] / frame["P22_RP"]) * 100
    frame.loc[~frame["dom"], "part_inconfort_pct"] = float("nan")
    return frame


def parse_dpe_counts(raw: pd.DataFrame) -> pd.DataFrame:
    """Pivot the frozen ADEME counts extract per commune × energy label (A..G).

    The extract is long-format (code_insee_ban; etiquette_dpe; n_dpe —
    counts aggregated by the acquisition, see shell/acquire.py). Rows
    without a BAN commune code, with an unknown label or a non-numeric
    count are dropped and counted via the returned attrs (definite
    rejects are reported, never silent). PLM arrondissement codes sum
    into their parent commune.
    """
    for col in ("code_insee_ban", "etiquette_dpe", "n_dpe"):
        if col not in raw.columns:
            raise BatiError(f"missing DPE column {col}")
    frame = raw.dropna(subset=["code_insee_ban"]).copy()
    frame["code"] = frame["code_insee_ban"].astype("string").str.strip().map(plm_parent)
    frame["etiquette"] = frame["etiquette_dpe"].astype("string").str.strip()
    frame["n"] = pd.to_numeric(frame["n_dpe"], errors="coerce")
    kept = frame["etiquette"].isin(DPE_LABELS) & frame["n"].notna()
    counts = (
        frame[kept]
        .groupby(["code", "etiquette"])["n"]
        .sum()
        .unstack(fill_value=0)
        .reindex(columns=list(DPE_LABELS), fill_value=0)
    )
    counts.attrs["dropped_rows"] = int(len(raw) - kept.sum())
    return counts


def dpe_by_ze(dpe_counts: pd.DataFrame, commune_ze: pd.DataFrame) -> pd.DataFrame:
    """Aggregate the commune label counts per ZE and derive the F+G share."""
    merged = dpe_counts.reset_index().merge(commune_ze, on="code", how="inner")
    if merged.empty:
        raise BatiError("no commune joined between DPE extract and membership table")
    frame = merged.groupby("ze")[list(DPE_LABELS)].sum()
    frame["n_dpe"] = frame.sum(axis=1)
    frame["part_fg_pct"] = (frame["F"] + frame["G"]) / frame["n_dpe"] * 100
    return frame


def _spearman(frame: pd.DataFrame, a: str, b: str) -> float:
    return float(frame[a].rank().corr(frame[b].rank()))


def build_summary(
    bati_ze: pd.DataFrame,
    dpe_ze: pd.DataFrame,
    vacancy_ze: pd.DataFrame,
    ze_names: pd.Series,
    dpe_dropped_rows: int,
) -> dict[str, object]:
    """Assemble the R-08 payload: age/energy × vacancy correlations, DOM contrast."""
    frame = (
        bati_ze.join(dpe_ze[["n_dpe", "part_fg_pct", "F", "G"]], how="inner")
        .join(vacancy_ze, how="inner")
        .join(ze_names.rename("ze_name"), how="left")
        .dropna(subset=["structural_rate_pct"])
    )
    if frame.empty:
        raise BatiError("no ZE joined between bati, DPE and vacancy frames")
    metro = frame[~frame["dom"]]
    dom = frame[frame["dom"]]
    old_half = frame["part_avant_1946_pct"] > frame["part_avant_1946_pct"].median()

    def entry(row: pd.Series) -> dict[str, object]:
        return {
            "ze": str(row.name),
            "name": row["ze_name"] if pd.notna(row["ze_name"]) else None,
            "part_avant_1946_pct": round(float(row["part_avant_1946_pct"]), 1),
            "part_fg_pct": round(float(row["part_fg_pct"]), 1),
            "n_dpe": round(float(row["n_dpe"])),
            "taux_structurelle_pct": round(float(row["structural_rate_pct"]), 2),
        }

    def ranked(sub: pd.DataFrame, by: str, count: int) -> list[dict[str, object]]:
        ordered = sub.sort_values([by, "ze_name"], ascending=[False, True], kind="stable")
        return [entry(r) for _, r in ordered.head(count).iterrows()]

    return {
        "n_ze": len(frame),
        "n_ze_dom": int(frame["dom"].sum()),
        "n_dpe_total": round(float(frame["n_dpe"].sum())),
        "dpe_dropped_rows": dpe_dropped_rows,
        "part_fg_diagnostiques_pct": round(
            float((frame["F"] + frame["G"]).sum() / frame["n_dpe"].sum() * 100), 1
        ),
        "spearman_age_vs_vacancy": {
            "all": round(_spearman(frame, "part_avant_1946_pct", "structural_rate_pct"), 2),
            "metropole": round(_spearman(metro, "part_avant_1946_pct", "structural_rate_pct"), 2),
            "metropole_ci95": stats.spearman_summary(
                metro, "part_avant_1946_pct", "structural_rate_pct"
            )["ci95"],
        },
        "spearman_fg_vs_vacancy": {
            "all": round(_spearman(frame, "part_fg_pct", "structural_rate_pct"), 2),
            "metropole": round(_spearman(metro, "part_fg_pct", "structural_rate_pct"), 2),
            "metropole_ci95": stats.spearman_summary(metro, "part_fg_pct", "structural_rate_pct")[
                "ci95"
            ],
        },
        "spearman_fg_vs_age": round(_spearman(frame, "part_fg_pct", "part_avant_1946_pct"), 2),
        # Review addition (L-13 direction): where vacancy is high the stock
        # is LESS diagnosed — the F+G share of the diagnosed is plausibly a
        # floor there, and the published levels only describe the
        # in-transaction stock.
        "spearman_couverture_dpe_vs_vacancy_metropole": round(
            _spearman(
                metro.assign(couverture_dpe_pct=metro["n_dpe"] / metro["private_stock"] * 100),
                "couverture_dpe_pct",
                "structural_rate_pct",
            ),
            2,
        ),
        "median_vacancy_rate_pct": {
            "oldest_half": round(float(frame.loc[old_half, "structural_rate_pct"].median()), 1),
            "newest_half": round(float(frame.loc[~old_half, "structural_rate_pct"].median()), 1),
        },
        "dom_contrast": {
            "n": len(dom),
            "median_vacancy_pct": round(float(dom["structural_rate_pct"].median()), 1),
            "median_part_avant_1946_pct": round(float(dom["part_avant_1946_pct"].median()), 1),
            "median_part_inconfort_pct": round(float(dom["part_inconfort_pct"].median()), 1),
            "spearman_inconfort_vs_vacancy": round(
                _spearman(dom, "part_inconfort_pct", "structural_rate_pct"), 2
            ),
        },
        "top_age": ranked(frame, "part_avant_1946_pct", 8),
        "top_fg": ranked(frame, "part_fg_pct", 8),
        "top_vacancy": ranked(frame, "structural_rate_pct", 8),
    }
