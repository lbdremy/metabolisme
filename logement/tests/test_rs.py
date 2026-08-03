"""Behaviour tests for the pure secondary-residences core."""

from __future__ import annotations

import pandas as pd
import pytest

from logement.core import rs


def test_parse_census_housing_deduplicates_plm() -> None:
    """Arrondissement rows collapse into the parent commune row (kept first)."""
    raw = pd.DataFrame(
        {
            "CODGEO": ["75056", "75101", "33063"],
            "P22_LOG": ["100", "10", "50"],
            "P22_RP": ["80", "8", "40"],
            "P22_RSECOCC": ["5", "1", "5"],
            "P22_LOGVAC": ["15", "1", "5"],
        }
    )
    out = rs.parse_census_housing(raw).set_index("code")
    assert len(out) == 2
    assert out.loc["75056", "P22_LOG"] == 100  # parent totals kept, not the arrondissement


def test_rs_by_ze_shares() -> None:
    """Counts aggregate by ZE and shares derive from the totals."""
    census = pd.DataFrame(
        {
            "code": ["00001", "00002"],
            "P22_LOG": [100.0, 100.0],
            "P22_RP": [60.0, 90.0],
            "P22_RSECOCC": [30.0, 5.0],
            "P22_LOGVAC": [10.0, 5.0],
        }
    )
    commune_ze = pd.DataFrame({"code": ["00001", "00002"], "ze": ["0001", "0001"]})
    out = rs.rs_by_ze(census, commune_ze)
    assert out.loc["0001", "part_rs_pct"] == pytest.approx(17.5)
    assert out.loc["0001", "part_vac_rp_pct"] == pytest.approx(7.5)
    with pytest.raises(rs.RsError, match="no commune joined"):
        rs.rs_by_ze(census, pd.DataFrame({"code": ["99999"], "ze": ["0002"]}))


def test_build_summary_flags_touristic_and_outliers() -> None:
    """The R-05 payload separates touristic ZE and RS+vacancy outliers."""
    rs_ze = pd.DataFrame(
        {
            "P22_LOG": [100.0, 100.0],
            "P22_RP": [50.0, 90.0],
            "P22_RSECOCC": [40.0, 5.0],
            "P22_LOGVAC": [10.0, 5.0],
            "part_rs_pct": [40.0, 5.0],
            "part_vac_rp_pct": [10.0, 5.0],
        },
        index=pd.Index(["0001", "0002"], name="ze"),
    )
    cost_ze = pd.DataFrame(
        {"indice_cout_pct": [0.9, 0.5], "taux_structurelle_pct": [6.0, 2.0]},
        index=pd.Index(["0001", "0002"], name="ze"),
    )
    summary = rs.build_summary(rs_ze, cost_ze, pd.Series({"0001": "Tour", "0002": "Ville"}))
    touristic = summary["touristic_ze"]
    assert isinstance(touristic, dict) and touristic["n"] == 1
    outliers = summary["rs_and_vacancy_outliers"]
    assert isinstance(outliers, list)
    assert [o["name"] for o in outliers] == ["Tour"]
    assert summary["national_rs_share_pct"] == pytest.approx(22.5)
