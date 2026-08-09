"""Behaviour tests for the pure ZE-cross core (membership, employment, join)."""

from __future__ import annotations

import pandas as pd
import pytest

from logement.core import ze


def test_parse_commune_ze_strips_and_drops_incomplete() -> None:
    """Membership rows become a clean code -> ZE frame."""
    raw = pd.DataFrame({"CODGEO": [" 01001 ", "01002", None], "ZE2020": ["8405", None, "8405"]})
    out = ze.parse_commune_ze(raw)
    assert out.to_dict("records") == [{"code": "01001", "ze": "8405"}]


def test_parse_commune_ze_requires_columns() -> None:
    """A sheet without CODGEO/ZE2020 is a loud error."""
    with pytest.raises(ze.ZeError, match="missing membership column"):
        ze.parse_commune_ze(pd.DataFrame({"CODGEO": ["01001"]}))


def test_parse_emploi_ze_extracts_codes_and_growth() -> None:
    """'0051 - Alençon' splits into code/name; growth is the 20-year mean rate."""
    raw = pd.DataFrame(
        {
            "Zone d'emploi": ["0051 - Alençon", "not a zone"],
            "Région": ["00 - Interrégional", ""],
            "1998": [50116, None],
            "2018": [46340, None],
        }
    )
    out = ze.parse_emploi_ze(raw)
    assert list(out.index) == ["0051"]
    assert out.loc["0051", "ze_name"] == "Alençon"
    expected = ((46340 / 50116) ** (1 / 20) - 1) * 100
    assert out.loc["0051", "growth_pct_per_year"] == pytest.approx(expected)


def test_aggregate_vacancy_by_ze_maps_plm_and_reports_unmatched() -> None:
    """Arrondissements aggregate into their parent's ZE; orphans are reported."""
    lovac_communes = pd.DataFrame(
        {
            "code": ["75101", "75102", "99999"],
            "pp_vacant_plus_2ans_2024": [100.0, 50.0, 10.0],
            "ff_pp_total_2024": [1000.0, 500.0, 100.0],
        }
    )
    commune_ze = pd.DataFrame({"code": ["75056"], "ze": ["1109"]})
    per_ze, unmatched = ze.aggregate_vacancy_by_ze(lovac_communes, commune_ze)
    assert unmatched == ["99999"]
    assert per_ze.loc["1109", "structural"] == 150.0
    assert per_ze.loc["1109", "structural_rate_pct"] == pytest.approx(10.0)


def test_build_summary_shape_and_shares() -> None:
    """The R-03 payload carries coherent shares between declining and growing ZE."""
    vacancy = pd.DataFrame(
        {
            "structural": [100.0, 300.0],
            "private_stock": [1000.0, 10000.0],
            "n_communes_masquees": [2, 0],
        },
        index=pd.Index(["0001", "0002"], name="ze"),
    )
    vacancy["structural_rate_pct"] = vacancy["structural"] / vacancy["private_stock"] * 100
    emploi = pd.DataFrame(
        {
            "ze_name": ["Declin", "Croissance"],
            "emploi_start": [1000.0, 1000.0],
            "emploi_end": [900.0, 1200.0],
            "growth_pct_per_year": [-0.5, 0.9],
        },
        index=pd.Index(["0001", "0002"], name="ze_code"),
    )
    summary = ze.build_summary(vacancy, emploi, unmatched=["97127"])
    assert summary["n_ze"] == 2
    declining = summary["declining_ze"]
    assert isinstance(declining, dict)
    assert declining["n"] == 1
    assert declining["structural_share_pct"] == pytest.approx(25.0)
    assert summary["unmatched_communes"] == ["97127"]
    assert -1 <= summary["spearman_rate_vs_growth"] <= 1


def test_build_summary_rejects_empty_join() -> None:
    """Disjoint vacancy/employment indexes raise instead of returning nonsense."""
    vacancy = pd.DataFrame(
        {"structural": [1.0], "private_stock": [10.0], "structural_rate_pct": [10.0]},
        index=pd.Index(["0001"], name="ze"),
    )
    emploi = pd.DataFrame(
        {
            "ze_name": ["X"],
            "emploi_start": [1.0],
            "emploi_end": [1.0],
            "growth_pct_per_year": [0.0],
        },
        index=pd.Index(["0002"], name="ze_code"),
    )
    with pytest.raises(ze.ZeError, match="no ZE joined"):
        ze.build_summary(vacancy, emploi, unmatched=[])
