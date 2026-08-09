"""Behaviour tests for the pure effort core (census mix, households, effort rate)."""

from __future__ import annotations

import pandas as pd
import pytest

from logement.core import effort
from logement.models import HypothesisRecord


def test_parse_census_mix_sums_plm_into_parent() -> None:
    """PLM arrondissement counts add up into the parent commune."""
    raw = pd.DataFrame(
        {
            "CODGEO": ["75101", "75102", "33063"],
            "P22_RPMAISON": ["10", "20", "5"],
            "P22_RPAPPART": ["100", "200", "50"],
        }
    )
    out = effort.parse_census_mix(raw).set_index("code")
    assert out.loc["75056", "rp_maison"] == pytest.approx(30.0)
    assert out.loc["75056", "rp_appart"] == pytest.approx(300.0)
    assert out.loc["33063", "rp_maison"] == pytest.approx(5.0)


def test_parse_census_mix_requires_columns() -> None:
    """A missing census column is a definite reject, not a silent skip."""
    with pytest.raises(effort.EffortError, match="missing census column"):
        effort.parse_census_mix(pd.DataFrame({"CODGEO": ["33063"]}))


def test_household_frame_computes_observed_ratio() -> None:
    """persons/UC is the observed Filosofi ratio, joined on common ZE only."""
    frame = effort.household_frame(
        pd.Series({"0001": 20000.0, "0002": 24000.0}),
        pd.Series({"0001": 300.0}),
        pd.Series({"0001": 200.0}),
    )
    assert list(frame.index) == ["0001"]
    assert frame.loc["0001", "pers_per_uc"] == pytest.approx(1.5)


def test_household_frame_rejects_non_positive_units() -> None:
    """Zero consumption units cannot silently produce an infinite ratio."""
    with pytest.raises(effort.EffortError, match="non-positive"):
        effort.household_frame(
            pd.Series({"0001": 20000.0}),
            pd.Series({"0001": 300.0}),
            pd.Series({"0001": 0.0}),
        )


def _h07(central: float = 50.0) -> HypothesisRecord:
    return HypothesisRecord(
        id="H-07",
        name="relocation_surface_per_person_m2",
        description="test",
        central_value=central,
        plausible_range=(35.0, 71.0),
        unit="m2_per_person",
        confidence="medium",
    )


def _effort_frame(surface: float = 50.0) -> pd.DataFrame:
    loyers_appart = pd.DataFrame({"code": ["00001", "00002"], "loyer_m2": [10.0, 20.0]})
    loyers_maison = pd.DataFrame({"code": ["00001", "00002"], "loyer_m2": [8.0, 16.0]})
    census_mix = pd.DataFrame(
        {"code": ["00001", "00002"], "rp_maison": [75.0, 25.0], "rp_appart": [25.0, 75.0]}
    )
    lovac = pd.DataFrame(
        {
            "code": ["00001", "00002"],
            "pp_vacant_plus_2ans_2024": [10.0, 20.0],
            "ff_pp_total_2024": [100.0, 300.0],
        }
    )
    commune_ze = pd.DataFrame({"code": ["00001", "00002"], "ze": ["0001", "0001"]})
    households = pd.DataFrame(
        {"niveau_vie_median": [24000.0], "pers_per_uc": [1.5]}, index=["0001"]
    )
    return effort.effort_by_ze(
        loyers_appart, loyers_maison, census_mix, lovac, commune_ze, households, surface
    )


def test_effort_by_ze_mixes_rents_and_scales_by_household() -> None:
    """Rent mix follows the RP composition; effort uses surface × persons/UC."""
    frame = _effort_frame()
    appart = (10.0 * 100 + 20.0 * 300) / 400
    maison = (8.0 * 100 + 16.0 * 300) / 400
    part_maison = 100.0 / 200.0
    mix = part_maison * maison + (1 - part_maison) * appart
    surface_per_uc = 50.0 * 1.5
    assert frame.loc["0001", "loyer_mix_m2"] == pytest.approx(mix)
    assert frame.loc["0001", "effort_brut_pct"] == pytest.approx(
        12 * mix * surface_per_uc / 24000.0 * 100
    )
    assert frame.loc["0001", "effort_appart_pct"] == pytest.approx(
        12 * appart * surface_per_uc / 24000.0 * 100
    )
    assert frame.loc["0001", "taux_structurelle_pct"] == pytest.approx(30 / 400 * 100)


def test_effort_is_linear_in_surface() -> None:
    """Doubling H-07 doubles every effort rate (ranking invariance)."""
    base, doubled = _effort_frame(50.0), _effort_frame(100.0)
    assert doubled["effort_brut_pct"].equals(base["effort_brut_pct"] * 2)


def test_effort_by_ze_keeps_secret_vacancy_missing() -> None:
    """An all-secret ZE keeps NaN vacancy (min_count), never a silent zero."""
    loyers = pd.DataFrame({"code": ["00001"], "loyer_m2": [10.0]})
    census_mix = pd.DataFrame({"code": ["00001"], "rp_maison": [50.0], "rp_appart": [50.0]})
    lovac = pd.DataFrame(
        {
            "code": ["00001"],
            "pp_vacant_plus_2ans_2024": [float("nan")],
            "ff_pp_total_2024": [100.0],
        }
    )
    commune_ze = pd.DataFrame({"code": ["00001"], "ze": ["0001"]})
    households = pd.DataFrame(
        {"niveau_vie_median": [24000.0], "pers_per_uc": [1.5]}, index=["0001"]
    )
    frame = effort.effort_by_ze(loyers, loyers, census_mix, lovac, commune_ze, households, 50.0)
    assert pd.isna(frame.loc["0001", "taux_structurelle_pct"])


def test_build_summary_shape_and_range_scaling() -> None:
    """The R-06 payload carries the H-07 sensitivity as a linear rescale."""
    frame = pd.concat(
        [
            _effort_frame(),
            _effort_frame()
            .rename(index={"0001": "0002"})
            .assign(effort_brut_pct=80.0, taux_structurelle_pct=1.0),
        ]
    )
    summary = effort.build_summary(frame, pd.Series({"0001": "Alpha", "0002": "Beta"}), _h07())
    assert summary["n_ze"] == 2
    assert -1 <= summary["spearman_effort_vs_vacancy"] <= 1
    top = summary["top_effort"]
    assert isinstance(top, list) and top[0]["name"] == "Beta"
    low, high = top[0]["effort_range_pct"]
    assert low == pytest.approx(80.0 * 35.0 / 50.0, abs=0.05)
    assert high == pytest.approx(80.0 * 71.0 / 50.0, abs=0.05)
    medians = summary["median_effort_by_h07_pct"]
    assert medians["low"] <= medians["central"] <= medians["high"]
