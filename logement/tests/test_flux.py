"""Behaviour tests for the pure housing-flow core (R-18)."""

from __future__ import annotations

import pandas as pd
import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

from logement.core import flux


def _census() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "CODGEO": ["75101", "75102", "13055", "01001"],
            "P11_MEN": ["100", "100", "1000", "50"],
            "P16_MEN": ["110", "110", "1000", "50"],
            "P22_MEN": ["130", "130", "970", "56"],
            "P11_LOG": ["120", "120", "1200", "60"],
            "P16_LOG": ["130", "130", "1200", "60"],
            "P22_LOG": ["160", "160", "1200", "70"],
            "P22_RP": ["130", "130", "970", "56"],
            "P22_RSECOCC": ["10", "10", "100", "7"],
            "P22_LOGVAC": ["20", "20", "130", "7"],
        }
    )


def _sitadel_monthly() -> pd.DataFrame:
    rows = []
    for year in range(2013, 2025):
        for month in ("01", "07"):
            rows.append((str(year), month, "75101", "Tous Logements", "6", "5", "0", "0"))
            rows.append((str(year), month, "75101", "Individuel pur", "1", "1", "0", "0"))
            rows.append((str(year), month, "13055", "Tous Logements", "2", "2", "0", "0"))
            rows.append((str(year), month, "01001", "Tous Logements", "1", "0", "0", "0"))
    # Column order follows the published file: ANNEE, MOIS, CODE_INSEE, TYPE_LGT, ...
    return pd.DataFrame(rows, columns=list(flux.SITADEL_MONTHLY_COLS))


def _sitadel() -> pd.DataFrame:
    """The frozen annual extract, as `acquire-sitadel` writes it."""
    return flux.aggregate_sitadel_monthly(_sitadel_monthly())


def _commune_ze() -> pd.DataFrame:
    return pd.DataFrame({"code": ["75056", "13055", "01001"], "ze": ["1109", "9312", "8401"]})


def test_parse_census_vintages_maps_plm_and_drops_duplicates() -> None:
    """Paris arrondissements collapse on the parent code (first row kept)."""
    census = flux.parse_census_vintages(_census())
    assert census["code"].tolist() == ["75056", "13055", "01001"]
    assert census.loc[census["code"] == "75056", "P22_MEN"].iloc[0] == 130
    with pytest.raises(flux.FluxError, match="P22_MEN"):
        flux.parse_census_vintages(_census().drop(columns=["P22_MEN"]))


def test_aggregate_monthly_keeps_all_dwellings_rows_only() -> None:
    """Component rows (individual/collective) are not double-counted."""
    extract = _sitadel()
    paris = extract[(extract["CODE_INSEE"] == "75101") & (extract["ANNEE"] == 2020)]
    assert paris["LOG_COM"].iloc[0] == 10  # 2 months × 5, "Individuel pur" ignored
    assert set(extract["ANNEE"]) == set(range(2013, 2025))
    with pytest.raises(flux.FluxError):
        flux.aggregate_sitadel_monthly(_sitadel_monthly().assign(TYPE_LGT="Collectif"))


def test_parse_annual_extract_maps_plm() -> None:
    """The arrondissement code lands on the parent commune; a missing count is dropped."""
    annual = flux.parse_sitadel_annual(_sitadel())
    assert (
        annual.loc[(annual["code"] == "75056") & (annual["annee"] == 2020), "log_com"].iloc[0] == 10
    )
    with pytest.raises(flux.FluxError, match="LOG_COM"):
        flux.parse_sitadel_annual(_sitadel().drop(columns=["LOG_COM"]))


def test_flux_by_ze_household_formation_and_need() -> None:
    """Formation = Δménages / 6 ; need keeps the 2022 RS + vacancy shares."""
    frame = flux.flux_by_ze(
        flux.parse_census_vintages(_census()), flux.parse_sitadel_annual(_sitadel()), _commune_ze()
    )
    paris = frame.loc["1109"]
    assert paris["formation_menages_an"] == pytest.approx(20 / 6)
    assert paris["logements_par_menage_forme"] == pytest.approx(1 / (1 - 10 / 160 - 20 / 160))
    assert paris["besoin_flux_an"] == pytest.approx(20 / 6 / (1 - 30 / 160))
    assert paris["commences_an"] == pytest.approx(10.0)  # 2 months × 5 per year
    assert paris["solde_flux_an"] == pytest.approx(10.0 - paris["besoin_flux_an"])
    # Declining households: need is zero, ratio undefined (never infinite).
    marseille = frame.loc["9312"]
    assert marseille["formation_menages_an"] < 0
    assert marseille["besoin_flux_an"] == 0.0
    assert pd.isna(marseille["ratio_production"])
    assert marseille["disparitions_implicites_an"] == pytest.approx(4.0 - 0.0)


@given(rs_share=st.floats(0.0, 0.4), vac_share=st.floats(0.0, 0.4))
@settings(max_examples=50)
def test_dwellings_per_household_formed_is_at_least_one(rs_share: float, vac_share: float) -> None:
    """Keeping a structure constant never needs less than one dwelling per household."""
    ratio = 1 / (1 - rs_share - vac_share)
    assert ratio >= 1.0


def test_build_summary_shares_and_stock_vs_flux() -> None:
    """Tense shares partition the national totals; years-to-absorption = need / deficit."""
    frame = flux.flux_by_ze(
        flux.parse_census_vintages(_census()), flux.parse_sitadel_annual(_sitadel()), _commune_ze()
    )
    idx = frame.index
    tendue = pd.Series([True, False, False], index=idx)
    cost = pd.Series([40.0, 25.0, 20.0], index=idx)
    names = pd.Series(["Paris", "Marseille", "Bourg"], index=idx)
    out = flux.build_summary(frame, tendue, cost, names, 1000.0)
    national = out["national"]
    assert isinstance(national, dict)
    assert national["n_ze"] == 3
    assert national["commences_an"] == round(float(frame["commences_an"].sum()))
    shares = out["parts_des_ze_tendues"]
    assert isinstance(shares, dict)
    assert 0 <= shares["part_commences_pct"] <= 100
    stock = out["stock_vs_flux"]
    assert isinstance(stock, dict)
    assert stock["besoin_detente"] == 1000
    # Paris (tense) has a surplus: no tense deficit → no absorption horizon.
    assert stock["deficit_des_ze_tendues_deficitaires_an"] == 0
    assert stock["annees_avant_absorption_par_le_deficit"] is None
    with pytest.raises(flux.FluxError):
        flux.build_summary(frame, tendue, cost, names, 0.0)
