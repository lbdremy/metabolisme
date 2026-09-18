"""Pure transforms for the institutional-proposal scenarios (session 7,
2026-09-18 — INTRO logement §16 scenarios, method INTRO step 13;
reworked by the 2026-09-18 adversarial review).

The diagnostic arc left three quantified constraints (I-07/I-09/I-10) and
one institutional parameter (R-14: ~83 % of the purchase toll is fiscal).
This module prices the MECHANISMS that could answer them, on the same
frozen inputs, so the proposal compares several designs instead of
defending one (DEC-03):

- M-A  the existing incentive channel at its documented exit rate
       (H-14, S-22 — a majorant: the rate is per CONTACTED owner);
- M-B  a collective operator that ACQUIRES the local durable-vacant
       stock at market value (H-15, D-22, plus the re-employment
       indemnity H-20), renovates it (R-09 unit costs) and builds new
       where the stock is missing (S-18), financed at the social-housing
       loan terms (H-16/H-17) with the sector's operating costs per
       dwelling (H-18) — the output is a per-ZE EQUILIBRIUM RENT (D-23)
       compared with the local market and social rents;
- M-C  the same operator WITHOUT acquisition — bail à réhabilitation
       (D-21, S-46): works only, amortised over the lease (H-19), TFPB
       exempt, volume conditional on owner consent (grid, DEC-09);
- M-D  shifting the DEPARTMENTAL part of the transaction toll (DMTO,
       D-19) to a yearly holding charge over the dwelling stock of the
       same perimeter (S-47, C-14) — a redistribution between mobile
       and immobile households, with the causal evidence on volumes
       (S-43) kept out of the arithmetic.

Units, after the review (ST-1/SE-1/HD-1): every cost is carried PER
SQUARE METRE (DVF median price/m², renovation €/m², S-18 price/m² of
surface utile) and converted to dwellings with the surface of the
segment (C-07 mix for the vacant stock, S-18 surface for the new
build) — never a per-dwelling price divided by another segment's
surface. Descriptive arithmetic on published sources; no behavioural
model. No I/O, no clock — reads happen in the shell.
"""

from __future__ import annotations

from typing import cast

import pandas as pd

from logement.core import remob, transaction
from logement.core.lovac import plm_parent
from logement.models import HypothesisRecord

# S-18 (Éclairages n° 33): 169 200 € per new social dwelling in 2023 at
# 2 550 €/m² of surface utile — the implicit surface (~66 m², « autour de
# 66 m² de surface utile par logement », S-18) is DERIVED, never typed.
PRIX_REVIENT_NEUF_M2_EUR_2023 = 2_550.0
SURFACE_NEUF_M2 = remob.PRIX_REVIENT_NEUF_EUR_2023 / PRIX_REVIENT_NEUF_M2_EUR_2023
# TFPB per dwelling 2023 (S-40, p. 24: 559 €) — removed from the H-18
# charges for a TFPB-exempt operator (bail à réhabilitation, S-46).
TFPB_EUR_PER_DWELLING_2023 = 559.0
# TLV yield 2023 (S-22, p. 36: « 271 M€ en 2023 pour la TLV »).
TLV_YIELD_2023_EUR = 271e6
# Departmental DMTO product on the OFGL constant perimeter (hors Rhône,
# Martinique, Guyane, Corse et Paris): 2025 central (S-47, p. 47:
# « 11,9 Md€ » — first vintage at the 5.00 % rate, ST-6) and the 2024
# low point kept as sensitivity (S-39, p. 4: « 9,9 Md€ »).
DMTO_PRODUCT_EUR = {"2025": 11.9e9, "2024": 9.9e9}
DMTO_CENTRAL_VINTAGE = "2025"
# Departments outside the OFGL constant perimeter (S-39/S-47, champ).
DMTO_PERIMETER_EXCLUDED_DEPARTEMENTS = ("75", "69", "2A", "2B", "972", "973")
# A ZE whose stock lies less than this share inside the perimeter is
# published but kept out of the M-D quantiles (ST-3).
PERIMETER_SHARE_FLOOR = 0.5
# Descriptive grids (not hypotheses — no frozen source elects a central
# value; same status as R-14's HOLDING_YEARS_GRID).
HORIZON_YEARS_GRID = (5, 10, 20)
CONSENT_SHARE_GRID = (0.10, 0.25, 0.50, 1.00)
PROGRAMME_YEARS_GRID = (5, 10, 20)
DISCOUNT_GRID = (0.5, 0.75, 1.0)

RPLS_RENT_COLUMNS = ("DEPCOM_ARM", "nb_ls", "loymoy")


class InstitutionError(Exception):
    """A scenario payload does not have the expected shape."""


# ------------------------------------------------------------------ finance


def annuity_factor(rate_pct: float, years: float) -> float:
    """Constant-annuity factor: yearly payment per euro borrowed."""
    if years <= 0:
        raise InstitutionError(f"non-positive amortisation {years}")
    if rate_pct < 0:
        raise InstitutionError(f"negative rate {rate_pct}")
    r = rate_pct / 100
    denominator = 1 - (1 + r) ** (-years)
    if denominator <= 0:  # r == 0, or so small that (1+r)^-n rounds to 1
        return 1 / years
    return r / denominator


def equilibrium_rent_m2(
    investment_m2_eur: float, factor: float, charges_eur_per_dwelling: float, surface_m2: float
) -> float:
    """Monthly net rent per m² covering the annuity and the fixed charges (D-23)."""
    if surface_m2 <= 0:
        raise InstitutionError(f"non-positive surface {surface_m2}")
    if charges_eur_per_dwelling < 0:
        raise InstitutionError(f"negative charges {charges_eur_per_dwelling}")
    return (investment_m2_eur * factor + charges_eur_per_dwelling / surface_m2) / 12


def weighted_median(values: pd.Series, weights: pd.Series) -> float | None:
    """Median of `values` weighted by `weights` (None when nothing to weigh)."""
    frame = pd.DataFrame({"v": values, "w": weights}).dropna()
    frame = frame[frame["w"] > 0].sort_values("v", kind="stable")
    if frame.empty:
        return None
    cumulative = frame["w"].cumsum()
    return float(frame.loc[cumulative >= cumulative.iloc[-1] / 2, "v"].iloc[0])


# ---------------------------------------------------------------- RPLS rents


def parse_rpls_rents(raw: pd.DataFrame) -> pd.DataFrame:
    """Parse the S-28 COMMUNE sheet down to stock + mean rent (€/m²/month)."""
    for col in RPLS_RENT_COLUMNS:
        if col not in raw.columns:
            raise InstitutionError(f"missing RPLS column {col}")
    out = pd.DataFrame({"code": raw["DEPCOM_ARM"].astype("string").str.strip().map(plm_parent)})
    out["nb_ls"] = pd.to_numeric(raw["nb_ls"], errors="coerce")
    out["loymoy"] = pd.to_numeric(raw["loymoy"], errors="coerce")
    out = out.dropna(subset=["code"])
    if out.empty:
        raise InstitutionError("no commune row in the RPLS sheet")
    return out


def social_rent_by_ze(rents: pd.DataFrame, commune_ze: pd.DataFrame) -> pd.Series:
    """Stock-weighted mean social rent by ZE (convention C-09; NA-safe)."""
    merged = rents.merge(commune_ze, on="code", how="inner").dropna(subset=["loymoy", "nb_ls"])
    if merged.empty:
        raise InstitutionError("no commune joined between RPLS rents and membership")
    merged = merged[merged["nb_ls"] > 0]
    weighted = (merged["loymoy"] * merged["nb_ls"]).groupby(merged["ze"]).sum(min_count=1)
    weights = merged.groupby("ze")["nb_ls"].sum(min_count=1)
    return (weighted / weights).rename("loyer_social_m2")


# --------------------------------------------------------------- M-A reference


def incentive_scenario(detente: pd.DataFrame, h14: HypothesisRecord) -> dict[str, object]:
    """Count the exits from vacancy the incentive channel would produce, vs the need.

    Exits are linear in time, capped per ZE by BOTH the local stock and
    the local need (HD-18): a ZE whose stock exceeds its need cannot
    contribute more than its need to the national coverage.
    """
    besoin = detente["besoin_mobilisation"]
    gisement = detente["structurelle"].fillna(0)
    besoin_total = float(besoin.sum())
    if besoin_total <= 0:
        raise InstitutionError("non-positive detente need")
    grid: list[dict[str, object]] = []
    for label, rate in (
        ("bas", h14.plausible_range[0]),
        ("central", h14.central_value),
        ("haut", h14.plausible_range[1]),
    ):
        for years in HORIZON_YEARS_GRID:
            share = min(1.0, rate / 100 * years)
            sorties = float((gisement * share).clip(upper=besoin).sum())
            grid.append(
                {
                    "taux": label,
                    "taux_pct_an": rate,
                    "horizon_ans": years,
                    "sorties": round(sorties),
                    "part_gisement_pct": round(share * 100, 1),
                    "couverture_besoin": round(sorties / besoin_total, 3),
                }
            )
    central_10 = next(g for g in grid if g["taux"] == "central" and g["horizon_ans"] == 10)
    return {
        "hypothese": {
            "id": h14.id,
            "central_pct_an": h14.central_value,
            "plausible_range": list(h14.plausible_range),
            "assiette": (
                "taux par propriétaire CONTACTÉ (S-22) appliqué au gisement entier : majorant"
            ),
        },
        "gisement_effectif": round(float(gisement.sum())),
        "besoin": round(besoin_total),
        "plafond": "sorties d'une ZE ≤ min(gisement, besoin) de la ZE",
        "grille": grid,
        "central_10_ans": central_10,
        "rendement_tlv_2023_meur": round(TLV_YIELD_2023_EUR / 1e6),
    }


# ------------------------------------------------------------ M-B operator


def operator_frame(
    detente: pd.DataFrame,
    renovation_m2: pd.Series,
    prix_m2: pd.Series,
    loyer_marche_m2: pd.Series,
    loyer_social_m2: pd.Series,
    discount: float,
    reemployment_pct: float,
    rate_pct: float,
    years: float,
    charges_eur: float,
) -> pd.DataFrame:
    """Per-tense-ZE costs, annuities and equilibrium rents of the operator.

    Everything per m² (ST-1): renovated segment = `discount` × DVF
    median price/m² × (1 + re-employment indemnity) + renovation €/m²,
    at the C-07 mixed surface of the ZE; new segment = S-18 price/m² at
    the S-18 surface. Charges are fixed per dwelling (H-18) and spread
    over the segment's surface (D-23).
    """
    if not 0 < discount <= 1:
        raise InstitutionError(f"implausible discount factor {discount}")
    if reemployment_pct < 0:
        raise InstitutionError(f"negative re-employment indemnity {reemployment_pct}")
    frame = (
        detente.join(renovation_m2.rename("renovation_m2"), how="inner")
        .join(prix_m2.rename("prix_m2"), how="inner")
        .join(loyer_marche_m2.rename("loyer_marche_m2"), how="left")
        .join(loyer_social_m2.rename("loyer_social_m2"), how="left")
    )
    if frame.empty:
        raise InstitutionError("no tense ZE joined with prices and renovation costs")
    af = annuity_factor(rate_pct, years)
    frame["renovables"] = frame["renovables"].fillna(0)
    frame["deficit_neuf"] = frame["deficit_neuf"].fillna(0)
    frame["surface_m2"] = (
        frame["part_maison"] * remob.SURFACE_MAISON_M2
        + (1 - frame["part_maison"]) * remob.SURFACE_APPART_M2
    )
    frame["acquisition_m2"] = frame["prix_m2"] * discount * (1 + reemployment_pct / 100)
    frame["cout_renove_m2"] = frame["acquisition_m2"] + frame["renovation_m2"]
    frame["prix_acquisition"] = frame["acquisition_m2"] * frame["surface_m2"]
    frame["cout_unitaire_renove"] = frame["cout_renove_m2"] * frame["surface_m2"]
    frame["cout_acquisition"] = frame["renovables"] * frame["prix_acquisition"]
    frame["cout_renovation"] = frame["renovables"] * frame["renovation_m2"] * frame["surface_m2"]
    frame["cout_neuf"] = frame["deficit_neuf"] * remob.PRIX_REVIENT_NEUF_EUR_2023
    frame["investissement"] = (
        frame["cout_acquisition"] + frame["cout_renovation"] + frame["cout_neuf"]
    )
    frame["annuite"] = frame["investissement"] * af
    frame["loyer_equilibre_renove_m2"] = [
        equilibrium_rent_m2(float(c), af, charges_eur, float(s))
        for c, s in zip(frame["cout_renove_m2"], frame["surface_m2"], strict=True)
    ]
    frame["loyer_equilibre_neuf_m2"] = equilibrium_rent_m2(
        PRIX_REVIENT_NEUF_M2_EUR_2023, af, charges_eur, SURFACE_NEUF_M2
    )
    # Balancing subsidies: to the local SOCIAL rent (attribution reading)
    # and to the local MARKET rent (fluidity reading, SE-7); zero where
    # the equilibrium rent is already below the reference.
    for ref in ("social", "marche"):
        for segment, count, surface in (
            ("renove", frame["renovables"], frame["surface_m2"]),
            ("neuf", frame["deficit_neuf"], SURFACE_NEUF_M2),
        ):
            gap = (frame[f"loyer_equilibre_{segment}_m2"] - frame[f"loyer_{ref}_m2"]).clip(lower=0)
            frame[f"subvention_{ref}_{segment}_eur_an"] = gap * surface * 12 * count
        frame[f"subvention_{ref}_eur_an"] = (
            frame[f"subvention_{ref}_renove_eur_an"] + frame[f"subvention_{ref}_neuf_eur_an"]
        )
    frame["ratio_equilibre_renove_sur_marche"] = (
        frame["loyer_equilibre_renove_m2"] / frame["loyer_marche_m2"]
    )
    frame["ratio_equilibre_renove_sur_social"] = (
        frame["loyer_equilibre_renove_m2"] / frame["loyer_social_m2"]
    )
    return frame


def _quantiles(series: pd.Series, digits: int = 2) -> dict[str, float]:
    clean = series.dropna()
    quantiles = clean.quantile([0, 0.25, 0.5, 0.75, 1])
    keys = ("min", "p25", "median", "p75", "max")
    return {k: round(float(v), digits) for k, v in zip(keys, quantiles, strict=True)}


def _opt(value: float | None, digits: int) -> float | None:
    return None if value is None else round(value, digits)


def operator_summary(frame: pd.DataFrame, rp_total: float) -> dict[str, object]:
    """National aggregates and distributions of an operator frame.

    Distributions are simple medians ACROSS ZE (one ZE = one point, as
    in R-14); the rénovables-weighted median is published beside them
    (ST-5). Subsidies are summed only over ZE that have the reference
    rent — the count of ZE left out is published (ST-9).
    """
    if rp_total <= 0:
        raise InstitutionError("non-positive household base")
    renovables = float(frame["renovables"].sum())
    deficit = float(frame["deficit_neuf"].sum())
    invest = float(frame["investissement"].sum())
    annuite = float(frame["annuite"].sum())
    with_rents = frame.dropna(subset=["loyer_marche_m2", "loyer_social_m2"])
    portes = float((with_rents["renovables"] + with_rents["deficit_neuf"]).sum())
    return {
        "logements": {"renoves": round(renovables), "neufs": round(deficit)},
        "investissement_mdeur": round(invest / 1e9, 1),
        "dont_acquisition_mdeur": round(float(frame["cout_acquisition"].sum()) / 1e9, 1),
        "dont_renovation_mdeur": round(float(frame["cout_renovation"].sum()) / 1e9, 1),
        "dont_neuf_mdeur": round(float(frame["cout_neuf"].sum()) / 1e9, 1),
        "cout_unitaire_renove_median_eur": round(float(frame["cout_unitaire_renove"].median())),
        "cout_renove_m2_median_eur": round(float(frame["cout_renove_m2"].median())),
        "annuite_mdeur_an": round(annuite / 1e9, 2),
        "annuite_cumulee_40_ans_mdeur": round(annuite * 40 / 1e9, 1),
        "annuite_par_residence_principale_eur_an": round(annuite / rp_total),
        "annuite_par_logement_porte_eur_an": (
            round(annuite / (renovables + deficit)) if renovables + deficit > 0 else None
        ),
        "loyer_equilibre_renove_m2": _quantiles(frame["loyer_equilibre_renove_m2"]),
        "loyer_equilibre_renove_m2_median_pondere_renovables": _opt(
            weighted_median(frame["loyer_equilibre_renove_m2"], frame["renovables"]), 2
        ),
        "loyer_equilibre_neuf_m2": round(float(frame["loyer_equilibre_neuf_m2"].iloc[0]), 2),
        "loyer_marche_m2": _quantiles(frame["loyer_marche_m2"]),
        "loyer_social_m2": _quantiles(frame["loyer_social_m2"]),
        "ratio_equilibre_renove_sur_marche": _quantiles(
            with_rents["ratio_equilibre_renove_sur_marche"]
        ),
        "ratio_equilibre_renove_sur_social": _quantiles(
            with_rents["ratio_equilibre_renove_sur_social"]
        ),
        "n_ze": len(frame),
        "n_ze_avec_loyers": len(with_rents),
        "n_ze_sans_loyer_marche": int(frame["loyer_marche_m2"].isna().sum()),
        "n_ze_sans_loyer_social": int(frame["loyer_social_m2"].isna().sum()),
        "n_ze_equilibre_renove_sous_marche": int(
            (with_rents["loyer_equilibre_renove_m2"] <= with_rents["loyer_marche_m2"]).sum()
        ),
        "n_ze_equilibre_neuf_sous_marche": int(
            (with_rents["loyer_equilibre_neuf_m2"] <= with_rents["loyer_marche_m2"]).sum()
        ),
        "n_ze_equilibre_renove_sous_social": int(
            (with_rents["loyer_equilibre_renove_m2"] <= with_rents["loyer_social_m2"]).sum()
        ),
        "subvention_equilibre_social_mdeur_an": round(
            float(with_rents["subvention_social_eur_an"].sum()) / 1e9, 2
        ),
        "dont_renove_mdeur_an": round(
            float(with_rents["subvention_social_renove_eur_an"].sum()) / 1e9, 2
        ),
        "dont_neuf_mdeur_an": round(
            float(with_rents["subvention_social_neuf_eur_an"].sum()) / 1e9, 2
        ),
        "subvention_equilibre_marche_mdeur_an": round(
            float(with_rents["subvention_marche_eur_an"].sum()) / 1e9, 2
        ),
        "subvention_social_par_logement_porte_eur_an": (
            round(float(with_rents["subvention_social_eur_an"].sum()) / portes)
            if portes > 0
            else None
        ),
    }


def _ze_entry(row: pd.Series) -> dict[str, object]:
    def opt(value: float, digits: int) -> float | None:
        return None if pd.isna(value) else round(float(value), digits)

    return {
        "ze": str(row.name),
        "name": row["ze_name"] if pd.notna(row["ze_name"]) else None,
        "renovables": round(float(row["renovables"])),
        "deficit_neuf": round(float(row["deficit_neuf"])),
        "prix_m2_eur": round(float(row["prix_m2"])),
        "surface_m2": round(float(row["surface_m2"]), 1),
        "cout_renove_m2_eur": round(float(row["cout_renove_m2"])),
        "cout_unitaire_renove_eur": round(float(row["cout_unitaire_renove"])),
        "investissement_meur": round(float(row["investissement"]) / 1e6, 1),
        "loyer_equilibre_renove_m2": round(float(row["loyer_equilibre_renove_m2"]), 2),
        "loyer_marche_m2": opt(row["loyer_marche_m2"], 2),
        "loyer_social_m2": opt(row["loyer_social_m2"], 2),
        "subvention_social_meur_an": opt(row["subvention_social_eur_an"] / 1e6, 1),
    }


def operator_scenario(
    detente: pd.DataFrame,
    renovation_m2: pd.Series,
    prix_m2: pd.Series,
    loyer_marche_m2: pd.Series,
    loyer_social_m2: pd.Series,
    rp_total: float,
    h15: HypothesisRecord,
    h16: HypothesisRecord,
    h17: HypothesisRecord,
    h18: HypothesisRecord,
    h20: HypothesisRecord,
) -> dict[str, object]:
    """M-B payload: central frame, one-at-a-time sensitivities, rhythm, ZE lists."""

    def run(
        discount: float, reemploy: float, rate: float, years: float, charges: float
    ) -> pd.DataFrame:
        return operator_frame(
            detente,
            renovation_m2,
            prix_m2,
            loyer_marche_m2,
            loyer_social_m2,
            discount,
            reemploy,
            rate,
            years,
            charges,
        )

    c15, c16, c17, c18, c20 = (
        h15.central_value,
        h16.central_value,
        h17.central_value,
        h18.central_value,
        h20.central_value,
    )
    central = run(c15, c20, c16, c17, c18)
    summary = operator_summary(central, rp_total)

    def brief(frame: pd.DataFrame) -> dict[str, object]:
        s = operator_summary(frame, rp_total)
        renove = cast(dict[str, float], s["loyer_equilibre_renove_m2"])
        return {
            "investissement_mdeur": s["investissement_mdeur"],
            "annuite_mdeur_an": s["annuite_mdeur_an"],
            "loyer_equilibre_renove_median_m2": renove["median"],
            "loyer_equilibre_neuf_m2": s["loyer_equilibre_neuf_m2"],
            "n_ze_equilibre_renove_sous_marche": s["n_ze_equilibre_renove_sous_marche"],
            "subvention_equilibre_social_mdeur_an": s["subvention_equilibre_social_mdeur_an"],
            "subvention_equilibre_marche_mdeur_an": s["subvention_equilibre_marche_mdeur_an"],
        }

    sensibilite: dict[str, object] = {
        "h15_decote": {f"{d:g}": brief(run(d, c20, c16, c17, c18)) for d in DISCOUNT_GRID},
        "h20_remploi_pct": {
            f"{r:g}": brief(run(c15, r, c16, c17, c18))
            for r in (h20.plausible_range[0], c20, h20.plausible_range[1])
        },
        "h16_taux_pct": {
            f"{r:g}": brief(run(c15, c20, r, c17, c18))
            for r in (h16.plausible_range[0], c16, h16.plausible_range[1])
        },
        "h17_duree_ans": {
            f"{y:g}": brief(run(c15, c20, c16, y, c18))
            for y in (h17.plausible_range[0], c17, h17.plausible_range[1])
        },
        "h18_charges_eur": {
            f"{o:g}": brief(run(c15, c20, c16, c17, o))
            for o in (h18.plausible_range[0], c18, h18.plausible_range[1])
        },
        "favorable": brief(
            run(
                h15.plausible_range[0],
                h20.plausible_range[0],
                h16.plausible_range[0],
                h17.plausible_range[1],
                h18.plausible_range[0],
            )
        ),
        "defavorable": brief(
            run(
                h15.plausible_range[1],
                h20.plausible_range[1],
                h16.plausible_range[1],
                h17.plausible_range[0],
                h18.plausible_range[1],
            )
        ),
    }
    invest = float(central["investissement"].sum())
    portes = float((central["renovables"] + central["deficit_neuf"]).sum())
    rythme = [
        {
            "programme_ans": y,
            "investissement_mdeur_an": round(invest / y / 1e9, 1),
            "logements_par_an": round(portes / y),
        }
        for y in PROGRAMME_YEARS_GRID
    ]
    ranked = central.sort_values(
        ["loyer_equilibre_renove_m2", "ze_name"], ascending=[False, True], kind="stable"
    )
    return {
        "hypotheses": {
            h.id: {
                "name": h.name,
                "central": h.central_value,
                "plausible_range": list(h.plausible_range),
            }
            for h in (h15, h16, h17, h18, h20)
        },
        "annuity_factor_central": round(annuity_factor(c16, c17), 5),
        "neuf": {
            "prix_revient_eur_2023": remob.PRIX_REVIENT_NEUF_EUR_2023,
            "prix_revient_m2_eur_2023": PRIX_REVIENT_NEUF_M2_EUR_2023,
            "surface_m2": round(SURFACE_NEUF_M2, 1),
        },
        "central": summary,
        "sensibilite": sensibilite,
        "rythme_programme": rythme,
        "loyer_equilibre_le_plus_haut": [_ze_entry(r) for _, r in ranked.head(8).iterrows()],
        "loyer_equilibre_le_plus_bas": [
            _ze_entry(r) for _, r in ranked.tail(8).iloc[::-1].iterrows()
        ],
    }


# -------------------------------------------------------------- M-C lease


def lease_scenario(
    detente: pd.DataFrame,
    renovation_m2: pd.Series,
    loyer_marche_m2: pd.Series,
    loyer_social_m2: pd.Series,
    rate_pct: float,
    lease_years: float,
    charges_eur: float,
) -> dict[str, object]:
    """M-C payload: works-only operator over the lease, TFPB exempt, volume by consent."""
    frame = (
        detente.join(renovation_m2.rename("renovation_m2"), how="inner")
        .join(loyer_marche_m2.rename("loyer_marche_m2"), how="left")
        .join(loyer_social_m2.rename("loyer_social_m2"), how="left")
    )
    if frame.empty:
        raise InstitutionError("no tense ZE joined with renovation costs")
    af = annuity_factor(rate_pct, lease_years)
    charges_hors_tfpb = max(0.0, charges_eur - TFPB_EUR_PER_DWELLING_2023)
    frame["renovables"] = frame["renovables"].fillna(0)
    frame["deficit_neuf"] = frame["deficit_neuf"].fillna(0)
    frame["surface_m2"] = (
        frame["part_maison"] * remob.SURFACE_MAISON_M2
        + (1 - frame["part_maison"]) * remob.SURFACE_APPART_M2
    )
    frame["loyer_equilibre_travaux_m2"] = [
        equilibrium_rent_m2(float(c), af, charges_hors_tfpb, float(s))
        for c, s in zip(frame["renovation_m2"], frame["surface_m2"], strict=True)
    ]
    besoin = float(frame["besoin_mobilisation"].sum())
    renovables = float(frame["renovables"].sum())
    deficit = float(frame["deficit_neuf"].sum())
    travaux = float((frame["renovables"] * frame["renovation_m2"] * frame["surface_m2"]).sum())
    neuf = deficit * remob.PRIX_REVIENT_NEUF_EUR_2023
    with_rents = frame.dropna(subset=["loyer_marche_m2", "loyer_social_m2"])
    grid = [
        {
            "consentement_pct": round(c * 100),
            "logements_renoves": round(renovables * c),
            "investissement_travaux_mdeur": round(travaux * c / 1e9, 1),
            "investissement_total_mdeur": round((travaux * c + neuf) / 1e9, 1),
            "couverture_besoin_bail_seul": round(renovables * c / besoin, 2),
            "couverture_besoin_avec_neuf": round((renovables * c + deficit) / besoin, 2),
        }
        for c in CONSENT_SHARE_GRID
    ]
    return {
        "duree_amortissement_ans": lease_years,
        "taux_pct": rate_pct,
        "charges_hors_tfpb_eur_logement_an": round(charges_hors_tfpb),
        "annuity_factor": round(af, 5),
        "loyer_equilibre_travaux_m2": _quantiles(frame["loyer_equilibre_travaux_m2"]),
        "n_ze_travaux_sous_social": int(
            (with_rents["loyer_equilibre_travaux_m2"] <= with_rents["loyer_social_m2"]).sum()
        ),
        "n_ze_avec_loyers": len(with_rents),
        "investissement_travaux_plein_mdeur": round(travaux / 1e9, 1),
        "investissement_neuf_mdeur": round(neuf / 1e9, 1),
        "grille_consentement": grid,
    }


# ------------------------------------------------------------- M-D toll shift


def holding_charge_eur_per_dwelling(product_eur: float, dwellings: float) -> float:
    """Yearly holding charge that replaces the DMTO product over the stock."""
    if dwellings <= 0:
        raise InstitutionError("non-positive dwelling base")
    return product_eur / dwellings


def toll_shift_scenario(
    prix: pd.DataFrame,
    niveau_vie: pd.Series,
    tense_index: pd.Index,
    perimeter_share: pd.Series,
    dwellings_perimeter: float,
    ze_names: pd.Series,
) -> dict[str, object]:
    """M-D payload: departmental toll per ZE vs the equivalent holding charge.

    Numerator = the DEPARTMENTAL duty only (voted rate × median price),
    the part the charge replaces (ST-2/HD-5); the communal tax, the
    State assessment fee, the CSI and the notary fee stay as the
    residual toll. ZE outside the OFGL perimeter (share of stock < floor)
    are published but excluded from the quantiles (ST-3).
    """
    for col in ("prix_median", "taux_dmto_pct", "n_ventes"):
        if col not in prix.columns:
            raise InstitutionError(f"prices frame lacks {col}")
    charges = {
        vintage: holding_charge_eur_per_dwelling(product, dwellings_perimeter)
        for vintage, product in DMTO_PRODUCT_EUR.items()
    }
    charge = charges[DMTO_CENTRAL_VINTAGE]
    frame = (
        prix.join(niveau_vie.rename("niveau_vie_median"), how="left")
        .join(ze_names.rename("ze_name"), how="left")
        .join(perimeter_share.rename("part_perimetre"), how="left")
    )
    # The territorialized total rate is departmental × 1.0237 + 1.20 (H-13):
    # recover the departmental duty proper.
    frame["taux_departemental_pct"] = (
        frame["taux_dmto_pct"] - transaction.COMMUNAL_TAX_PCT
    ) / transaction.ASSESSMENT_FEE_FACTOR
    frame["droit_departemental_eur"] = frame["prix_median"] * frame["taux_departemental_pct"] / 100
    frame["frais_assiette_eur"] = frame["droit_departemental_eur"] * (
        transaction.ASSESSMENT_FEE_FACTOR - 1
    )
    frame["taxe_communale_eur"] = frame["prix_median"] * transaction.COMMUNAL_TAX_PCT / 100
    frame["csi_eur"] = frame["prix_median"].map(transaction.csi_eur)
    frame["emoluments_eur"] = frame["prix_median"].map(transaction.emoluments_ttc)
    frame["peage_total_eur"] = (
        frame["droit_departemental_eur"]
        + frame["frais_assiette_eur"]
        + frame["taxe_communale_eur"]
        + frame["csi_eur"]
        + frame["emoluments_eur"]
    )
    frame["peage_residuel_eur"] = frame["peage_total_eur"] - frame["droit_departemental_eur"]
    monthly = frame["niveau_vie_median"] / 12
    frame["peage_total_mois"] = frame["peage_total_eur"] / monthly
    frame["droit_departemental_mois"] = frame["droit_departemental_eur"] / monthly
    frame["peage_residuel_mois"] = frame["peage_residuel_eur"] / monthly
    frame["annees_equivalentes"] = frame["droit_departemental_eur"] / charge
    frame["charge_pct_prix_median"] = charge / frame["prix_median"] * 100
    frame["tendue"] = frame.index.isin(tense_index)
    frame["part_perimetre"] = frame["part_perimetre"].fillna(0)
    frame["dans_perimetre"] = frame["part_perimetre"] >= PERIMETER_SHARE_FLOOR
    inside = frame[frame["dans_perimetre"]]
    tense = inside[inside["tendue"]]
    ranked = inside.sort_values(
        ["annees_equivalentes", "ze_name"], ascending=[False, True], kind="stable"
    )

    def entry(row: pd.Series) -> dict[str, object]:
        return {
            "ze": str(row.name),
            "name": row["ze_name"] if pd.notna(row["ze_name"]) else None,
            "prix_median_eur": round(float(row["prix_median"])),
            "droit_departemental_eur": round(float(row["droit_departemental_eur"])),
            "annees_equivalentes": round(float(row["annees_equivalentes"]), 1),
            "charge_pct_prix_median": round(float(row["charge_pct_prix_median"]), 2),
            "part_perimetre_pct": round(float(row["part_perimetre"]) * 100),
            "tendue": bool(row["tendue"]),
        }

    partial = frame[(frame["part_perimetre"] > 0) & (frame["part_perimetre"] < 1)]
    return {
        "produit_dmto_mdeur": {k: round(v / 1e9, 1) for k, v in DMTO_PRODUCT_EUR.items()},
        "millesime_central": DMTO_CENTRAL_VINTAGE,
        "perimetre": "OFGL périmètre constant (hors 75, 69, 2A, 2B, 972, 973)",
        "logements_perimetre": round(dwellings_perimeter),
        "charge_detention_eur_logement_an": {k: round(v) for k, v in charges.items()},
        "numerateur": (
            "droit DÉPARTEMENTAL seul (taux voté × prix médian) — la part que la charge remplace"
        ),
        "droit_departemental_eur": _quantiles(inside["droit_departemental_eur"], 0),
        "droit_departemental_eur_median_pondere_ventes": _opt(
            weighted_median(inside["droit_departemental_eur"], inside["n_ventes"]), 0
        ),
        "peage_total_mois_niveau_vie": _quantiles(inside["peage_total_mois"]),
        "droit_departemental_mois_niveau_vie": _quantiles(inside["droit_departemental_mois"]),
        "peage_residuel_mois_niveau_vie": _quantiles(inside["peage_residuel_mois"]),
        "annees_equivalentes": _quantiles(inside["annees_equivalentes"], 1),
        "annees_equivalentes_median_pondere_ventes": _opt(
            weighted_median(inside["annees_equivalentes"], inside["n_ventes"]), 1
        ),
        "annees_equivalentes_tendues": _quantiles(tense["annees_equivalentes"], 1),
        "annees_equivalentes_autres": _quantiles(
            inside[~inside["tendue"]]["annees_equivalentes"], 1
        ),
        "charge_pct_prix_median": _quantiles(inside["charge_pct_prix_median"], 2),
        "n_ze": len(frame),
        "n_ze_dans_perimetre": len(inside),
        "n_ze_hors_perimetre": int((~frame["dans_perimetre"]).sum()),
        "n_ze_perimetre_partiel": len(partial),
        "n_ze_tendues_dans_perimetre": len(tense),
        "n_ze_sans_niveau_vie": int(frame["niveau_vie_median"].isna().sum()),
        "ze_perimetre_partiel": [
            entry(r) for _, r in partial.sort_values("part_perimetre").iterrows()
        ],
        "bascule_la_plus_favorable_au_mobile": [entry(r) for _, r in ranked.head(8).iterrows()],
        "bascule_la_moins_favorable_au_mobile": [
            entry(r) for _, r in ranked.tail(8).iloc[::-1].iterrows()
        ],
    }
