"""Behaviour tests for the pure remobilisation-cost core (IPEA, unit cost)."""

from __future__ import annotations

import pandas as pd
import pytest

from logement.core import remob
from logement.models import HypothesisRecord

IPEA_XML = (
    '<obs TIME_PERIOD="2016-Q1" OBS_VALUE="90.0"/>'
    '<obs TIME_PERIOD="2016-Q2" OBS_VALUE="92.0"/>'
    '<obs TIME_PERIOD="2023-Q1" OBS_VALUE="113.75"/>'
    '<obs TIME_PERIOD="2023-Q2" OBS_VALUE="113.75"/>'
)


def test_parse_ipea_and_factor() -> None:
    """Annual means and the 2016→2023 factor come from the frozen series."""
    means = remob.parse_ipea_annual_means(IPEA_XML)
    assert means["2016"] == pytest.approx(91.0)
    assert remob.ipea_factor(means) == pytest.approx(113.75 / 91.0)


def test_ipea_factor_requires_both_years() -> None:
    """A truncated series is a definite reject, not a silent fallback."""
    means = remob.parse_ipea_annual_means('<obs TIME_PERIOD="2016-Q1" OBS_VALUE="90.0"/>')
    with pytest.raises(remob.RemobError, match="2023"):
        remob.ipea_factor(means)


def test_unit_cost_mixes_house_share() -> None:
    """The per-dwelling cost mixes house/flat costs at the S-12 surfaces."""
    cost = remob.unit_cost_eur(pd.Series([1.0, 0.0]), 400.0, 200.0, 1.25)
    assert cost.iloc[0] == pytest.approx(400.0 * remob.SURFACE_MAISON_M2 * 1.055 * 1.25)
    assert cost.iloc[1] == pytest.approx(200.0 * remob.SURFACE_APPART_M2 * 1.055 * 1.25)


def _hypothesis(hid: str, central: float, low: float, high: float) -> HypothesisRecord:
    return HypothesisRecord(
        id=hid,
        name="test",
        description="test",
        central_value=central,
        plausible_range=(low, high),
        unit="eur_ht_2016_per_m2",
        confidence="medium",
    )


def test_build_summary_variants_are_ordered() -> None:
    """bas ≤ central ≤ haut for every cost aggregate, and the ratio is coherent."""
    tense = pd.DataFrame(
        {"besoin_mobilisation": [1000.0], "structurelle": [2000.0]},
        index=pd.Index(["0001"], name="ze"),
    )
    summary = remob.build_summary(
        tense,
        pd.Series({"0001": 0.5}),
        pd.Series({"0001": "Alpha"}),
        _hypothesis("H-09", 400.0, 350.0, 500.0),
        _hypothesis("H-10", 250.0, 200.0, 300.0),
        remob.parse_ipea_annual_means(IPEA_XML),
    )
    couts = summary["couts"]
    assert (
        couts["bas"]["cout_detente_mdeur"]
        <= couts["central"]["cout_detente_mdeur"]
        <= couts["haut"]["cout_detente_mdeur"]
    )
    assert summary["besoin_total"] == 1000
    assert summary["top_cout_detente"][0]["name"] == "Alpha"
    ratios = summary["comparateur_neuf"]["ratio_neuf_sur_remobilisation"]
    assert ratios["bas"] >= ratios["central"] >= ratios["haut"]
