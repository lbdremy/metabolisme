"""Pure transforms for the tension/absolute-shortage cross (stabilized from
notebooks/exploration/08_tension_manque_absolu.py, corrected by the
2026-08-07 adversarial review).

Crosses the legal TLV zoning (S-13, D-14), the census total-vacancy stock
(S-11) and the LOVAC structural vacancy (S-05) into the per-ZE tension
frame: available vacancy = total minus structural (out of the market by
construction, D-10), a ZE is market-tense when its available-vacancy rate
is below the H-08 fluidity threshold (C-06 — the initial total-vacancy
test failed the consistency check against the legal zoning and R-06, the
correction is traced in the graph), the absolute mobilisation need is
`t·parc − disponibles` and the local structural stock covers it or not.

Review corrections carried here (each traced in the graph):
- H-12 existence rate: LOVAC over-records vacancy (~25 % false vacants,
  S-22 p. 21); the rate applies BOTH to the usable stock and to the
  subtraction that defines available vacancy — false vacants are not an
  available supply either.  The net effect on coverage is computed, not
  guessed.
- Negative available vacancy (structural > census vacants, mixed
  apparatuses, L-06/L-12) is clipped out of the need instead of
  inflating it; the clipped amount is published.
- The stock of the tense ZEs partly sits in their NON-TLV communes: the
  TLV-restricted variant recomputes the coverage with the stock of the
  legally-tense communes only (infra-ZE localisation objection).
- The fluidity threshold of S-14/S-15 is defined on TOTAL vacancy while
  C-06 tests AVAILABLE vacancy: the recalibrated-basis variant shifts
  the threshold by the national structural rate and republishes the
  national numbers (basis-choice sensitivity).
- LOVAC secrecy (< 11) hides communes whose structural stock is bounded
  by 10 each: the bound on the national coverage is published (the
  masked mass moves coverage DOWN when the stock exceeds the need).

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
# LOVAC secrecy masks counts below 11 (L-05): a masked commune carries at
# most 10 structurally-vacant dwellings.
SECRET_MAX_PER_COMMUNE = 10
# Classification grey band around the fluidity threshold: the available
# vacancy is a construct of two apparatuses (census × LOVAC, L-12) whose
# error visibly reaches percentage points (negative values in Corsica).
GREY_BAND_PCT = 1.0


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
    existence_rate: float = 1.0,
) -> pd.DataFrame:
    """Cross census stock, TLV zoning and structural vacancy into the ZE frame.

    Available vacancy is census total vacancy minus the EFFECTIVE LOVAC
    structural vacancy (`existence_rate` × recorded, H-12 — false vacants
    are neither a usable stock nor an available supply); the mobilisation
    need at the `threshold_pct` fluidity target is `t·parc − disponibles`
    with negative availables clipped to zero (apparatus artefacts must
    not inflate the need). min_count keeps all-secret LOVAC groups
    missing, never zero.
    """
    if threshold_pct <= 0 or threshold_pct >= 100:
        raise TensionError(f"implausible fluidity threshold {threshold_pct}")
    if not 0 < existence_rate <= 1:
        raise TensionError(f"implausible existence rate {existence_rate}")
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
    lovac = (
        lovac.merge(tlv, on="code", how="left")
        .merge(commune_ze, on="code", how="left")
        .dropna(subset=["ze"])
    )
    lovac["zonage"] = lovac["zonage"].fillna("3. Non tendue")
    grouped = lovac.groupby("ze")
    structural = grouped[[vac_col]].sum(min_count=1).rename(columns={vac_col: "structurelle_lovac"})
    structural["n_communes_masquees"] = grouped[vac_col].agg(lambda s: int(s.isna().sum()))
    in_tlv = lovac[lovac["zonage"].isin(TLV_TENSE_CATEGORIES)]
    structural_tlv = (
        in_tlv.groupby("ze")[[vac_col]]
        .sum(min_count=1)
        .rename(columns={vac_col: "structurelle_tlv_lovac"})
    )
    frame = frame.join(structural, how="inner").join(structural_tlv, how="left")
    if frame.empty:
        raise TensionError("no ZE joined between census, TLV and LOVAC")
    # A ZE without any TLV commune has a genuinely zero TLV stock; a ZE
    # whose TLV communes are all masked keeps NaN (unknown keeps).
    no_tlv_parc = (frame["parc_tlv1"] + frame["parc_tlv2"]) == 0
    frame.loc[no_tlv_parc, "structurelle_tlv_lovac"] = frame.loc[
        no_tlv_parc, "structurelle_tlv_lovac"
    ].fillna(0)

    frame["structurelle"] = frame["structurelle_lovac"] * existence_rate
    frame["structurelle_tlv"] = frame["structurelle_tlv_lovac"] * existence_rate

    threshold = threshold_pct / 100
    frame["taux_vacance_pct"] = frame["vacants"] / frame["parc"] * 100
    frame["vacants_disponibles"] = frame["vacants"] - frame["structurelle"]
    frame["taux_disponible_pct"] = frame["vacants_disponibles"] / frame["parc"] * 100
    frame["tendue"] = frame["taux_disponible_pct"] < threshold_pct
    frame["besoin_mobilisation"] = threshold * frame["parc"] - frame["vacants_disponibles"].clip(
        lower=0
    )
    frame["couverture_gisement"] = frame["structurelle"] / frame["besoin_mobilisation"]
    return frame


def _national_at(frame: pd.DataFrame, threshold_pct: float) -> dict[str, object]:
    """Aggregate the tense-ZE need and local stock at one threshold value.

    The need clips negative availables to zero (apparatus artefacts,
    L-12); the unclipped need is published next to it so the correction
    stays visible.
    """
    threshold = threshold_pct / 100
    tense = frame[frame["taux_disponible_pct"] < threshold_pct]
    besoin = float((threshold * tense["parc"] - tense["vacants_disponibles"].clip(lower=0)).sum())
    besoin_brut = float((threshold * tense["parc"] - tense["vacants_disponibles"]).sum())
    gisement = float(tense["structurelle"].sum())
    gisement_tlv = float(tense["structurelle_tlv"].sum())
    return {
        "seuil_pct": threshold_pct,
        "n_ze_tendues": len(tense),
        "parc_tendues": round(float(tense["parc"].sum())),
        "besoin_logements": round(besoin),
        "besoin_sans_ecretage": round(besoin_brut),
        "gisement_structurel": round(gisement),
        "gisement_structurel_communes_tlv": round(gisement_tlv),
        "couverture": round(gisement / besoin, 2) if besoin > 0 else None,
        "couverture_communes_tlv": round(gisement_tlv / besoin, 2) if besoin > 0 else None,
    }


def _existence_grid(
    frames: dict[str, pd.DataFrame], h08: HypothesisRecord, h12: HypothesisRecord
) -> list[dict[str, object]]:
    """Cross the H-08 threshold range with the H-12 existence range.

    The joint sensitivity is the review's central demand: each hypothesis
    was previously published alone, hiding the corner where the coverage
    drops below 1.
    """
    low8, high8 = h08.plausible_range
    low12, high12 = h12.plausible_range
    rates = {"bas": low12, "central": h12.central_value, "haut": high12}
    grid: list[dict[str, object]] = []
    for label, rate in rates.items():
        frame = frames[label]
        for threshold in (low8, h08.central_value, high8):
            national = _national_at(frame, threshold)
            grid.append(
                {
                    "existence_label": label,
                    "existence_rate": rate,
                    "seuil_pct": threshold,
                    "besoin_logements": national["besoin_logements"],
                    "gisement_structurel": national["gisement_structurel"],
                    "couverture": national["couverture"],
                }
            )
    return grid


def _basis_variant(frame: pd.DataFrame, threshold_pct: float) -> dict[str, object]:
    """Recalibrated-basis variant of C-06 (review objection on H-08's basis).

    S-14/S-15 state the fluidity band on TOTAL vacancy; C-06 tests
    AVAILABLE vacancy, a mechanically harsher test. The recalibrated
    threshold subtracts the national effective structural rate from the
    H-08 value, so the available-vacancy test matches the total-vacancy
    band on average. ZEs tense mainly BECAUSE of a record structural rate
    (the circularity flagged in the DOM) are counted and listed.
    """
    national_structural_rate = float(frame["structurelle"].sum() / frame["parc"].sum() * 100)
    recalibrated = threshold_pct - national_structural_rate
    national = _national_at(frame, recalibrated)
    tense = frame[frame["tendue"]]
    by_structural = tense[tense["structurelle"] / tense["parc"] * 100 > national_structural_rate]
    return {
        "taux_structurel_national_pct": round(national_structural_rate, 2),
        "seuil_recalibre_pct": round(recalibrated, 2),
        "national_au_seuil_recalibre": national,
        "tendues_par_structurelle_record": {
            "n": len(by_structural),
            "gisement_structurel": round(float(by_structural["structurelle"].sum())),
            "ze": sorted(str(idx) for idx in by_structural.index),
        },
    }


def _secrecy_bound(
    frame: pd.DataFrame, threshold_pct: float, existence_rate: float
) -> dict[str, object]:
    """Bound the national coverage against LOVAC secrecy (L-05, corrected L-12).

    Each masked commune hides at most SECRET_MAX_PER_COMMUNE structural
    dwellings. Adding the hidden mass raises the stock AND the need by
    the same amount (one more structural vacant removes one available),
    so when the stock exceeds the need the coverage moves DOWN toward 1 —
    the opposite of what the pre-review L-12 asserted.
    """
    threshold = threshold_pct / 100
    tense = frame[frame["taux_disponible_pct"] < threshold_pct]
    hidden = float(tense["n_communes_masquees"].sum()) * SECRET_MAX_PER_COMMUNE * existence_rate
    besoin = float((threshold * tense["parc"] - tense["vacants_disponibles"].clip(lower=0)).sum())
    gisement = float(tense["structurelle"].sum())
    bounded = (gisement + hidden) / (besoin + hidden) if besoin + hidden > 0 else None
    return {
        "n_communes_masquees_tendues": round(float(tense["n_communes_masquees"].sum())),
        "max_structurels_par_commune_masquee": SECRET_MAX_PER_COMMUNE,
        "masse_masquee_max": round(hidden),
        "couverture_borne_masquee": round(bounded, 2) if bounded is not None else None,
    }


def build_summary(
    frames: dict[str, pd.DataFrame],
    ze_names: pd.Series,
    h08: HypothesisRecord,
    h12: HypothesisRecord,
) -> dict[str, object]:
    """Assemble the R-07 payload: tense ZE, absolute needs, coverage, variants.

    `frames` maps the H-12 sensitivity labels (bas/central/haut) to the
    tension frames built at those existence rates; the central frame
    carries every headline number.
    """
    for label in ("bas", "central", "haut"):
        if label not in frames:
            raise TensionError(f"missing existence-rate frame {label}")
    frame = frames["central"].join(ze_names.rename("ze_name"), how="left")
    low, high = h08.plausible_range
    tense = frame[frame["tendue"]].copy()
    covered = tense["couverture_gisement"] >= 1
    majority_tlv = frame["part_tlv_pct"] > TLV_MAJORITY_THRESHOLD_PCT
    tense_deficit = (tense["besoin_mobilisation"] - tense["structurelle"]).clip(lower=0)
    negative = frame["vacants_disponibles"] < 0
    grey = (frame["taux_disponible_pct"] - h08.central_value).abs() < GREY_BAND_PCT

    def entry(row: pd.Series) -> dict[str, object]:
        return {
            "ze": str(row.name),
            "name": row["ze_name"] if pd.notna(row["ze_name"]) else None,
            "parc": round(float(row["parc"])),
            "taux_vacance_pct": round(float(row["taux_vacance_pct"]), 2),
            "taux_disponible_pct": round(float(row["taux_disponible_pct"]), 2),
            "part_tlv_pct": round(float(row["part_tlv_pct"]), 1),
            "structurelle": round(float(row["structurelle"])),
            "structurelle_lovac": round(float(row["structurelle_lovac"])),
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
        "hypothesis_existence": {
            "id": h12.id,
            "name": h12.name,
            "central_value": h12.central_value,
            "plausible_range": list(h12.plausible_range),
        },
        "n_ze": len(frame),
        "national": _national_at(frame, h08.central_value),
        "sensibilite_seuil": [
            _national_at(frame, value) for value in (low, h08.central_value, high)
        ],
        "sensibilite_seuil_x_existence": _existence_grid(frames, h08, h12),
        "variante_assiette": _basis_variant(frame, h08.central_value),
        "borne_secretisation": _secrecy_bound(frame, h08.central_value, h12.central_value),
        "bande_grise": {
            "largeur_pct": GREY_BAND_PCT,
            "n_ze": int(grey.sum()),
            "dont_tendues": int((grey & frame["tendue"]).sum()),
        },
        "ze_couvertes": {
            "n": int(covered.sum()),
            "sur": len(tense),
            "parc_couvert": round(float(tense.loc[covered, "parc"].sum())),
            "parc_non_couvert": round(float(tense.loc[~covered, "parc"].sum())),
            "besoin_couvert": round(float(tense.loc[covered, "besoin_mobilisation"].sum())),
            "besoin_non_couvert": round(float(tense.loc[~covered, "besoin_mobilisation"].sum())),
            "deficit_incompressible": round(float(tense_deficit.sum())),
        },
        "croisement_admin_marche": {
            "seuil_majorite_tlv_pct": TLV_MAJORITY_THRESHOLD_PCT,
            "n_majoritaires_tlv": int(majority_tlv.sum()),
            "n_majoritaires_tlv_tendues": int((majority_tlv & frame["tendue"]).sum()),
            "n_majoritaires_tlv_tendues_test_vacance_totale": int(
                (majority_tlv & (frame["taux_vacance_pct"] < h08.central_value)).sum()
            ),
            "n_tendues_non_majoritaires_tlv": int((frame["tendue"] & ~majority_tlv).sum()),
            "n_tendues_part_tlv_sous_1pct": int(
                (frame["tendue"] & (frame["part_tlv_pct"] < 1.0)).sum()
            ),
        },
        "artefacts_disponible_negatif": sorted(str(idx) for idx in frame.index[negative]),
        "besoin_artefacts_ecrete": round(
            float((-frame.loc[negative & frame["tendue"], "vacants_disponibles"]).sum())
        ),
        "top_besoin": ranked(tense, "besoin_mobilisation", ascending=False, count=12),
        "pires_couvertures": ranked(
            tense[tense["besoin_mobilisation"] > 1000],
            "couverture_gisement",
            ascending=True,
            count=8,
        ),
    }
