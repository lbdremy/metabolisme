"""Behaviour tests for the pure building-condition core (age, DPE, contrast)."""

from __future__ import annotations

import pandas as pd
import pytest

from logement.core import bati


def test_parse_census_bati_dedupes_plm() -> None:
    """PLM parent rows come first in the base and win over arrondissements."""
    raw = pd.DataFrame(
        {
            "CODGEO": ["75056", "75101", "33063"],
            "P22_RP": ["100", "10", "50"],
            "P22_RP_ACHTOT": ["90", "9", "45"],
            "P22_RP_ACH1919": ["30", "3", "5"],
            "P22_RP_ACH1945": ["15", "2", "4"],
            "P22_RP_BDWC": ["0", "0", "0"],
        }
    )
    out = bati.parse_census_bati(raw).set_index("code")
    assert len(out) == 2
    assert out.loc["75056", "P22_RP"] == pytest.approx(100.0)


def test_bati_by_ze_masks_discomfort_outside_dom() -> None:
    """The sanitary question only exists in the DOM: métropole share is missing."""
    census = pd.DataFrame(
        {
            "code": ["97101", "33063"],
            "P22_RP": [100.0, 200.0],
            "P22_RP_ACHTOT": [90.0, 180.0],
            "P22_RP_ACH1919": [9.0, 60.0],
            "P22_RP_ACH1945": [9.0, 30.0],
            "P22_RP_BDWC": [95.0, 0.0],
        }
    )
    commune_ze = pd.DataFrame({"code": ["97101", "33063"], "ze": ["0101", "7507"]})
    frame = bati.bati_by_ze(census, commune_ze)
    assert frame.loc["0101", "part_inconfort_pct"] == pytest.approx(5.0)
    assert pd.isna(frame.loc["7507", "part_inconfort_pct"])
    assert frame.loc["7507", "part_avant_1946_pct"] == pytest.approx(50.0)
    assert not frame.loc["7507", "dom"]


def test_parse_dpe_counts_drops_unknown_labels_and_reports() -> None:
    """Missing commune codes and unknown labels are dropped AND counted."""
    raw = pd.DataFrame(
        {
            "code_insee_ban": ["75101", "75102", None, "33063"],
            "etiquette_dpe": ["G", "G", "G", "X"],
            "n_dpe": ["5", "7", "3", "2"],
        }
    )
    counts = bati.parse_dpe_counts(raw)
    assert counts.loc["75056", "G"] == 12  # arrondissements summed into Paris
    assert counts.attrs["dropped_rows"] == 2
    assert list(counts.columns) == list(bati.DPE_LABELS)


def test_dpe_by_ze_computes_fg_share() -> None:
    """The F+G share is computed over all diagnosed dwellings of the ZE."""
    counts = pd.DataFrame(
        {"A": [1], "B": [0], "C": [3], "D": [2], "E": [0], "F": [2], "G": [2]},
        index=pd.Index(["33063"], name="code"),
    )
    commune_ze = pd.DataFrame({"code": ["33063"], "ze": ["7507"]})
    frame = bati.dpe_by_ze(counts, commune_ze)
    assert frame.loc["7507", "n_dpe"] == 10
    assert frame.loc["7507", "part_fg_pct"] == pytest.approx(40.0)


def _summary_fixture() -> dict[str, object]:
    bati_ze = pd.DataFrame(
        {
            "P22_RP": [100.0, 200.0],
            "P22_RP_ACHTOT": [90.0, 180.0],
            "P22_RP_ACH1919": [9.0, 60.0],
            "P22_RP_ACH1945": [9.0, 30.0],
            "P22_RP_BDWC": [95.0, 0.0],
            "part_avant_1946_pct": [20.0, 50.0],
            "dom": [True, False],
            "part_inconfort_pct": [5.0, float("nan")],
        },
        index=pd.Index(["0101", "7507"], name="ze"),
    )
    dpe_ze = pd.DataFrame(
        {
            "n_dpe": [10.0, 20.0],
            "part_fg_pct": [40.0, 20.0],
            "F": [2.0, 2.0],
            "G": [2.0, 2.0],
        },
        index=pd.Index(["0101", "7507"], name="ze"),
    )
    vacancy_ze = pd.DataFrame(
        {"structural_rate_pct": [12.0, 4.0]},
        index=pd.Index(["0101", "7507"], name="ze"),
    )
    names = pd.Series({"0101": "Dom", "7507": "Metro"})
    return bati.build_summary(bati_ze, dpe_ze, vacancy_ze, names, dpe_dropped_rows=3)


def test_build_summary_shape_and_dom_contrast() -> None:
    """The R-08 payload separates the DOM contrast from the metropolitan cross."""
    summary = _summary_fixture()
    assert summary["n_ze"] == 2
    assert summary["n_ze_dom"] == 1
    assert summary["dpe_dropped_rows"] == 3
    contrast = summary["dom_contrast"]
    assert contrast["n"] == 1
    assert contrast["median_vacancy_pct"] == pytest.approx(12.0)
    spearman = summary["spearman_age_vs_vacancy"]
    assert -1 <= spearman["all"] <= 1
    assert summary["top_age"][0]["name"] == "Metro"
