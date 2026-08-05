"""Pure transforms for the tension/absolute-shortage cross (stabilized from
notebooks/exploration/08_tension_manque_absolu.py).

Crosses the legal TLV zoning (S-13, D-14), the census total-vacancy stock
(S-11) and the LOVAC structural vacancy (S-05) into the per-ZE tension
frame: available vacancy = total minus structural (out of the market by
construction, D-10), a ZE is market-tense when its available-vacancy rate
is below the H-08 fluidity threshold (C-06 — the initial total-vacancy
test failed the consistency check against the legal zoning and R-06, the
correction is traced in the graph), the absolute mobilisation need is
`t·parc − disponibles` and the local structural stock covers it or not.
No I/O, no clock; reads happen in the shell.
"""

from __future__ import annotations

import pandas as pd

from logement.core.lovac import REFERENCE_MILLESIME, plm_parent
from logement.models import HypothesisRecord


class TensionError(Exception):
    """A tension payload does not have the expected shape."""


TLV_CODE_COL = "CODGEO25"
TLV_ZONING_COL = "Zonage TLV post décret 22/12/2025"
TLV_TENSE_CATEGORIES = ("1. Zone tendue", "2. Zone touristique et tendue")
TLV_MAJORITY_THRESHOLD_PCT = 50.0


def parse_tlv(raw: pd.DataFrame) -> pd.DataFrame:
    """Parse the TLV zoning list: commune code + latest zoning category.

    PLM parents are already communes in the source; duplicated codes keep
    their first row.
    """
    for col in (TLV_CODE_COL, TLV_ZONING_COL):
        if col not in raw.columns:
            raise TensionError(f"missing TLV column {col}")
    out = pd.DataFrame(
        {
            "code": raw[TLV_CODE_COL].astype("string").str.strip().map(plm_parent),
            "zonage": raw[TLV_ZONING_COL].astype("string").str.strip(),
        }
    ).dropna()
    return out.drop_duplicates(subset="code", keep="first")


def tension_by_ze(
    census: pd.DataFrame,
    tlv: pd.DataFrame,
    lovac_communes: pd.DataFrame,
    commune_ze: pd.DataFrame,
    threshold_pct: float,
) -> pd.DataFrame:
    """Cross census stock, TLV zoning and structural vacancy into the ZE frame.

    Available vacancy is census total vacancy minus LOVAC structural
    vacancy (mixed perimeters, L-06/L-12); the mobilisation need at the
    `threshold_pct` fluidity target is `t·parc − disponibles` (mobilising
    a structural vacant adds one available dwelling without growing the
    stock). min_count keeps all-secret LOVAC groups missing, never zero.
    """
    if threshold_pct <= 0 or threshold_pct >= 100:
        raise TensionError(f"implausible fluidity threshold {threshold_pct}")
    for col in ("code", "P22_LOG", "P22_LOGVAC"):
        if col not in census.columns:
            raise TensionError(f"missing census column {col}")
    ref = REFERENCE_MILLESIME
    vac_col = f"pp_vacant_plus_2ans_{ref}"
    if vac_col not in lovac_communes.columns:
        raise TensionError(f"missing LOVAC column {vac_col}")

    com = (
        census.rename(columns={"P22_LOG": "parc", "P22_LOGVAC": "vacants"})[
            ["code", "parc", "vacants"]
        ]
        .merge(tlv, on="code", how="left")
        .merge(commune_ze, on="code", how="left")
        .dropna(subset=["ze", "parc"])
    )
    com["zonage"] = com["zonage"].fillna("3. Non tendue")
    frame = com.groupby("ze")[["parc", "vacants"]].sum()
    for cat, col in zip(TLV_TENSE_CATEGORIES, ("parc_tlv1", "parc_tlv2"), strict=True):
        frame[col] = com[com["zonage"] == cat].groupby("ze")["parc"].sum()
    frame[["parc_tlv1", "parc_tlv2"]] = frame[["parc_tlv1", "parc_tlv2"]].fillna(0)
    frame["part_tlv_pct"] = (frame["parc_tlv1"] + frame["parc_tlv2"]) / frame["parc"] * 100

    lovac = lovac_communes.copy()
    lovac["code"] = lovac["code"].map(plm_parent)
    structural = (
        lovac.merge(commune_ze, on="code", how="left")
        .dropna(subset=["ze"])
        .groupby("ze")[[vac_col]]
        .sum(min_count=1)
        .rename(columns={vac_col: "structurelle"})
    )
    frame = frame.join(structural, how="inner")
    if frame.empty:
        raise TensionError("no ZE joined between census, TLV and LOVAC")

    threshold = threshold_pct / 100
    frame["taux_vacance_pct"] = frame["vacants"] / frame["parc"] * 100
    frame["vacants_disponibles"] = frame["vacants"] - frame["structurelle"]
    frame["taux_disponible_pct"] = frame["vacants_disponibles"] / frame["parc"] * 100
    frame["tendue"] = frame["taux_disponible_pct"] < threshold_pct
    frame["besoin_mobilisation"] = threshold * frame["parc"] - frame["vacants_disponibles"]
    frame["couverture_gisement"] = frame["structurelle"] / frame["besoin_mobilisation"]
    return frame


def _national_at(frame: pd.DataFrame, threshold_pct: float) -> dict[str, object]:
    """Aggregate the tense-ZE need and local stock at one threshold value."""
    threshold = threshold_pct / 100
    tense = frame[frame["taux_disponible_pct"] < threshold_pct]
    besoin = float((threshold * tense["parc"] - tense["vacants_disponibles"]).sum())
    gisement = float(tense["structurelle"].sum())
    return {
        "seuil_pct": threshold_pct,
        "n_ze_tendues": len(tense),
        "parc_tendues": round(float(tense["parc"].sum())),
        "besoin_logements": round(besoin),
        "gisement_structurel": round(gisement),
        "couverture": round(gisement / besoin, 2) if besoin > 0 else None,
    }


def build_summary(
    tension_ze: pd.DataFrame, ze_names: pd.Series, h08: HypothesisRecord
) -> dict[str, object]:
    """Assemble the R-07 payload: tense ZE, absolute needs, coverage, extremes."""
    frame = tension_ze.join(ze_names.rename("ze_name"), how="left")
    low, high = h08.plausible_range
    tense = frame[frame["tendue"]].copy()
    covered = tense["couverture_gisement"] >= 1
    majority_tlv = frame["part_tlv_pct"] > TLV_MAJORITY_THRESHOLD_PCT

    def entry(row: pd.Series) -> dict[str, object]:
        return {
            "ze": str(row.name),
            "name": row["ze_name"] if pd.notna(row["ze_name"]) else None,
            "parc": round(float(row["parc"])),
            "taux_vacance_pct": round(float(row["taux_vacance_pct"]), 2),
            "taux_disponible_pct": round(float(row["taux_disponible_pct"]), 2),
            "part_tlv_pct": round(float(row["part_tlv_pct"]), 1),
            "structurelle": round(float(row["structurelle"])),
            "besoin_mobilisation": round(float(row["besoin_mobilisation"])),
            "couverture_gisement": round(float(row["couverture_gisement"]), 2),
        }

    def ranked(sub: pd.DataFrame, by: str, ascending: bool, count: int) -> list[dict[str, object]]:
        ordered = sub.sort_values([by, "ze_name"], ascending=[ascending, True], kind="stable")
        return [entry(r) for _, r in ordered.head(count).iterrows()]

    return {
        "reference_millesime": REFERENCE_MILLESIME,
        "hypothesis": {
            "id": h08.id,
            "name": h08.name,
            "central_value_pct": h08.central_value,
            "plausible_range": [low, high],
        },
        "n_ze": len(frame),
        "national": _national_at(frame, h08.central_value),
        "sensibilite_seuil": [
            _national_at(frame, value) for value in (low, h08.central_value, high)
        ],
        "ze_couvertes": {
            "n": int(covered.sum()),
            "sur": len(tense),
            "parc_couvert": round(float(tense.loc[covered, "parc"].sum())),
            "parc_non_couvert": round(float(tense.loc[~covered, "parc"].sum())),
        },
        "croisement_admin_marche": {
            "seuil_majorite_tlv_pct": TLV_MAJORITY_THRESHOLD_PCT,
            "n_majoritaires_tlv": int(majority_tlv.sum()),
            "n_majoritaires_tlv_tendues": int((majority_tlv & frame["tendue"]).sum()),
            "n_majoritaires_tlv_tendues_test_vacance_totale": int(
                (majority_tlv & (frame["taux_vacance_pct"] < h08.central_value)).sum()
            ),
        },
        "artefacts_disponible_negatif": sorted(
            str(idx) for idx in frame.index[frame["vacants_disponibles"] < 0]
        ),
        "top_besoin": ranked(tense, "besoin_mobilisation", ascending=False, count=12),
        "pires_couvertures": ranked(
            tense[tense["besoin_mobilisation"] > 1000],
            "couverture_gisement",
            ascending=True,
            count=8,
        ),
    }
