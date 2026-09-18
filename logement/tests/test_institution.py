"""Behaviour tests for the pure institutional-scenario core (R-15..R-17)."""

from __future__ import annotations

import pandas as pd
import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

from logement.core import institution, remob
from logement.models import HypothesisRecord


def _hypothesis(hid: str, central: float, low: float, high: float) -> HypothesisRecord:
    return HypothesisRecord(
        id=hid,
        name="test",
        description="test",
        central_value=central,
        plausible_range=(low, high),
        unit="test",
        confidence="low",
    )


def _detente() -> pd.DataFrame:
    """Two tense ZE: one fully covered by its stock, one with a deficit."""
    return pd.DataFrame(
        {
            "besoin_mobilisation": [1000.0, 1000.0],
            "structurelle": [1500.0, 400.0],
            "renovables": [1000.0, 400.0],
            "deficit_neuf": [0.0, 600.0],
            "part_maison": [0.0, 1.0],
            "ze_name": ["Alpha", "Beta"],
        },
        index=pd.Index(["0001", "0002"], name="ze"),
    )


# ------------------------------------------------------------------ finance


def test_annuity_factor_matches_closed_form() -> None:
    """2.30 % over 40 years: the textbook constant-annuity factor."""
    factor = institution.annuity_factor(2.30, 40)
    assert factor == pytest.approx(0.023 / (1 - 1.023**-40))
    assert institution.annuity_factor(0.0, 25) == pytest.approx(1 / 25)


@given(
    rate=st.one_of(st.just(0.0), st.floats(min_value=0.01, max_value=10.0)),
    years=st.floats(min_value=1.0, max_value=80.0),
)
@settings(max_examples=200)
def test_annuity_factor_bounds(rate: float, years: float) -> None:
    """The yearly payment per euro lies between 1/n (free money) and 1 (one year)."""
    factor = institution.annuity_factor(rate, years)
    assert (1 / years) * (1 - 1e-6) <= factor <= 1.0 + rate / 100 + 1e-9


def test_annuity_factor_increases_with_rate_and_decreases_with_years() -> None:
    """Monotonicity in both arguments (the sensitivities must read in one direction)."""
    assert institution.annuity_factor(2.0, 40) < institution.annuity_factor(3.0, 40)
    assert institution.annuity_factor(2.0, 50) < institution.annuity_factor(2.0, 30)


def test_annuity_factor_rejects_bad_inputs() -> None:
    """Zero/negative durations and negative rates are definite rejects."""
    with pytest.raises(institution.InstitutionError):
        institution.annuity_factor(2.0, 0)
    with pytest.raises(institution.InstitutionError):
        institution.annuity_factor(-1.0, 10)


def test_equilibrium_rent_m2_adds_annuity_and_fixed_charges() -> None:
    """Rent/m²/month = (investment/m² × factor + charges/surface) / 12 (D-23)."""
    rent = institution.equilibrium_rent_m2(3_000.0, 0.04, 2_652.0, 66.0)
    assert rent == pytest.approx((3_000.0 * 0.04 + 2_652.0 / 66.0) / 12)
    with pytest.raises(institution.InstitutionError):
        institution.equilibrium_rent_m2(3_000.0, 0.04, 2_652.0, 0.0)
    with pytest.raises(institution.InstitutionError):
        institution.equilibrium_rent_m2(3_000.0, 0.04, -1.0, 66.0)


def test_weighted_median() -> None:
    """Weighted median picks the value where cumulative weight crosses half."""
    values = pd.Series([1.0, 2.0, 3.0, 4.0])
    assert institution.weighted_median(values, pd.Series([1.0, 1.0, 1.0, 10.0])) == 4.0
    assert institution.weighted_median(values, pd.Series([1.0, 1.0, 1.0, 1.0])) == 2.0
    assert institution.weighted_median(values, pd.Series([0.0, 0.0, 0.0, 0.0])) is None


def test_neuf_surface_is_derived_from_s18() -> None:
    """169 200 € at 2 550 €/m² is the ~66 m² surface utile S-18 reports."""
    assert institution.SURFACE_NEUF_M2 == pytest.approx(66.35, abs=0.01)


# ---------------------------------------------------------------- RPLS rents


def test_social_rent_is_stock_weighted_and_na_safe() -> None:
    """Rents aggregate by stock (C-09); a masked rent is dropped, never zero."""
    raw = pd.DataFrame(
        {
            "DEPCOM_ARM": ["75101", "75102", "13201", "13202"],
            "nb_ls": [100, 300, 50, None],
            "loymoy": [8.0, 6.0, 5.0, 4.0],
        }
    )
    rents = institution.parse_rpls_rents(raw)
    commune_ze = pd.DataFrame({"code": ["75056", "13055"], "ze": ["1109", "9312"]})
    out = institution.social_rent_by_ze(rents, commune_ze)
    assert out["1109"] == pytest.approx((8 * 100 + 6 * 300) / 400)
    assert out["9312"] == pytest.approx(5.0)


def test_parse_rpls_rents_rejects_missing_column() -> None:
    """A sheet without the rent column is a definite reject."""
    with pytest.raises(institution.InstitutionError, match="loymoy"):
        institution.parse_rpls_rents(pd.DataFrame({"DEPCOM_ARM": ["01001"], "nb_ls": [1]}))


# ------------------------------------------------------------- M-A reference


def test_incentive_scenario_is_linear_and_capped() -> None:
    """Exits = stock × rate × years, capped at the whole stock."""
    out = institution.incentive_scenario(_detente(), _hypothesis("H-14", 0.75, 0.25, 2.5))
    assert out["gisement_effectif"] == 1900
    central_10 = out["central_10_ans"]
    assert isinstance(central_10, dict)
    assert central_10["sorties"] == round(1900 * 0.075)
    assert central_10["couverture_besoin"] == pytest.approx(1900 * 0.075 / 2000, abs=1e-3)
    # At the high rate over 20 years the first ZE saturates its NEED (1000),
    # not its stock (1500): exits are capped per ZE (HD-18).
    haut_20 = next(g for g in out["grille"] if g["taux"] == "haut" and g["horizon_ans"] == 20)
    assert haut_20["sorties"] == 750 + 200
    assert all(g["sorties"] <= 2000 for g in out["grille"])
    grid = out["grille"]
    assert isinstance(grid, list)
    assert all(g["part_gisement_pct"] <= 100 for g in grid)


# ------------------------------------------------------------- M-B operator


def _operator_inputs() -> dict[str, pd.Series]:
    idx = pd.Index(["0001", "0002"], name="ze")
    return {
        "reno_m2": pd.Series([600.0, 400.0], index=idx),
        "prix_m2": pd.Series([3_000.0, 1_000.0], index=idx),
        "marche": pd.Series([12.0, 9.0], index=idx),
        "social": pd.Series([6.0, 5.0], index=idx),
    }


def _run(
    discount: float = 1.0,
    reemploy: float = 10.0,
    rate: float = 2.3,
    years: float = 40,
    charges: float = 2_652.0,
) -> pd.DataFrame:
    i = _operator_inputs()
    return institution.operator_frame(
        _detente(),
        i["reno_m2"],
        i["prix_m2"],
        i["marche"],
        i["social"],
        discount,
        reemploy,
        rate,
        years,
        charges,
    )


def test_operator_frame_prices_both_segments_per_m2() -> None:
    """Acquisition/m² × (1 + remploi) + works/m², at the ZE surface; deficit at S-18."""
    frame = _run()
    surface_flat = remob.SURFACE_APPART_M2  # ZE 0001 is 100 % flats
    unit = (3_000.0 * 1.10 + 600.0) * surface_flat
    assert frame.loc["0001", "cout_unitaire_renove"] == pytest.approx(unit)
    assert frame.loc["0001", "investissement"] == pytest.approx(1000 * unit)
    unit_house = (1_000.0 * 1.10 + 400.0) * remob.SURFACE_MAISON_M2
    assert frame.loc["0002", "investissement"] == pytest.approx(
        400 * unit_house + 600 * remob.PRIX_REVIENT_NEUF_EUR_2023
    )
    af = institution.annuity_factor(2.3, 40)
    expected = ((3_000.0 * 1.10 + 600.0) * af + 2_652.0 / surface_flat) / 12
    assert frame.loc["0001", "loyer_equilibre_renove_m2"] == pytest.approx(expected)
    neuf = (2_550.0 * af + 2_652.0 / institution.SURFACE_NEUF_M2) / 12
    assert frame.loc["0001", "loyer_equilibre_neuf_m2"] == pytest.approx(neuf)
    # Subsidies: positive gap to the reference × surface × 12 × count; never negative.
    gap = expected - 6.0
    assert frame.loc["0001", "subvention_social_renove_eur_an"] == pytest.approx(
        gap * surface_flat * 12 * 1000
    )
    assert frame.loc["0001", "subvention_social_neuf_eur_an"] == 0.0
    assert (frame[[c for c in frame.columns if c.startswith("subvention_")]] >= 0).all().all()
    assert frame["subvention_social_eur_an"].sum() == pytest.approx(
        frame["subvention_social_renove_eur_an"].sum()
        + frame["subvention_social_neuf_eur_an"].sum()
    )


@given(discount=st.floats(min_value=0.1, max_value=1.0))
@settings(max_examples=50)
def test_operator_investment_is_monotone_in_discount(discount: float) -> None:
    """A lower acquisition price never raises the investment or the rent."""
    base, frame = _run(), _run(discount=discount)
    assert (frame["investissement"] <= base["investissement"] + 1e-6).all()
    assert (frame["loyer_equilibre_renove_m2"] <= base["loyer_equilibre_renove_m2"] + 1e-9).all()
    assert (frame["loyer_equilibre_neuf_m2"] == base["loyer_equilibre_neuf_m2"]).all()


def test_operator_rent_is_monotone_in_rate_years_and_charges() -> None:
    """Dearer money, shorter amortisation or higher charges never lower the rent."""
    base = _run()
    for frame in (_run(rate=3.6), _run(years=30), _run(charges=3_978.0), _run(reemploy=10.5)):
        assert (frame["loyer_equilibre_renove_m2"] >= base["loyer_equilibre_renove_m2"]).all()
    for frame in (_run(rate=1.5), _run(years=50), _run(charges=2_093.0), _run(reemploy=0.0)):
        assert (frame["loyer_equilibre_renove_m2"] <= base["loyer_equilibre_renove_m2"]).all()


def test_operator_summary_totals_and_counts() -> None:
    """National sums equal the per-ZE sums; ZE counts partition correctly."""
    frame = _run()
    summary = institution.operator_summary(frame, 500_000.0)
    assert summary["investissement_mdeur"] == round(float(frame["investissement"].sum()) / 1e9, 1)
    parts = (
        float(frame["cout_acquisition"].sum())
        + float(frame["cout_renovation"].sum())
        + float(frame["cout_neuf"].sum())
    )
    assert parts == pytest.approx(float(frame["investissement"].sum()))
    assert summary["n_ze"] == 2
    assert summary["n_ze_avec_loyers"] == 2
    assert summary["n_ze_sans_loyer_social"] == 0
    n_under = summary["n_ze_equilibre_renove_sous_marche"]
    assert isinstance(n_under, int) and 0 <= n_under <= 2
    with pytest.raises(institution.InstitutionError):
        institution.operator_summary(frame, 0.0)


def test_operator_summary_counts_ze_without_reference_rent() -> None:
    """A ZE without a social rent is counted out of the subsidy, never zeroed silently."""
    i = _operator_inputs()
    social = i["social"].copy()
    social.iloc[1] = float("nan")
    frame = institution.operator_frame(
        _detente(), i["reno_m2"], i["prix_m2"], i["marche"], social, 1.0, 10.0, 2.3, 40, 2_652.0
    )
    summary = institution.operator_summary(frame, 500_000.0)
    assert summary["n_ze_sans_loyer_social"] == 1
    assert summary["n_ze_avec_loyers"] == 1


def test_operator_scenario_sensitivity_orders() -> None:
    """The favourable corner is cheaper than the central, the unfavourable dearer."""
    i = _operator_inputs()
    out = institution.operator_scenario(
        _detente(),
        i["reno_m2"],
        i["prix_m2"],
        i["marche"],
        i["social"],
        500_000.0,
        _hypothesis("H-15", 1.0, 0.5, 1.0),
        _hypothesis("H-16", 2.3, 1.5, 3.6),
        _hypothesis("H-17", 40.0, 30.0, 50.0),
        _hypothesis("H-18", 2_652.0, 2_093.0, 3_978.0),
        _hypothesis("H-20", 10.0, 0.0, 10.5),
    )
    sens = out["sensibilite"]
    assert isinstance(sens, dict)
    central = out["central"]
    assert isinstance(central, dict)
    fav, unfav = sens["favorable"], sens["defavorable"]
    assert isinstance(fav, dict) and isinstance(unfav, dict)
    median = central["loyer_equilibre_renove_m2"]["median"]
    assert (
        fav["loyer_equilibre_renove_median_m2"] < median < unfav["loyer_equilibre_renove_median_m2"]
    )
    rythme = out["rythme_programme"]
    assert isinstance(rythme, list)
    assert rythme[0]["investissement_mdeur_an"] >= rythme[-1]["investissement_mdeur_an"]


# --------------------------------------------------------------- M-C lease


def test_lease_scenario_consent_grid() -> None:
    """Coverage grows with consent; full consent reaches the whole need."""
    i = _operator_inputs()
    out = institution.lease_scenario(
        _detente(), i["reno_m2"], i["marche"], i["social"], 2.3, 30.0, 2_652.0
    )
    grid = out["grille_consentement"]
    assert isinstance(grid, list)
    coverages = [g["couverture_besoin_avec_neuf"] for g in grid]
    assert coverages == sorted(coverages)
    assert grid[-1]["couverture_besoin_avec_neuf"] == pytest.approx(1.0)
    assert grid[-1]["couverture_besoin_bail_seul"] == pytest.approx(1400 / 2000)
    assert grid[-1]["logements_renoves"] == 1400
    assert out["duree_amortissement_ans"] == 30.0
    # TFPB exempt: the charges carried are the H-18 central minus the S-40 TFPB.
    assert out["charges_hors_tfpb_eur_logement_an"] == round(2_652.0 - 559.0)


# ---------------------------------------------------------- M-D toll shift


def test_toll_shift_break_even_years() -> None:
    """Years-equivalent = departmental duty / holding charge; perimeter partitions."""
    idx = pd.Index(["0001", "0002", "0003"], name="ze")
    prix = pd.DataFrame(
        {
            "prix_median": [200_000.0, 100_000.0, 300_000.0],
            "taux_dmto_pct": [5.00 * 1.0237 + 1.20, 4.50 * 1.0237 + 1.20, 5.00 * 1.0237 + 1.20],
            "n_ventes": [500, 100, 50],
        },
        index=idx,
    )
    nv = pd.Series([24_000.0, 20_000.0, 30_000.0], index=idx)
    names = pd.Series(["Alpha", "Beta", "Corsica"], index=idx)
    share = pd.Series([1.0, 0.8, 0.0], index=idx)
    out = institution.toll_shift_scenario(prix, nv, pd.Index(["0001"]), share, 34_565_110.0, names)
    charge = institution.DMTO_PRODUCT_EUR["2025"] / 34_565_110.0
    charges = out["charge_detention_eur_logement_an"]
    assert isinstance(charges, dict) and charges["2025"] == round(charge)
    top = out["bascule_la_plus_favorable_au_mobile"]
    assert isinstance(top, list)
    assert all(e["ze"] != "0003" for e in top)  # outside the perimeter: excluded
    alpha = next(e for e in top if e["ze"] == "0001")
    duty = 200_000 * 5.00 / 100  # total = 5.00 departmental × 1.0237 + 1.20 (H-13)
    assert alpha["droit_departemental_eur"] == round(duty)
    assert alpha["annees_equivalentes"] == round(duty / charge, 1)
    assert alpha["tendue"] is True
    assert out["n_ze_hors_perimetre"] == 1
    assert out["n_ze_perimetre_partiel"] == 1
    assert out["n_ze_tendues_dans_perimetre"] == 1
    # The residual toll is everything but the departmental duty.
    residual = out["peage_residuel_mois_niveau_vie"]
    assert isinstance(residual, dict) and residual["min"] > 0
    with pytest.raises(institution.InstitutionError):
        institution.holding_charge_eur_per_dwelling(1.0, 0.0)
