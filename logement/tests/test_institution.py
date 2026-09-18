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


def test_equilibrium_rent_covers_operating_costs() -> None:
    """At the S-40 structure, 43.8 € of annuity needs ~97 € of net rent."""
    assert institution.equilibrium_rent(43.8, 0.549) == pytest.approx(43.8 / 0.451)
    with pytest.raises(institution.InstitutionError):
        institution.equilibrium_rent(10.0, 1.0)


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
    grid = out["grille"]
    assert isinstance(grid, list)
    assert all(g["part_gisement_pct"] <= 100 for g in grid)


# ------------------------------------------------------------- M-B operator


def _operator_inputs() -> dict[str, pd.Series]:
    idx = pd.Index(["0001", "0002"], name="ze")
    return {
        "cu": pd.Series([40_000.0, 50_000.0], index=idx),
        "prix": pd.Series([200_000.0, 100_000.0], index=idx),
        "marche": pd.Series([12.0, 9.0], index=idx),
        "social": pd.Series([6.0, 5.0], index=idx),
        "nv": pd.Series([24_000.0, 20_000.0], index=idx),
    }


def test_operator_frame_prices_both_segments() -> None:
    """Acquisition at discount × price + works; deficit at the S-18 price."""
    i = _operator_inputs()
    frame = institution.operator_frame(
        _detente(), i["cu"], i["prix"], i["marche"], i["social"], i["nv"], 1.0, 2.3, 40, 0.549
    )
    assert frame.loc["0001", "investissement"] == pytest.approx(1000 * 240_000)
    assert frame.loc["0002", "investissement"] == pytest.approx(
        400 * 150_000 + 600 * remob.PRIX_REVIENT_NEUF_EUR_2023
    )
    af = institution.annuity_factor(2.3, 40)
    expected = 240_000 * af / (1 - 0.549) / 12 / remob.SURFACE_APPART_M2
    assert frame.loc["0001", "loyer_equilibre_renove_m2"] == pytest.approx(expected)
    # The subsidy is the positive gap to the social rent, over the surface and the count.
    gap = expected - 6.0
    assert frame.loc["0001", "subvention_renove_eur_an"] == pytest.approx(
        gap * remob.SURFACE_APPART_M2 * 12 * 1000
    )
    assert frame.loc["0001", "subvention_neuf_eur_an"] == 0.0


@given(discount=st.floats(min_value=0.1, max_value=1.0))
@settings(max_examples=50)
def test_operator_investment_is_monotone_in_discount(discount: float) -> None:
    """A lower acquisition price never raises the investment or the rent."""
    i = _operator_inputs()
    base = institution.operator_frame(
        _detente(), i["cu"], i["prix"], i["marche"], i["social"], i["nv"], 1.0, 2.3, 40, 0.549
    )
    frame = institution.operator_frame(
        _detente(), i["cu"], i["prix"], i["marche"], i["social"], i["nv"], discount, 2.3, 40, 0.549
    )
    assert (frame["investissement"] <= base["investissement"] + 1e-6).all()
    assert (frame["loyer_equilibre_renove_m2"] <= base["loyer_equilibre_renove_m2"] + 1e-9).all()
    assert (frame["loyer_equilibre_neuf_m2"] == base["loyer_equilibre_neuf_m2"]).all()


def test_operator_summary_totals_and_counts() -> None:
    """National sums equal the per-ZE sums; ZE counts partition correctly."""
    i = _operator_inputs()
    frame = institution.operator_frame(
        _detente(), i["cu"], i["prix"], i["marche"], i["social"], i["nv"], 1.0, 2.3, 40, 0.549
    )
    summary = institution.operator_summary(frame, 500_000.0)
    assert summary["investissement_mdeur"] == round(float(frame["investissement"].sum()) / 1e9, 1)
    assert summary["n_ze"] == 2
    assert summary["n_ze_avec_loyers"] == 2
    n_under = summary["n_ze_equilibre_renove_sous_marche"]
    assert isinstance(n_under, int) and 0 <= n_under <= 2
    with pytest.raises(institution.InstitutionError):
        institution.operator_summary(frame, 0.0)


def test_operator_scenario_sensitivity_orders() -> None:
    """The favourable corner is cheaper than the central, the unfavourable dearer."""
    i = _operator_inputs()
    out = institution.operator_scenario(
        _detente(),
        i["cu"],
        i["prix"],
        i["marche"],
        i["social"],
        i["nv"],
        500_000.0,
        _hypothesis("H-15", 1.0, 0.5, 1.0),
        _hypothesis("H-16", 2.3, 1.5, 2.81),
        _hypothesis("H-17", 40.0, 30.0, 50.0),
        _hypothesis("H-18", 0.549, 0.40, 0.60),
    )
    sens = out["sensibilite"]
    assert isinstance(sens, dict)
    central = out["central"]
    assert isinstance(central, dict)
    fav, unfav = sens["favorable"], sens["defavorable"]
    assert isinstance(fav, dict) and isinstance(unfav, dict)
    assert fav["loyer_equilibre_renove_median_m2"] < central["loyer_equilibre_renove_m2"]["median"]
    assert (
        unfav["loyer_equilibre_renove_median_m2"] > central["loyer_equilibre_renove_m2"]["median"]
    )


# --------------------------------------------------------------- M-C lease


def test_lease_scenario_consent_grid() -> None:
    """Coverage grows with consent; full consent reaches the whole need."""
    i = _operator_inputs()
    out = institution.lease_scenario(_detente(), i["cu"], i["marche"], i["social"], 2.3, 0.549)
    grid = out["grille_consentement"]
    assert isinstance(grid, list)
    coverages = [g["couverture_besoin"] for g in grid]
    assert coverages == sorted(coverages)
    assert grid[-1]["couverture_besoin"] == pytest.approx(1.0)
    assert grid[-1]["logements_renoves"] == 1400
    assert out["duree_amortissement_ans"] == institution.BAR_AMORTISATION_YEARS


# ---------------------------------------------------------- M-D toll shift


def test_toll_shift_break_even_years() -> None:
    """Years-equivalent = fiscal toll / holding charge; tense flag partitions."""
    idx = pd.Index(["0001", "0002"], name="ze")
    prix = pd.DataFrame(
        {"prix_median": [200_000.0, 100_000.0], "taux_dmto_pct": [6.32, 5.81]}, index=idx
    )
    nv = pd.Series([24_000.0, 20_000.0], index=idx)
    names = pd.Series(["Alpha", "Beta"], index=idx)
    out = institution.toll_shift_scenario(prix, nv, pd.Index(["0001"]), 34_565_110.0, names)
    charge = institution.DMTO_PRODUCT_2024_EUR / 34_565_110.0
    assert out["charge_detention_eur_logement_an"] == round(charge)
    top = out["bascule_la_plus_favorable_au_mobile"]
    assert isinstance(top, list)
    alpha = next(e for e in top if e["ze"] == "0001")
    expected_toll = 200_000 * 0.0632 + 200.0
    assert alpha["peage_fiscal_eur"] == round(expected_toll)
    assert alpha["annees_equivalentes"] == round(expected_toll / charge, 1)
    assert alpha["tendue"] is True
    assert out["n_ze_tendues"] == 1
    with pytest.raises(institution.InstitutionError):
        institution.holding_charge_eur_per_dwelling(1.0, 0.0)
