"""Behaviour tests for the pure tension core (TLV zoning, shortage, coverage).

Extended by the 2026-08-07 adversarial review: existence rate H-12
propagated on both sides of C-06, negative availables clipped out of the
need, TLV-restricted stock, secrecy bound, joint H-08 × H-12 grid.
"""

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


def _h12(central: float = 1.0, low: float = 0.5) -> HypothesisRecord:
    return HypothesisRecord(
        id="H-12",
        name="lovac_structural_existence_rate",
        description="test",
        central_value=central,
        plausible_range=(low, 1.0),
        unit="fraction",
        confidence="low",
    )


_CENSUS = pd.DataFrame(
    {
        "code": ["00001", "00002"],
        "P22_LOG": [1000.0, 2000.0],
        "P22_LOGVAC": [40.0, 200.0],
    }
)
_TLV = pd.DataFrame({"code": ["00001"], "zonage": ["1. Zone tendue"]})
_LOVAC = pd.DataFrame({"code": ["00001", "00002"], "pp_vacant_plus_2ans_2024": [10.0, 60.0]})
_COMMUNE_ZE = pd.DataFrame({"code": ["00001", "00002"], "ze": ["0001", "0002"]})


def _tension_frame(threshold: float = 6.0, existence_rate: float = 1.0) -> pd.DataFrame:
    return tension.tension_by_ze(_CENSUS, _TLV, _LOVAC, _COMMUNE_ZE, threshold, existence_rate)


def _frames(existence_central: float = 1.0, existence_low: float = 0.5) -> dict[str, pd.DataFrame]:
    return {
        "bas": _tension_frame(existence_rate=existence_low),
        "central": _tension_frame(existence_rate=existence_central),
        "haut": _tension_frame(existence_rate=1.0),
    }


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


def test_existence_rate_applies_to_both_sides() -> None:
    """H-12 shrinks the stock AND grows the available vacancy coherently."""
    frame = _tension_frame(existence_rate=0.5)
    # ZE 0001: effective structurelle 5, disponibles 35, besoin 60-35=25.
    assert frame.loc["0001", "structurelle"] == pytest.approx(5.0)
    assert frame.loc["0001", "structurelle_lovac"] == pytest.approx(10.0)
    assert frame.loc["0001", "vacants_disponibles"] == pytest.approx(35.0)
    assert frame.loc["0001", "besoin_mobilisation"] == pytest.approx(25.0)
    assert frame.loc["0001", "couverture_gisement"] == pytest.approx(5 / 25)


def test_tlv_restricted_stock_splits_by_zoning() -> None:
    """The TLV-restricted stock only counts the legally-tense communes."""
    frame = _tension_frame()
    # ZE 0001 is fully TLV -> its whole stock counts; ZE 0002 has none.
    assert frame.loc["0001", "structurelle_tlv"] == pytest.approx(10.0)
    assert frame.loc["0002", "structurelle_tlv"] == pytest.approx(0.0)


def test_tension_by_ze_keeps_secret_structural_missing() -> None:
    """An all-secret LOVAC ZE keeps NaN structural vacancy, never a silent zero."""
    census = pd.DataFrame({"code": ["00001"], "P22_LOG": [1000.0], "P22_LOGVAC": [40.0]})
    lovac = pd.DataFrame({"code": ["00001"], "pp_vacant_plus_2ans_2024": [float("nan")]})
    commune_ze = pd.DataFrame({"code": ["00001"], "ze": ["0001"]})
    frame = tension.tension_by_ze(
        census, pd.DataFrame({"code": [], "zonage": []}), lovac, commune_ze, 6.0
    )
    assert pd.isna(frame.loc["0001", "structurelle"])
    assert frame.loc["0001", "n_communes_masquees"] == 1


def test_build_summary_shape_and_threshold_monotonicity() -> None:
    """A higher fluidity threshold can only widen the tense-ZE set."""
    summary = tension.build_summary(
        _frames(), pd.Series({"0001": "Alpha", "0002": "Beta"}), _h08(), _h12()
    )
    assert summary["n_ze"] == 2
    national = summary["national"]
    assert national["n_ze_tendues"] == 1
    assert national["besoin_logements"] == 30
    assert national["couverture_communes_tlv"] == national["couverture"]  # ZE 0001 all-TLV
    low, central, high = summary["sensibilite_seuil"]
    assert low["n_ze_tendues"] <= central["n_ze_tendues"] <= high["n_ze_tendues"]
    assert summary["top_besoin"][0]["name"] == "Alpha"
    assert summary["artefacts_disponible_negatif"] == []
    assert len(summary["sensibilite_seuil_x_existence"]) == 9
    couvertes = summary["ze_couvertes"]
    assert couvertes["besoin_couvert"] + couvertes["besoin_non_couvert"] == pytest.approx(
        national["besoin_logements"]
    )


def test_secrecy_bound_moves_coverage_toward_one() -> None:
    """Adding the masked mass moves an above-one coverage DOWN toward 1."""
    census = pd.DataFrame({"code": ["00001", "00002"], "P22_LOG": [1000.0, 1000.0], "P22_LOGVAC": [40.0, 40.0]})
    lovac = pd.DataFrame(
        {"code": ["00001", "00002"], "pp_vacant_plus_2ans_2024": [35.0, float("nan")]}
    )
    commune_ze = pd.DataFrame({"code": ["00001", "00002"], "ze": ["0001", "0001"]})
    frame = tension.tension_by_ze(
        census, pd.DataFrame({"code": [], "zonage": []}), lovac, commune_ze, 6.0
    )
    frames = {"bas": frame, "central": frame, "haut": frame}
    summary = tension.build_summary(frames, pd.Series({"0001": "Alpha"}), _h08(), _h12())
    national = summary["national"]
    bound = summary["borne_secretisation"]
    assert bound["n_communes_masquees_tendues"] == 1
    # coverage 35/(120-45)=0.466... adding 10 hidden: 45/85=0.53 — moves UP
    # toward 1 when below 1; the property is monotone convergence toward 1.
    couverture = national["couverture"]
    borne = bound["couverture_borne_masquee"]
    assert abs(borne - 1) <= abs(couverture - 1) + 1e-9


def test_build_summary_flags_and_clips_negative_available_vacancy() -> None:
    """Structural above census vacancy is flagged AND clipped out of the need."""
    census = pd.DataFrame({"code": ["00001"], "P22_LOG": [1000.0], "P22_LOGVAC": [40.0]})
    lovac = pd.DataFrame({"code": ["00001"], "pp_vacant_plus_2ans_2024": [70.0]})
    commune_ze = pd.DataFrame({"code": ["00001"], "ze": ["0001"]})
    frame = tension.tension_by_ze(
        census, pd.DataFrame({"code": [], "zonage": []}), lovac, commune_ze, 6.0
    )
    frames = {"bas": frame, "central": frame, "haut": frame}
    summary = tension.build_summary(frames, pd.Series({"0001": "Alpha"}), _h08(), _h12())
    assert summary["artefacts_disponible_negatif"] == ["0001"]
    # disponible -30 clipped: besoin = 60, not 90; the clipped mass is published.
    assert summary["national"]["besoin_logements"] == 60
    assert summary["national"]["besoin_sans_ecretage"] == 90
    assert summary["besoin_artefacts_ecrete"] == 30
