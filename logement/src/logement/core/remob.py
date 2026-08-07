"""Pure transforms for the remobilisation-cost estimate (stabilized from
notebooks/exploration/10_cout_remobilisation.py, corrected by the
2026-08-07 adversarial review).

Prices the R-07 detente need: unit cost of a complete performant
renovation per dwelling (H-09 maison / H-10 collectif in 2016 euros,
S-17), mixed by each ZE's house share, at the S-12 average surfaces,
converted to VAT-included 2023 euros with the frozen IPEA index (S-19),
and compared with building the same dwellings new at the 2023 social-
housing production price (S-18). An order of magnitude, not a quote
(C-07/L-14).

Review corrections carried here (each traced in the graph):
- MIXED COST, coherent with R-07's own geography: renovation can only
  price the dwellings that exist locally — per tense ZE the renovated
  count is min(need, local structural stock) and the residual deficit is
  priced at the new-build comparator. The pre-review figure billed the
  whole need at renovation cost, including ~58k dwellings in ZEs that
  R-07 itself shows have no local stock; that naive figure stays
  published, labeled, so the correction is visible.
- H-08 PROPAGATION: the published cost range only covered H-09/H-10 at
  the central need; the need varies by a factor ~4.6 across the H-08
  range, now propagated.
- Heavy-rehabilitation stress test: R-08 shows the stock is the oldest,
  most-degraded segment, and S-17 prices voluntary energy renovations of
  in-use dwellings — a doubled renovation unit cost bounds that bias
  direction (L-14; S-22/S-25 context).

No I/O, no clock; reads happen in the shell.
"""

from __future__ import annotations

import re

import pandas as pd

from logement.models import HypothesisRecord

SURFACE_MAISON_M2 = 114.3  # S-12 (enquête Logement 2020, moyennes)
SURFACE_APPART_M2 = 65.5
TVA_RENOVATION = 1.055  # S-17: « la TVA applicable sur ces travaux est de 5,5% »
IPEA_YEAR_FROM = "2016"  # euros of the S-17 cost study
IPEA_YEAR_TO = "2023"  # euros of the S-18 comparator
PRIX_REVIENT_NEUF_EUR_2023 = 169_200.0  # S-18, logement social neuf, 2023
FACTEUR_REHABILITATION_LOURDE = 2.0  # stress test, L-14 (direction set by R-08)


class RemobError(Exception):
    """A remobilisation payload does not have the expected shape."""


def parse_ipea_annual_means(xml_text: str) -> pd.Series:
    """Extract annual means from the frozen IPEA SDMX response (S-19)."""
    obs = re.findall(r'TIME_PERIOD="(\d{4})-Q[1-4]" OBS_VALUE="([\d.]+)"', xml_text)
    if not obs:
        raise RemobError("no quarterly observations found in the IPEA XML")
    frame = pd.DataFrame(obs, columns=["annee", "valeur"]).astype({"valeur": float})
    return frame.groupby("annee")["valeur"].mean()


def ipea_factor(annual_means: pd.Series) -> float:
    """Actualisation factor from the S-17 cost vintage to the S-18 one."""
    for year in (IPEA_YEAR_FROM, IPEA_YEAR_TO):
        if year not in annual_means.index:
            raise RemobError(f"IPEA year {year} missing from the frozen series")
    return float(annual_means[IPEA_YEAR_TO] / annual_means[IPEA_YEAR_FROM])


def unit_cost_eur(
    part_maison: pd.Series, cost_maison_m2: float, cost_collectif_m2: float, factor: float
) -> pd.Series:
    """Per-dwelling renovation cost, VAT included, actualised (C-07 model)."""
    ht_2016 = (
        part_maison * cost_maison_m2 * SURFACE_MAISON_M2
        + (1 - part_maison) * cost_collectif_m2 * SURFACE_APPART_M2
    )
    return ht_2016 * TVA_RENOVATION * factor


def _join_mix(tense: pd.DataFrame, part_maison: pd.Series, ze_names: pd.Series) -> pd.DataFrame:
    """Join a tense-ZE frame with the house-share mix and the ZE names.

    A tense ZE whose structural stock is unknown (all-secret LOVAC) keeps
    its need but renovates zero dwellings — the deficit leg prices it at
    the new-build comparator (conservative, and flagged in the payload).
    """
    frame = (
        tense.join(part_maison.rename("part_maison"), how="inner")
        .join(ze_names.rename("ze_name"), how="left")
        .dropna(subset=["part_maison"])
    )
    if frame.empty:
        raise RemobError("no tense ZE joined with the house-share mix")
    stock = frame["structurelle"].fillna(0)
    return frame.assign(
        renovables=frame["besoin_mobilisation"].clip(upper=stock),
        deficit_neuf=(frame["besoin_mobilisation"] - stock).clip(lower=0),
    )


def _mixed_cost_eur(
    frame: pd.DataFrame, cu: pd.Series, factor_renovation: float = 1.0
) -> dict[str, float]:
    """Price a tense frame: renovation capped by the local stock + deficit new."""
    renovation = float((frame["renovables"] * cu * factor_renovation).sum())
    neuf = float((frame["deficit_neuf"] * PRIX_REVIENT_NEUF_EUR_2023).sum())
    return {"renovation": renovation, "neuf": neuf, "total": renovation + neuf}


def build_summary(
    tense_by_seuil: dict[str, pd.DataFrame],
    part_maison: pd.Series,
    ze_names: pd.Series,
    h08: HypothesisRecord,
    h09: HypothesisRecord,
    h10: HypothesisRecord,
    h12: HypothesisRecord,
    annual_means: pd.Series,
) -> dict[str, object]:
    """Assemble the R-09 payload: mixed costs, comparator, sensitivities, top ZE.

    `tense_by_seuil` maps the H-08 labels (bas/central/haut) to the tense
    subframes of the tension chain built at those thresholds (existence
    rate H-12 already applied upstream by tension_by_ze).
    """
    for label in ("bas", "central", "haut"):
        if label not in tense_by_seuil:
            raise RemobError(f"missing H-08 tense frame {label}")
    frame = _join_mix(tense_by_seuil["central"], part_maison, ze_names)
    factor = ipea_factor(annual_means)
    besoin_total = float(frame["besoin_mobilisation"].sum())
    gisement_total = float(frame["structurelle"].sum())
    renovables_total = float(frame["renovables"].sum())
    deficit_total = float(frame["deficit_neuf"].sum())

    variants: dict[str, dict[str, float]] = {}
    detente_mixte: dict[str, float] = {}
    detente_renovation_seule: dict[str, float] = {}
    for label, maison, collectif in (
        ("bas", h09.plausible_range[0], h10.plausible_range[0]),
        ("central", h09.central_value, h10.central_value),
        ("haut", h09.plausible_range[1], h10.plausible_range[1]),
    ):
        cu = unit_cost_eur(frame["part_maison"], maison, collectif, factor)
        mixed = _mixed_cost_eur(frame, cu)
        detente_mixte[label] = mixed["total"]
        detente_renovation_seule[label] = float((frame["besoin_mobilisation"] * cu).sum())
        variants[label] = {
            "cout_unitaire_renovation_moyen_eur": round(
                float((cu * frame["renovables"]).sum() / renovables_total)
            ),
            "cout_detente_mixte_mdeur": round(mixed["total"] / 1e9, 1),
            "dont_renovation_mdeur": round(mixed["renovation"] / 1e9, 1),
            "dont_deficit_neuf_mdeur": round(mixed["neuf"] / 1e9, 1),
            "cout_detente_renovation_seule_mdeur": round(detente_renovation_seule[label] / 1e9, 1),
            "cout_gisement_mdeur": round(float((frame["structurelle"] * cu).sum()) / 1e9, 1),
        }

    cu_central = unit_cost_eur(frame["part_maison"], h09.central_value, h10.central_value, factor)
    cout_neuf = besoin_total * PRIX_REVIENT_NEUF_EUR_2023
    lourde = _mixed_cost_eur(frame, cu_central, FACTEUR_REHABILITATION_LOURDE)
    frame = frame.assign(
        cout_detente_eur=frame["renovables"] * cu_central
        + frame["deficit_neuf"] * PRIX_REVIENT_NEUF_EUR_2023
    )

    seuils: list[dict[str, object]] = []
    low8, high8 = h08.plausible_range
    for label, seuil in (("bas", low8), ("central", h08.central_value), ("haut", high8)):
        tense_frame = _join_mix(tense_by_seuil[label], part_maison, ze_names)
        cu = unit_cost_eur(tense_frame["part_maison"], h09.central_value, h10.central_value, factor)
        mixed = _mixed_cost_eur(tense_frame, cu)
        besoin = float(tense_frame["besoin_mobilisation"].sum())
        seuils.append(
            {
                "seuil_pct": seuil,
                "n_ze_tendues": len(tense_frame),
                "besoin_total": round(besoin),
                "cout_detente_mixte_mdeur": round(mixed["total"] / 1e9, 1),
                "ratio_neuf_sur_detente": round(
                    besoin * PRIX_REVIENT_NEUF_EUR_2023 / mixed["total"], 1
                )
                if mixed["total"] > 0
                else None,
            }
        )

    def entry(row: pd.Series) -> dict[str, object]:
        return {
            "ze": str(row.name),
            "name": row["ze_name"] if pd.notna(row["ze_name"]) else None,
            "besoin_mobilisation": round(float(row["besoin_mobilisation"])),
            "renovables": round(float(row["renovables"])),
            "deficit_neuf": round(float(row["deficit_neuf"])),
            "part_maison_pct": round(float(row["part_maison"]) * 100, 1),
            "cout_detente_meur": round(float(row["cout_detente_eur"]) / 1e6, 1),
            "cout_neuf_meur": round(
                float(row["besoin_mobilisation"]) * PRIX_REVIENT_NEUF_EUR_2023 / 1e6, 1
            ),
        }

    ranked = frame.sort_values(
        ["cout_detente_eur", "ze_name"], ascending=[False, True], kind="stable"
    )
    return {
        "modele": {
            "surface_maison_m2": SURFACE_MAISON_M2,
            "surface_appart_m2": SURFACE_APPART_M2,
            "tva": TVA_RENOVATION,
            "prix_revient_neuf_eur_2023": PRIX_REVIENT_NEUF_EUR_2023,
            "regle_mixte": "renovation = min(besoin, gisement local) ; deficit au prix neuf",
        },
        "hypotheses": {
            "h09_maison_eur_ht_m2": {
                "central": h09.central_value,
                "plausible_range": list(h09.plausible_range),
            },
            "h10_collectif_eur_ht_m2": {
                "central": h10.central_value,
                "plausible_range": list(h10.plausible_range),
            },
            "h12_existence_rate": {
                "central": h12.central_value,
                "plausible_range": list(h12.plausible_range),
            },
        },
        "ipea": {
            "moyenne_2016": round(float(annual_means[IPEA_YEAR_FROM]), 2),
            "moyenne_2023": round(float(annual_means[IPEA_YEAR_TO]), 2),
            "facteur": round(factor, 3),
        },
        "n_ze_tendues": len(frame),
        "besoin_total": round(besoin_total),
        "gisement_total": round(gisement_total),
        "logements": {
            "renovables": round(renovables_total),
            "deficit_neuf": round(deficit_total),
            "n_ze_structurelle_inconnue": int(frame["structurelle"].isna().sum()),
        },
        "couts": variants,
        "comparateur_neuf": {
            "cout_neuf_mdeur": round(cout_neuf / 1e9, 1),
            "ratio_neuf_sur_detente_mixte": {
                label: round(cout_neuf / raw, 1) for label, raw in detente_mixte.items()
            },
            "ratio_neuf_sur_renovation_seule": {
                label: round(cout_neuf / raw, 1) for label, raw in detente_renovation_seule.items()
            },
        },
        "variante_rehabilitation_lourde": {
            "facteur_renovation": FACTEUR_REHABILITATION_LOURDE,
            "cout_detente_mixte_mdeur": round(lourde["total"] / 1e9, 1),
            "ratio_neuf_sur_detente": round(cout_neuf / lourde["total"], 1)
            if lourde["total"] > 0
            else None,
        },
        "sensibilite_seuil_h08": seuils,
        "top_cout_detente": [entry(r) for _, r in ranked.head(10).iterrows()],
    }
