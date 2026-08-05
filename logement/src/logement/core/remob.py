"""Pure transforms for the remobilisation-cost estimate (stabilized from
notebooks/exploration/10_cout_remobilisation.py).

Prices the R-07 detente need: unit cost of a complete performant
renovation per dwelling (H-09 maison / H-10 collectif in 2016 euros,
S-17), mixed by each ZE's house share, at the S-12 average surfaces,
converted to VAT-included 2023 euros with the frozen IPEA index (S-19),
and compared with building the same dwellings new at the 2023 social-
housing production price (S-18). An order of magnitude, not a quote
(C-07/L-14). No I/O, no clock; reads happen in the shell.
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


def build_summary(
    tense: pd.DataFrame,
    part_maison: pd.Series,
    ze_names: pd.Series,
    h09: HypothesisRecord,
    h10: HypothesisRecord,
    annual_means: pd.Series,
) -> dict[str, object]:
    """Assemble the R-09 payload: costs per variant, comparator, top ZE."""
    frame = (
        tense.join(part_maison.rename("part_maison"), how="inner")
        .join(ze_names.rename("ze_name"), how="left")
        .dropna(subset=["part_maison"])
    )
    if frame.empty:
        raise RemobError("no tense ZE joined with the house-share mix")
    factor = ipea_factor(annual_means)
    besoin_total = float(frame["besoin_mobilisation"].sum())
    gisement_total = float(frame["structurelle"].sum())

    variants: dict[str, dict[str, float]] = {}
    detente_raw: dict[str, float] = {}
    for label, maison, collectif in (
        ("bas", h09.plausible_range[0], h10.plausible_range[0]),
        ("central", h09.central_value, h10.central_value),
        ("haut", h09.plausible_range[1], h10.plausible_range[1]),
    ):
        cu = unit_cost_eur(frame["part_maison"], maison, collectif, factor)
        detente_raw[label] = float((frame["besoin_mobilisation"] * cu).sum())
        variants[label] = {
            "cout_unitaire_moyen_pondere_eur": round(
                float((cu * frame["besoin_mobilisation"]).sum() / besoin_total)
            ),
            "cout_detente_mdeur": round(detente_raw[label] / 1e9, 1),
            "cout_gisement_mdeur": round(float((frame["structurelle"] * cu).sum()) / 1e9, 1),
        }

    cu_central = unit_cost_eur(frame["part_maison"], h09.central_value, h10.central_value, factor)
    cout_neuf = besoin_total * PRIX_REVIENT_NEUF_EUR_2023
    frame = frame.assign(cout_detente_eur=frame["besoin_mobilisation"] * cu_central)

    def entry(row: pd.Series) -> dict[str, object]:
        return {
            "ze": str(row.name),
            "name": row["ze_name"] if pd.notna(row["ze_name"]) else None,
            "besoin_mobilisation": round(float(row["besoin_mobilisation"])),
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
        },
        "ipea": {
            "moyenne_2016": round(float(annual_means[IPEA_YEAR_FROM]), 2),
            "moyenne_2023": round(float(annual_means[IPEA_YEAR_TO]), 2),
            "facteur": round(factor, 3),
        },
        "n_ze_tendues": len(frame),
        "besoin_total": round(besoin_total),
        "gisement_total": round(gisement_total),
        "couts": variants,
        "comparateur_neuf": {
            "cout_neuf_mdeur": round(cout_neuf / 1e9, 1),
            "ratio_neuf_sur_remobilisation": {
                label: round(cout_neuf / raw, 1) for label, raw in detente_raw.items()
            },
        },
        "top_cout_detente": [entry(r) for _, r in ranked.head(10).iterrows()],
    }
