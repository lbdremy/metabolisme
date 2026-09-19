"""Behaviour tests for the pure housing-flow core (R-18, post-review API)."""

from __future__ import annotations

import pandas as pd
import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

from logement.core import flux
from logement.models import HypothesisRecord


def _census() -> pd.DataFrame:
    cols = {
        "CODGEO": ["75056", "75101", "13055", "01001"],
        "P11_MEN": ["100", "50", "1000", "50"],
        "P16_MEN": ["110", "55", "1000", "50"],
        "P22_MEN": ["130", "65", "970", "56"],
        "P11_LOG": ["120", "60", "1200", "60"],
        "P16_LOG": ["130", "65", "1200", "60"],
        "P22_LOG": ["160", "80", "1200", "70"],
        "P22_RP": ["130", "65", "970", "56"],
        "P16_RP": ["110", "55", "1000", "50"],
        "P22_RSECOCC": ["10", "5", "100", "7"],
        "P16_RSECOCC": ["4", "2", "90", "5"],
        "P22_LOGVAC": ["20", "10", "130", "7"],
        "P16_LOGVAC": ["16", "8", "110", "5"],
    }
    return pd.DataFrame(cols)


def _sitadel_real_date() -> pd.DataFrame:
    """The S-56 layout: ANNEE, COMM, TYPE_LGT…, Paris parent AND arrondissement."""
    rows = []
    for year in range(2013, 2026):
        com = "" if year == 2025 else "10"
        rows.append((str(year), "75056", "Tous Logements", "12", com, "0", "0"))
        rows.append((str(year), "75101", "Tous Logements", "6", "5", "0", "0"))
        rows.append((str(year), "75056", "Individuel pur", "1", "1", "0", "0"))
        rows.append((str(year), "13055", "Tous Logements", "2", "2", "0", "0"))
        rows.append((str(year), "01001", "Tous Logements", "1", "0", "0", "0"))
        rows.append((str(year), "01999", "Tous Logements", "3", "3", "0", "0"))  # merged commune
    return pd.DataFrame(
        rows, columns=["ANNEE", "COMM", "TYPE_LGT", "LOG_AUT", "LOG_COM", "SDP_AUT", "SDP_COM"]
    )


def _commune_ze() -> pd.DataFrame:
    return pd.DataFrame({"code": ["75056", "13055", "01001"], "ze": ["1109", "9312", "8401"]})


def _h21() -> HypothesisRecord:
    return HypothesisRecord(
        id="H-21",
        name="t",
        description="t",
        central_value=1.155,
        plausible_range=(1.122, 1.235),
        unit="factor",
        confidence="medium",
    )


def test_parse_census_vintages_keeps_parent_row() -> None:
    """Paris parent row is kept, its arrondissement dropped (never summed twice)."""
    census = flux.parse_census_vintages(_census())
    assert census["code"].tolist() == ["75056", "13055", "01001"]
    assert census.loc[census["code"] == "75056", "P22_MEN"].iloc[0] == 130
    with pytest.raises(flux.FluxError, match="P16_RSECOCC"):
        flux.parse_census_vintages(_census().drop(columns=["P16_RSECOCC"]))


def test_parse_real_date_series_drops_arrondissements_and_missing_counts() -> None:
    """S-56 lists Paris twice: the parent wins; 2025 (no starts) is dropped."""
    annual = flux.parse_sitadel_annual(_sitadel_real_date(), code_col="COMM")
    paris = annual[annual["code"] == "75056"]
    assert paris.loc[paris["annee"] == 2020, "log_com"].iloc[0] == 10  # not 10 + 5
    assert 2025 not in set(paris["annee"])  # LOG_COM empty → dropped, not zero
    assert 2025 in set(annual.loc[annual["code"] == "13055", "annee"])


def test_cog_successor_map_and_remap_counts_lost_starts() -> None:
    """A merged code follows the movements table; an unknown code is counted, not dropped."""
    mvt = pd.DataFrame(
        {
            "MOD": ["32", "10", "32"],
            "COM_AV": ["01999", "01001", "01998"],
            "COM_AP": ["01001", "01001", "01997"],
            "TYPECOM_AP": ["COM", "COM", "COM"],
        }
    )
    successors = flux.cog_successor_map(mvt)
    assert successors == {"01999": "01001", "01998": "01997"}
    annual = flux.parse_sitadel_annual(_sitadel_real_date(), code_col="COMM")
    remapped, report = flux.remap_to_membership(annual, set(_commune_ze()["code"]), successors)
    bourg = remapped[(remapped["code"] == "01001") & (remapped["annee"] == 2020)]
    assert bourg["log_com"].iloc[0] == 3  # 0 own + 3 from the merged commune
    assert report["codes_remappes"] == 1
    assert report["codes_sans_ze"] == 0


def test_undercount_ratios_and_national_series() -> None:
    """Ratio = estimated / communal per common closed year."""
    national = pd.DataFrame(
        {
            "ANNEE": ["2020", "2020", "2021"],
            "MOIS": ["01", "01", "01"],
            "TYPE_LGT": ["Tous Logements", "Tous Logements", "Tous Logements"],
            "NAT_SERIES": ["Brute", "CVS-CJO", "Brute"],
            "LOG_COM": ["115", "110", "120"],
        }
    )
    estimated = flux.parse_national_estimated(national)
    assert estimated.to_dict() == {2020: 115.0, 2021: 120.0}
    communal = pd.DataFrame(
        {"code": ["a", "b"], "annee": [2020, 2020], "log_com": [60.0, 40.0], "log_aut": [0, 0]}
    )
    ratios = flux.undercount_ratios(estimated, communal)
    assert ratios.to_dict() == {2020: pytest.approx(1.15)}


def _frame() -> pd.DataFrame:
    annual = flux.parse_sitadel_annual(_sitadel_real_date(), code_col="COMM")
    by_year = flux.starts_by_ze_year(annual, _commune_ze())
    return flux.flux_by_ze(flux.parse_census_vintages(_census()), by_year, _commune_ze(), 1.155)


def test_flux_by_ze_formation_decomposition_and_three_needs() -> None:
    """Formation = Δménages / 6 ; the three affectations order the needs."""
    frame = _frame()
    paris = frame.loc["1109"]
    assert paris["formation_menages_an"] == pytest.approx(20 / 6)
    assert paris["croissance_parc_an"] == pytest.approx(30 / 6)
    assert paris["croissance_rs_an"] == pytest.approx(6 / 6)
    assert paris["part_rs_neuf_observee"] == pytest.approx(6 / 30)
    vac = 20 / 160
    assert paris["besoin_sans_rs_an"] == pytest.approx(20 / 6 / (1 - vac))
    assert paris["besoin_rs_observee_an"] == pytest.approx(20 / 6 / (1 - 0.2 - vac))
    assert paris["besoin_structure_2022_an"] == pytest.approx(20 / 6 / (1 - 10 / 160 - vac))
    assert paris["besoin_sans_rs_an"] <= paris["besoin_flux_an"]
    assert paris["commences_an"] == pytest.approx(10.0)
    assert paris["commences_estimes_an"] == pytest.approx(11.55)
    assert paris["solde_estime_an"] == pytest.approx(11.55 - paris["besoin_flux_an"])
    assert paris["commences_2023"] == 10.0 and paris["commences_2024"] == 10.0
    # Declining households: zero need, undefined ratio (never infinite).
    marseille = frame.loc["9312"]
    assert marseille["besoin_flux_an"] == 0.0
    assert pd.isna(marseille["ratio_estime"])
    with pytest.raises(flux.FluxError):
        flux.flux_by_ze(
            flux.parse_census_vintages(_census()),
            flux.starts_by_ze_year(
                flux.parse_sitadel_annual(_sitadel_real_date(), code_col="COMM"), _commune_ze()
            ),
            _commune_ze(),
            0.9,
        )


@given(rs_share=st.floats(0.0, 0.5), vac_share=st.floats(0.0, 0.4))
@settings(max_examples=50)
def test_dwellings_per_household_formed_is_at_least_one(rs_share: float, vac_share: float) -> None:
    """Keeping a structure constant never needs less than one dwelling per household."""
    assert 1 / (1 - rs_share - vac_share) >= 1.0


def test_build_summary_partitions_and_per_ze_absorption() -> None:
    """Tense + others = national; per-ZE absorption = need / own deficit."""
    frame = _frame()
    tendue = pd.Series({"1109": True, "9312": False, "8401": True})
    cost = pd.Series({"1109": 40.0, "9312": 25.0, "8401": 20.0})
    names = pd.Series({"1109": "Paris", "9312": "Marseille", "8401": "Bourg"})
    need = pd.Series([100.0, 50.0], index=pd.Index(["1109", "8401"]))
    yearly = {
        "communal_declare_france": pd.Series({2020: 12.0}),
        "ratio_x": pd.Series({2020: 1.1234}),
    }
    out = flux.build_summary(frame, tendue, cost, names, need, _h21(), yearly, {"codes_sans_ze": 0})
    national, tense, others = out["national"], out["tendues"], out["autres"]
    assert isinstance(national, dict) and isinstance(tense, dict) and isinstance(others, dict)
    assert (
        national["commences_estimes_an"]
        == tense["commences_estimes_an"] + others["commences_estimes_an"]
    )
    assert national["n_ze"] == tense["n_ze"] + others["n_ze"]
    series = out["series_annuelles"]
    assert isinstance(series, dict)
    assert series["ratio_x"]["2020"] == 1.123  # ratios keep three decimals
    stock = out["stock_vs_flux"]
    assert isinstance(stock, dict)
    assert stock["besoin_detente_tendues"] == 150
    block = stock["fenetre_2017_2022"]
    assert isinstance(block, dict)
    # Bourg (tense) has a deficit: its own need / its own deficit.
    bourg = frame.loc["8401"]
    if bourg["solde_estime_an"] < 0:
        assert block["n_ze"] >= 1
        assert block["annees_agregees"] is not None
    fen = out["fenetres_sensibilite"]
    assert isinstance(fen, dict) and set(fen) == {
        "2015-2020",
        "2017-2022",
        "2018-2023",
        "2019-2024",
    }
