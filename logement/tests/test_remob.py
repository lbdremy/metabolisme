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


def _summary(tense: pd.DataFrame) -> dict[str, object]:
    tense_by_seuil = {"bas": tense, "central": tense, "haut": tense}
    return remob.build_summary(
        tense_by_seuil,
        pd.Series({"0001": 0.5, "0002": 0.5}),
        pd.Series({"0001": "Alpha", "0002": "Beta"}),
        _hypothesis("H-08", 6.0, 5.0, 7.0),
        _hypothesis("H-09", 400.0, 350.0, 500.0),
        _hypothesis("H-10", 250.0, 200.0, 300.0),
        _hypothesis("H-12", 0.75, 0.6, 0.9),
        remob.parse_ipea_annual_means(IPEA_XML),
    )


def test_build_summary_variants_are_ordered() -> None:
    """bas ≤ central ≤ haut for every cost aggregate, and the ratio is coherent."""
    tense = pd.DataFrame(
        {"besoin_mobilisation": [1000.0], "structurelle": [2000.0]},
        index=pd.Index(["0001"], name="ze"),
    )
    summary = _summary(tense)
    couts = summary["couts"]
    assert (
        couts["bas"]["cout_detente_mixte_mdeur"]
        <= couts["central"]["cout_detente_mixte_mdeur"]
        <= couts["haut"]["cout_detente_mixte_mdeur"]
    )
    assert summary["besoin_total"] == 1000
    assert summary["top_cout_detente"][0]["name"] == "Alpha"
    ratios = summary["comparateur_neuf"]["ratio_neuf_sur_detente_mixte"]
    assert ratios["bas"] >= ratios["central"] >= ratios["haut"]
    # stock (2000) covers the need (1000): the mixed cost equals the naive one
    assert (
        couts["central"]["cout_detente_mixte_mdeur"]
        == couts["central"]["cout_detente_renovation_seule_mdeur"]
    )


def test_mixed_cost_caps_renovation_at_local_stock() -> None:
    """A ZE without local stock is priced at the new-build comparator."""
    tense = pd.DataFrame(
        {"besoin_mobilisation": [100_000.0, 50_000.0], "structurelle": [200_000.0, 0.0]},
        index=pd.Index(["0001", "0002"], name="ze"),
    )
    summary = _summary(tense)
    logements = summary["logements"]
    assert logements["renovables"] == 100_000
    assert logements["deficit_neuf"] == 50_000
    central = summary["couts"]["central"]
    # the deficit leg is priced at the S-18 comparator, so the mixed cost
    # exceeds the naive renovation-only figure (the pre-review incoherence)
    assert central["cout_detente_mixte_mdeur"] > central["cout_detente_renovation_seule_mdeur"]
    assert central["dont_deficit_neuf_mdeur"] == pytest.approx(
        50_000 * remob.PRIX_REVIENT_NEUF_EUR_2023 / 1e9, abs=0.05
    )
    # the heavy-rehabilitation stress test doubles only the renovation leg
    lourde = summary["variante_rehabilitation_lourde"]
    assert lourde["cout_detente_mixte_mdeur"] > central["cout_detente_mixte_mdeur"]
    assert len(summary["sensibilite_seuil_h08"]) == 3
