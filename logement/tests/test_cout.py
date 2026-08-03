"""Behaviour tests for the pure cost core (rents, Filosofi, cost index)."""

from __future__ import annotations

import pandas as pd
import pytest

from logement.core import cout


def test_parse_loyers_handles_commas_and_plm() -> None:
    """French decimals parse; PLM arrondissements average into the parent commune."""
    raw = pd.DataFrame(
        {"INSEE_C": ["75101", "75102", "33063"], "loypredm2": ["30,0", "20,0", "12,5"]}
    )
    out = cout.parse_loyers(raw).set_index("code")
    assert out.loc["75056", "loyer_m2"] == pytest.approx(25.0)
    assert out.loc["33063", "loyer_m2"] == pytest.approx(12.5)


def test_parse_filosofi_filters_level_and_measure() -> None:
    """Only the requested GEO_OBJECT/measure rows survive, numeric and indexed."""
    raw = pd.DataFrame(
        {
            "GEO": ["1109", "1109", "75056"],
            "GEO_OBJECT": ["ZE2020", "ZE2020", "COM"],
            "FILOSOFI_MEASURE": ["MED_SL", "NUM_PER", "MED_SL"],
            "OBS_VALUE": ["25510", "12", "28000"],
        }
    )
    series = cout.parse_filosofi(raw, geo_object="ZE2020", measure="MED_SL")
    assert series.to_dict() == {"1109": 25510.0}
    with pytest.raises(cout.CoutError, match="no Filosofi rows"):
        cout.parse_filosofi(raw, geo_object="BV2022", measure="MED_SL")


def _cost_frame() -> pd.DataFrame:
    loyers = pd.DataFrame({"code": ["00001", "00002"], "loyer_m2": [10.0, 20.0]})
    lovac = pd.DataFrame(
        {
            "code": ["00001", "00002"],
            "pp_vacant_plus_2ans_2024": [10.0, 20.0],
            "ff_pp_total_2024": [100.0, 300.0],
        }
    )
    commune_ze = pd.DataFrame({"code": ["00001", "00002"], "ze": ["0001", "0001"]})
    niveau_vie = pd.Series({"0001": 24000.0})
    return cout.cost_index_by_ze(loyers, lovac, commune_ze, niveau_vie)


def test_cost_index_weights_rent_by_stock() -> None:
    """The ZE rent is the stock-weighted mean and the index uses annual rent."""
    frame = _cost_frame()
    weighted = (10.0 * 100 + 20.0 * 300) / 400
    assert frame.loc["0001", "loyer_m2"] == pytest.approx(weighted)
    assert frame.loc["0001", "indice_cout_pct"] == pytest.approx(weighted * 12 / 24000 * 100)
    assert frame.loc["0001", "taux_structurelle_pct"] == pytest.approx(30 / 400 * 100)


def test_build_summary_shape() -> None:
    """The R-04 payload carries the correlation, halves and extreme lists."""
    frame = pd.concat(
        [
            _cost_frame(),
            _cost_frame()
            .rename(index={"0001": "0002"})
            .assign(indice_cout_pct=0.2, taux_structurelle_pct=12.0),
        ]
    )
    summary = cout.build_summary(frame, pd.Series({"0001": "Alpha", "0002": "Beta"}))
    assert summary["n_ze"] == 2
    assert -1 <= summary["spearman_cost_vs_vacancy"] <= 1
    top = summary["top_cost_index"]
    assert isinstance(top, list) and top[0]["name"] == "Alpha"
