"""Behaviour tests for the pure tension core (TLV zoning, shortage, coverage)."""

from __future__ import annotations

import pandas as pd
import pytest

from logement.core import tension
from logement.models import HypothesisRecord


def _tlv_raw(codes: list[str], zonings: list[str]) -> pd.DataFrame:
    return pd.DataFrame(
        {
            "CODGEO25": codes,
            "Zonage TLV post décret 22/12/2025": zonings,
        }
    )


def test_parse_tlv_dedupes_and_strips() -> None:
    """Duplicate commune codes keep their first zoning row."""
    raw = _tlv_raw(["75056", "75056", "33063 "], ["1. Zone tendue", "3. Non tendue", "3. Non tendue"])
    out = tension.parse_tlv(raw).set_index("code")
    assert out.loc["75056", "zonage"] == "1. Zone tendue"
    assert out.loc["33063", "zonage"] == "3. Non tendue"


def test_parse_tlv_requires_columns() -> None:
    """A missing zoning column is a definite reject, not a silent skip."""
    with pytest.raises(tension.TensionError, match="missing TLV column"):
        tension.parse_tlv(pd.DataFrame({"CODGEO25": ["75056"]}))


def _h08(central: float = 6.0) -> HypothesisRecord:
    return HypothesisRecord(
        id="H-08",
        name="fluidity_vacancy_threshold_pct",
        description="test",
        central_value=central,
        plausible_range=(5.0, 7.0),
        unit="pct_of_total_stock",
        confidence="low",
    )


def _tension_frame(threshold: float = 6.0) -> pd.DataFrame:
    census = pd.DataFrame(
        {
            "code": ["00001", "00002"],
            "P22_LOG": [1000.0, 2000.0],
            "P22_LOGVAC": [40.0, 200.0],
        }
    )
    tlv = pd.DataFrame({"code": ["00001"], "zonage": ["1. Zone tendue"]})
    lovac = pd.DataFrame(
        {"code": ["00001", "00002"], "pp_vacant_plus_2ans_2024": [10.0, 60.0]}
    )
    commune_ze = pd.DataFrame(
        {"code": ["00001", "00002"], "ze": ["0001", "0002"]}
    )
    return tension.tension_by_ze(census, tlv, lovac, commune_ze, threshold)


def test_tension_by_ze_computes_need_and_coverage() -> None:
    """Available vacancy, mobilisation need and coverage follow the formulas."""
    frame = _tension_frame()
    # ZE 0001: parc 1000, vacants 40, structurelle 10 -> disponibles 30 (3 %).
    assert frame.loc["0001", "vacants_disponibles"] == pytest.approx(30.0)
    assert bool(frame.loc["0001", "tendue"]) is True
    assert frame.loc["0001", "besoin_mobilisation"] == pytest.approx(0.06 * 1000 - 30)
    assert frame.loc["0001", "couverture_gisement"] == pytest.approx(10 / 30)
    assert frame.loc["0001", "part_tlv_pct"] == pytest.approx(100.0)
    # ZE 0002: vacants 200, structurelle 60 -> disponibles 140 (7 %) : fluide.
    assert bool(frame.loc["0002", "tendue"]) is False
    assert frame.loc["0002", "part_tlv_pct"] == pytest.approx(0.0)


def test_tension_by_ze_keeps_secret_structural_missing() -> None:
    """An all-secret LOVAC ZE keeps NaN structural vacancy, never a silent zero."""
    census = pd.DataFrame(
        {"code": ["00001"], "P22_LOG": [1000.0], "P22_LOGVAC": [40.0]}
    )
    lovac = pd.DataFrame({"code": ["00001"], "pp_vacant_plus_2ans_2024": [float("nan")]})
    commune_ze = pd.DataFrame({"code": ["00001"], "ze": ["0001"]})
    frame = tension.tension_by_ze(
        census, pd.DataFrame({"code": [], "zonage": []}), lovac, commune_ze, 6.0
    )
    assert pd.isna(frame.loc["0001", "structurelle"])


def test_build_summary_shape_and_threshold_monotonicity() -> None:
    """A higher fluidity threshold can only widen the tense-ZE set."""
    frame = _tension_frame()
    summary = tension.build_summary(
        frame, pd.Series({"0001": "Alpha", "0002": "Beta"}), _h08()
    )
    assert summary["n_ze"] == 2
    national = summary["national"]
    assert national["n_ze_tendues"] == 1
    assert national["besoin_logements"] == 30
    low, central, high = summary["sensibilite_seuil"]
    assert low["n_ze_tendues"] <= central["n_ze_tendues"] <= high["n_ze_tendues"]
    assert summary["top_besoin"][0]["name"] == "Alpha"
    assert summary["artefacts_disponible_negatif"] == []


def test_build_summary_flags_negative_available_vacancy() -> None:
    """Structural above census vacancy (perimeter artifact) is flagged, kept."""
    census = pd.DataFrame(
        {"code": ["00001"], "P22_LOG": [1000.0], "P22_LOGVAC": [40.0]}
    )
    lovac = pd.DataFrame({"code": ["00001"], "pp_vacant_plus_2ans_2024": [70.0]})
    commune_ze = pd.DataFrame({"code": ["00001"], "ze": ["0001"]})
    frame = tension.tension_by_ze(
        census, pd.DataFrame({"code": [], "zonage": []}), lovac, commune_ze, 6.0
    )
    summary = tension.build_summary(frame, pd.Series({"0001": "Alpha"}), _h08())
    assert summary["artefacts_disponible_negatif"] == ["0001"]
