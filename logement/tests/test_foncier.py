"""Behaviour tests for the pure immobilised-land core (friches, density)."""

from __future__ import annotations

import pandas as pd
import pytest

from logement.core import foncier
from logement.models import HypothesisRecord


def test_parse_friches_maps_plm_and_flags_residential() -> None:
    """Commune codes map to PLM parents; residential typing survives accents."""
    raw = pd.DataFrame(
        {
            "comm_insee": ["75101", "33063", "13055"],
            "site_statut": ["friche sans projet"] * 3,
            "unite_fonciere_surface": ["1000", "2000", None],
            "bati_type": ["résidentiel", "industriel", None],
        }
    )
    out = foncier.parse_friches(raw)
    assert list(out["code"]) == ["75056", "33063"]  # NA surface dropped
    assert list(out["residentiel"]) == [True, False]


def _density_frame() -> pd.DataFrame:
    census = pd.DataFrame(
        {
            "CODGEO": ["75101", "75116"],
            "P22_LOG": ["15000", "80000"],
            "P22_RP_ACHTOT": ["10000", "60000"],
            "P22_RP_ACH1919": ["8000", "20000"],
        }
    )
    superficies = pd.Series({"75101": 1.0, "75116": 8.0})
    return foncier.haussmann_density(census, superficies)


def test_haussmann_density_selects_pre1919_arrondissements() -> None:
    """Only arrondissements with ≥ 60 % pre-1919 stock carry the flag."""
    frame = _density_frame()
    assert bool(frame.loc["75101", "haussmannien"]) is True  # 80 % avant 1919
    assert bool(frame.loc["75116", "haussmannien"]) is False  # 33 %
    assert frame.loc["75101", "densite_logts_ha"] == pytest.approx(150.0)


def _h11(central: float = 150.0, low: float = 150.0, high: float = 150.0) -> HypothesisRecord:
    return HypothesisRecord(
        id="H-11",
        name="haussmann_reference_density_dwellings_per_ha",
        description="test",
        central_value=central,
        plausible_range=(low, high),
        unit="dwellings_per_ha",
        confidence="medium",
    )


def test_check_h11_refuses_registry_drift() -> None:
    """A registry value that no longer matches the data is a hard error."""
    frame = _density_frame()
    assert foncier.check_h11_against_data(frame, _h11())["central"] == pytest.approx(150.0)
    with pytest.raises(foncier.FoncierError, match="drift"):
        foncier.check_h11_against_data(frame, _h11(central=140.0, low=140.0, high=150.0))


def test_foncier_summary_caps_and_counts() -> None:
    """Per-site cap applies, residential sites are excluded, ratios computed."""
    friches = pd.DataFrame(
        {
            "code": ["00001", "00001", "00002"],
            "statut": ["friche sans projet", "friche sans projet", "friche potentielle"],
            "surface_m2": [600_000.0, 10_000.0, 20_000.0],
            "residentiel": [False, True, False],
        }
    )
    commune_ze = pd.DataFrame({"code": ["00001", "00002"], "ze": ["0001", "0001"]})
    tense_besoin = pd.Series({"0001": 1000.0})
    besoin_par_seuil = {
        "bas": {"seuil_pct": 5.0, "besoin": 500.0},
        "central": {"seuil_pct": 6.0, "besoin": 1000.0},
        "haut": {"seuil_pct": 7.0, "besoin": 2000.0},
    }
    summary = foncier.foncier_summary(
        friches,
        commune_ze,
        tense_besoin,
        besoin_par_seuil,
        _density_frame(),
        pd.Series({"0001": "Alpha"}),
        _h11(),
    )
    central = summary["gisement_central"]
    assert central["n_sites"] == 1  # residential excluded
    assert central["n_sites_plafonnes"] == 1
    assert central["ha_plafonnes"] == 50  # capped at 50 ha
    assert central["ha_bruts"] == 60
    assert summary["capacite_centrale"]["central"]["logements"] == 50 * 150
    assert summary["gisement_haute"]["n_sites"] == 2
    assert summary["top_gisements"][0]["name"] == "Alpha"
    # H-08 propagation: a doubled need halves the density-central ratio
    seuils = {s["seuil_pct"]: s for s in summary["sensibilite_seuil_h08"]}
    assert seuils[7.0]["ratio_capacite_centrale"] == pytest.approx(
        seuils[6.0]["ratio_capacite_centrale"] / 2, abs=0.1
    )
    # observed fonds-friches density is far below the Haussmannian etalon
    constatee = summary["densite_constatee_fonds_friches"]
    assert constatee["logements_par_ha"] < 150
    assert constatee["capacite_gisement_central"] == pytest.approx(
        50 * constatee["logements_par_ha"], abs=1
    )
