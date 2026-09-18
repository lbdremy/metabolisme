"""Pure transforms for the institutional-proposal scenarios (session 7,
2026-09-18 — INTRO logement §16 scenarios, method INTRO step 13).

The diagnostic arc left three quantified constraints (I-07/I-09/I-10) and
one institutional parameter (R-14: ~83 % of the purchase toll is fiscal).
This module prices the MECHANISMS that could answer them, on the same
frozen inputs, so the proposal compares several designs instead of
defending one (DEC-03):

- M-A  the existing incentive channel (TLV/ZLV) at its documented exit
       rate (H-14, S-22) — the reference scenario;
- M-B  a collective operator that ACQUIRES the local durable-vacant
       stock at market value (H-15, D-22), renovates it (R-09 unit
       costs) and builds new on brownfields where the stock is missing
       (S-18), financed at the social-housing loan terms (H-16/H-17)
       with the sector's observed operating-cost structure (H-18) —
       the output is a per-ZE EQUILIBRIUM RENT compared with the local
       market and social rents;
- M-C  the same operator WITHOUT acquisition — bail à réhabilitation
       (D-21, S-46): works only, amortised over the average lease,
       volume conditional on owner consent (grid, DEC-09);
- M-D  shifting the fiscal part of the transaction toll (DMTO, D-19)
       to a yearly holding charge over the dwelling stock (S-39, C-14)
       — a redistribution between mobile and immobile households, with
       the causal evidence on volumes (S-43) kept out of the arithmetic.

Descriptive arithmetic on published sources; no behavioural model. No
I/O, no clock — reads happen in the shell.
"""

from __future__ import annotations

from typing import cast

import pandas as pd

from logement.core import remob, transaction
from logement.core.lovac import plm_parent
from logement.models import HypothesisRecord

# Average bail à réhabilitation duration (S-46: « entre 12 et 99 ans, en
# moyenne 30 ans ») — the works of M-C are amortised over the lease, not
# over the life of the building the operator does not own.
BAR_AMORTISATION_YEARS = 30.0
# TLV yield 2023 (S-22, p. 36: « 271 M€ en 2023 pour la TLV ») — the
# order of magnitude of what the incentive channel already levies.
TLV_YIELD_2023_EUR = 271e6
# Departmental DMTO product 2024 on the OFGL constant perimeter (S-39,
# p. 4: « un montant total de 9,9 Md€ » — hors Rhône, Martinique,
# Guyane, Corse et Paris, C-14).
DMTO_PRODUCT_2024_EUR = 9.9e9
# Departments outside the OFGL constant perimeter (S-39, champ des
# graphiques 6) — the dwelling base of the holding charge excludes them.
DMTO_PERIMETER_EXCLUDED_DEPARTEMENTS = ("75", "69", "2A", "2B", "972", "973")
# Comparison horizons for the incentive channel and the consent grid of
# the lease mechanism: descriptive grids, deliberately NOT hypotheses
# (no frozen source elects a central value — same status as R-14's
# HOLDING_YEARS_GRID).
HORIZON_YEARS_GRID = (5, 10, 20)
CONSENT_SHARE_GRID = (0.10, 0.25, 0.50, 1.00)
# H-15 sensitivity grid (central 1.0 = valeur vénale, DEC-04).
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


def equilibrium_rent(annuity_eur: float, operating_share: float) -> float:
    """Net rent covering the annuity AND the operating costs (D-20, H-18)."""
    if not 0 <= operating_share < 1:
        raise InstitutionError(f"implausible operating share {operating_share}")
    return annuity_eur / (1 - operating_share)


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
    """Count the exits from vacancy the incentive channel would produce, vs the need."""
    besoin = float(detente["besoin_mobilisation"].sum())
    gisement = float(detente["structurelle"].fillna(0).sum())
    if besoin <= 0:
        raise InstitutionError("non-positive detente need")
    grid: list[dict[str, object]] = []
    for label, rate in (
        ("bas", h14.plausible_range[0]),
        ("central", h14.central_value),
        ("haut", h14.plausible_range[1]),
    ):
        for years in HORIZON_YEARS_GRID:
            share = min(1.0, rate / 100 * years)
            sorties = gisement * share
            grid.append(
                {
                    "taux": label,
                    "taux_pct_an": rate,
                    "horizon_ans": years,
                    "sorties": round(sorties),
                    "part_gisement_pct": round(share * 100, 1),
                    "couverture_besoin": round(sorties / besoin, 3),
                }
            )
    central_10 = next(g for g in grid if g["taux"] == "central" and g["horizon_ans"] == 10)
    return {
        "hypothese": {
            "id": h14.id,
            "central_pct_an": h14.central_value,
            "plausible_range": list(h14.plausible_range),
        },
        "gisement_effectif": round(gisement),
        "besoin": round(besoin),
        "grille": grid,
        "central_10_ans": central_10,
        "rendement_tlv_2023_meur": round(TLV_YIELD_2023_EUR / 1e6),
    }


# ------------------------------------------------------------ M-B operator


def operator_frame(
    detente: pd.DataFrame,
    unit_renovation_cost: pd.Series,
    prix_median: pd.Series,
    loyer_marche_m2: pd.Series,
    loyer_social_m2: pd.Series,
    niveau_vie: pd.Series,
    discount: float,
    rate_pct: float,
    years: float,
    operating_share: float,
) -> pd.DataFrame:
    """Per-tense-ZE costs, annuities and equilibrium rents of the operator.

    Renovated segment: acquisition at `discount` × local median price
    (C-12) plus the R-09 renovation unit cost; new segment: the S-18
    production price (land included). Equilibrium rents are per m² per
    month at the C-07 surfaces, comparable with the S-09 market rent and
    the S-28 social rent of the same ZE.
    """
    if not 0 < discount <= 1:
        raise InstitutionError(f"implausible discount factor {discount}")
    frame = (
        detente.join(unit_renovation_cost.rename("cout_renovation_unitaire"), how="inner")
        .join(prix_median.rename("prix_median"), how="inner")
        .join(loyer_marche_m2.rename("loyer_marche_m2"), how="left")
        .join(loyer_social_m2.rename("loyer_social_m2"), how="left")
        .join(niveau_vie.rename("niveau_vie_median"), how="left")
    )
    if frame.empty:
        raise InstitutionError("no tense ZE joined with prices and renovation costs")
    af = annuity_factor(rate_pct, years)
    frame["renovables"] = frame["renovables"].fillna(0)
    frame["deficit_neuf"] = frame["deficit_neuf"].fillna(0)
    frame["prix_acquisition"] = frame["prix_median"] * discount
    frame["cout_unitaire_renove"] = frame["prix_acquisition"] + frame["cout_renovation_unitaire"]
    frame["cout_acquisition"] = frame["renovables"] * frame["prix_acquisition"]
    frame["cout_renovation"] = frame["renovables"] * frame["cout_renovation_unitaire"]
    frame["cout_neuf"] = frame["deficit_neuf"] * remob.PRIX_REVIENT_NEUF_EUR_2023
    frame["investissement"] = (
        frame["cout_acquisition"] + frame["cout_renovation"] + frame["cout_neuf"]
    )
    frame["annuite"] = frame["investissement"] * af
    frame["surface_m2"] = (
        frame["part_maison"] * remob.SURFACE_MAISON_M2
        + (1 - frame["part_maison"]) * remob.SURFACE_APPART_M2
    )
    for segment, unit in (
        ("renove", frame["cout_unitaire_renove"]),
        ("neuf", pd.Series(remob.PRIX_REVIENT_NEUF_EUR_2023, index=frame.index)),
    ):
        annual = (unit * af).map(lambda a: equilibrium_rent(float(a), operating_share))
        frame[f"loyer_equilibre_{segment}_m2"] = annual / 12 / frame["surface_m2"]
    # Balancing subsidy to bring every dwelling down to the local SOCIAL
    # rent (zero where the equilibrium rent is already below it).
    for segment, count in (("renove", frame["renovables"]), ("neuf", frame["deficit_neuf"])):
        gap = (frame[f"loyer_equilibre_{segment}_m2"] - frame["loyer_social_m2"]).clip(lower=0)
        frame[f"subvention_{segment}_eur_an"] = gap * frame["surface_m2"] * 12 * count
    frame["subvention_eur_an"] = frame["subvention_renove_eur_an"].fillna(0) + frame[
        "subvention_neuf_eur_an"
    ].fillna(0)
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


def operator_summary(frame: pd.DataFrame, rp_total: float) -> dict[str, object]:
    """National aggregates and distributions of an operator frame."""
    if rp_total <= 0:
        raise InstitutionError("non-positive household base")
    renovables = float(frame["renovables"].sum())
    deficit = float(frame["deficit_neuf"].sum())
    invest = float(frame["investissement"].sum())
    annuite = float(frame["annuite"].sum())
    with_rents = frame.dropna(subset=["loyer_marche_m2", "loyer_social_m2"])
    return {
        "logements": {"renoves": round(renovables), "neufs": round(deficit)},
        "investissement_mdeur": round(invest / 1e9, 1),
        "dont_acquisition_mdeur": round(float(frame["cout_acquisition"].sum()) / 1e9, 1),
        "dont_renovation_mdeur": round(float(frame["cout_renovation"].sum()) / 1e9, 1),
        "dont_neuf_mdeur": round(float(frame["cout_neuf"].sum()) / 1e9, 1),
        "cout_unitaire_renove_median_eur": round(float(frame["cout_unitaire_renove"].median())),
        "annuite_mdeur_an": round(annuite / 1e9, 2),
        "annuite_par_residence_principale_eur_an": round(annuite / rp_total),
        "loyer_equilibre_renove_m2": _quantiles(frame["loyer_equilibre_renove_m2"]),
        "loyer_equilibre_neuf_m2": _quantiles(frame["loyer_equilibre_neuf_m2"]),
        "loyer_marche_m2": _quantiles(frame["loyer_marche_m2"]),
        "loyer_social_m2": _quantiles(frame["loyer_social_m2"]),
        "ratio_equilibre_renove_sur_marche": _quantiles(frame["ratio_equilibre_renove_sur_marche"]),
        "ratio_equilibre_renove_sur_social": _quantiles(frame["ratio_equilibre_renove_sur_social"]),
        "n_ze": len(frame),
        "n_ze_avec_loyers": len(with_rents),
        "n_ze_equilibre_renove_sous_marche": int(
            (with_rents["loyer_equilibre_renove_m2"] <= with_rents["loyer_marche_m2"]).sum()
        ),
        "n_ze_equilibre_renove_sous_social": int(
            (with_rents["loyer_equilibre_renove_m2"] <= with_rents["loyer_social_m2"]).sum()
        ),
        "subvention_equilibre_social_mdeur_an": round(
            float(frame["subvention_eur_an"].sum()) / 1e9, 2
        ),
        "dont_renove_mdeur_an": round(float(frame["subvention_renove_eur_an"].sum()) / 1e9, 2),
        "dont_neuf_mdeur_an": round(float(frame["subvention_neuf_eur_an"].sum()) / 1e9, 2),
    }


def _ze_entry(row: pd.Series) -> dict[str, object]:
    def opt(value: float, digits: int) -> float | None:
        return None if pd.isna(value) else round(float(value), digits)

    return {
        "ze": str(row.name),
        "name": row["ze_name"] if pd.notna(row["ze_name"]) else None,
        "renovables": round(float(row["renovables"])),
        "deficit_neuf": round(float(row["deficit_neuf"])),
        "prix_acquisition_eur": round(float(row["prix_acquisition"])),
        "cout_unitaire_renove_eur": round(float(row["cout_unitaire_renove"])),
        "investissement_meur": round(float(row["investissement"]) / 1e6, 1),
        "loyer_equilibre_renove_m2": round(float(row["loyer_equilibre_renove_m2"]), 2),
        "loyer_equilibre_neuf_m2": round(float(row["loyer_equilibre_neuf_m2"]), 2),
        "loyer_marche_m2": opt(row["loyer_marche_m2"], 2),
        "loyer_social_m2": opt(row["loyer_social_m2"], 2),
        "subvention_meur_an": round(float(row["subvention_eur_an"]) / 1e6, 1),
    }


def operator_scenario(
    detente: pd.DataFrame,
    unit_renovation_cost: pd.Series,
    prix_median: pd.Series,
    loyer_marche_m2: pd.Series,
    loyer_social_m2: pd.Series,
    niveau_vie: pd.Series,
    rp_total: float,
    h15: HypothesisRecord,
    h16: HypothesisRecord,
    h17: HypothesisRecord,
    h18: HypothesisRecord,
) -> dict[str, object]:
    """M-B payload: central frame + one-at-a-time sensitivities + ZE lists."""

    def run(discount: float, rate: float, years: float, opex: float) -> pd.DataFrame:
        return operator_frame(
            detente,
            unit_renovation_cost,
            prix_median,
            loyer_marche_m2,
            loyer_social_m2,
            niveau_vie,
            discount,
            rate,
            years,
            opex,
        )

    central = run(h15.central_value, h16.central_value, h17.central_value, h18.central_value)
    summary = operator_summary(central, rp_total)

    def brief(frame: pd.DataFrame) -> dict[str, object]:
        s = operator_summary(frame, rp_total)
        return {
            "investissement_mdeur": s["investissement_mdeur"],
            "annuite_mdeur_an": s["annuite_mdeur_an"],
            "loyer_equilibre_renove_median_m2": cast(
                dict[str, float], s["loyer_equilibre_renove_m2"]
            )["median"],
            "n_ze_equilibre_renove_sous_marche": s["n_ze_equilibre_renove_sous_marche"],
            "subvention_equilibre_social_mdeur_an": s["subvention_equilibre_social_mdeur_an"],
        }

    sensibilite: dict[str, object] = {
        "h15_decote": {
            f"{d:g}": brief(run(d, h16.central_value, h17.central_value, h18.central_value))
            for d in DISCOUNT_GRID
        },
        "h16_taux_pct": {
            f"{r:g}": brief(run(h15.central_value, r, h17.central_value, h18.central_value))
            for r in (h16.plausible_range[0], h16.central_value, h16.plausible_range[1])
        },
        "h17_duree_ans": {
            f"{y:g}": brief(run(h15.central_value, h16.central_value, y, h18.central_value))
            for y in (h17.plausible_range[0], h17.central_value, h17.plausible_range[1])
        },
        "h18_charges": {
            f"{o:g}": brief(run(h15.central_value, h16.central_value, h17.central_value, o))
            for o in (h18.plausible_range[0], h18.central_value, h18.plausible_range[1])
        },
        "favorable": brief(
            run(
                h15.plausible_range[0],
                h16.plausible_range[0],
                h17.plausible_range[1],
                h18.plausible_range[0],
            )
        ),
        "defavorable": brief(
            run(
                h15.plausible_range[1],
                h16.plausible_range[1],
                h17.plausible_range[0],
                h18.plausible_range[1],
            )
        ),
    }
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
            for h in (h15, h16, h17, h18)
        },
        "annuity_factor_central": round(annuity_factor(h16.central_value, h17.central_value), 5),
        "prix_revient_neuf_eur_2023": remob.PRIX_REVIENT_NEUF_EUR_2023,
        "central": summary,
        "sensibilite": sensibilite,
        "loyer_equilibre_le_plus_haut": [_ze_entry(r) for _, r in ranked.head(8).iterrows()],
        "loyer_equilibre_le_plus_bas": [
            _ze_entry(r) for _, r in ranked.tail(8).iloc[::-1].iterrows()
        ],
    }


# -------------------------------------------------------------- M-C lease


def lease_scenario(
    detente: pd.DataFrame,
    unit_renovation_cost: pd.Series,
    loyer_marche_m2: pd.Series,
    loyer_social_m2: pd.Series,
    rate_pct: float,
    operating_share: float,
) -> dict[str, object]:
    """M-C payload: works-only operator over the lease, volume by consent."""
    frame = (
        detente.join(unit_renovation_cost.rename("cout_renovation_unitaire"), how="inner")
        .join(loyer_marche_m2.rename("loyer_marche_m2"), how="left")
        .join(loyer_social_m2.rename("loyer_social_m2"), how="left")
    )
    if frame.empty:
        raise InstitutionError("no tense ZE joined with renovation costs")
    af = annuity_factor(rate_pct, BAR_AMORTISATION_YEARS)
    frame["renovables"] = frame["renovables"].fillna(0)
    frame["deficit_neuf"] = frame["deficit_neuf"].fillna(0)
    frame["surface_m2"] = (
        frame["part_maison"] * remob.SURFACE_MAISON_M2
        + (1 - frame["part_maison"]) * remob.SURFACE_APPART_M2
    )
    annual = (frame["cout_renovation_unitaire"] * af).map(
        lambda a: equilibrium_rent(float(a), operating_share)
    )
    frame["loyer_equilibre_travaux_m2"] = annual / 12 / frame["surface_m2"]
    besoin = float(frame["besoin_mobilisation"].sum())
    renovables = float(frame["renovables"].sum())
    deficit = float(frame["deficit_neuf"].sum())
    travaux = float((frame["renovables"] * frame["cout_renovation_unitaire"]).sum())
    neuf = deficit * remob.PRIX_REVIENT_NEUF_EUR_2023
    with_rents = frame.dropna(subset=["loyer_marche_m2", "loyer_social_m2"])
    grid = [
        {
            "consentement_pct": round(c * 100),
            "logements_renoves": round(renovables * c),
            "investissement_travaux_mdeur": round(travaux * c / 1e9, 1),
            "investissement_total_mdeur": round((travaux * c + neuf) / 1e9, 1),
            "couverture_besoin": round((renovables * c + deficit) / besoin, 2),
        }
        for c in CONSENT_SHARE_GRID
    ]
    return {
        "duree_amortissement_ans": BAR_AMORTISATION_YEARS,
        "taux_pct": rate_pct,
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
    dwellings_perimeter: float,
    ze_names: pd.Series,
) -> dict[str, object]:
    """M-D payload: fiscal toll per ZE vs the equivalent holding charge."""
    for col in ("prix_median", "taux_dmto_pct"):
        if col not in prix.columns:
            raise InstitutionError(f"prices frame lacks {col}")
    charge = holding_charge_eur_per_dwelling(DMTO_PRODUCT_2024_EUR, dwellings_perimeter)
    frame = prix.join(niveau_vie.rename("niveau_vie_median"), how="left").join(
        ze_names.rename("ze_name"), how="left"
    )
    frame["droits_eur"] = frame["prix_median"] * frame["taux_dmto_pct"] / 100
    frame["csi_eur"] = frame["prix_median"].map(transaction.csi_eur)
    frame["emoluments_eur"] = frame["prix_median"].map(transaction.emoluments_ttc)
    frame["peage_fiscal_eur"] = frame["droits_eur"] + frame["csi_eur"]
    frame["peage_total_eur"] = frame["peage_fiscal_eur"] + frame["emoluments_eur"]
    frame["peage_fiscal_mois"] = frame["peage_fiscal_eur"] / (frame["niveau_vie_median"] / 12)
    frame["peage_residuel_mois"] = frame["emoluments_eur"] / (frame["niveau_vie_median"] / 12)
    frame["annees_equivalentes"] = frame["peage_fiscal_eur"] / charge
    frame["tendue"] = frame.index.isin(tense_index)
    tense = frame[frame["tendue"]]
    ranked = frame.sort_values(
        ["annees_equivalentes", "ze_name"], ascending=[False, True], kind="stable"
    )

    def entry(row: pd.Series) -> dict[str, object]:
        return {
            "ze": str(row.name),
            "name": row["ze_name"] if pd.notna(row["ze_name"]) else None,
            "prix_median_eur": round(float(row["prix_median"])),
            "peage_fiscal_eur": round(float(row["peage_fiscal_eur"])),
            "annees_equivalentes": round(float(row["annees_equivalentes"]), 1),
            "tendue": bool(row["tendue"]),
        }

    return {
        "produit_dmto_2024_mdeur": round(DMTO_PRODUCT_2024_EUR / 1e9, 1),
        "perimetre": "OFGL périmètre constant (hors 75, 69, 2A, 2B, 972, 973)",
        "logements_perimetre": round(dwellings_perimeter),
        "charge_detention_eur_logement_an": round(charge),
        "peage_fiscal_eur": _quantiles(frame["peage_fiscal_eur"], 0),
        "peage_fiscal_mois_niveau_vie": _quantiles(frame["peage_fiscal_mois"]),
        "peage_residuel_mois_niveau_vie": _quantiles(frame["peage_residuel_mois"]),
        "annees_equivalentes": _quantiles(frame["annees_equivalentes"], 1),
        "annees_equivalentes_tendues": _quantiles(tense["annees_equivalentes"], 1),
        "annees_equivalentes_autres": _quantiles(frame[~frame["tendue"]]["annees_equivalentes"], 1),
        "n_ze": len(frame),
        "n_ze_tendues": len(tense),
        "bascule_la_plus_favorable_au_mobile": [entry(r) for _, r in ranked.head(8).iterrows()],
        "bascule_la_moins_favorable_au_mobile": [
            entry(r) for _, r in ranked.tail(8).iloc[::-1].iterrows()
        ],
    }
