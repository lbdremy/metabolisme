"""Behaviour tests for the pure parc core (parsing, invariants, transforms)."""

from __future__ import annotations

import pandas as pd
import pytest
from hypothesis import given
from hypothesis import strategies as st

from logement.core import parc

RP, RS, VAC = parc.CATEGORIES


def eapl_frame(rows: dict[str, list[float]], years: list[str]) -> pd.DataFrame:
    """Build a raw frame shaped like S-02's 'Données' sheet (header on the year row)."""
    return pd.DataFrame(
        {"Parc de logements": list(rows.keys())} | dict(zip(years, zip(*rows.values()))),
    )


VALID_ROWS = {
    "Résidences principales": [100.0, 110.0],
    "\xa0\xa0\xa0\xa0Individuel": [60.0, 65.0],
    "Logements vacants": [10.0, 12.0],
    "Résidences secondaires,\xa0 logements occasionnels": [20.0, 21.0],
    "Ensemble": [130.0, 143.0],
}


def test_parse_eapl_categories_normalizes_and_orders() -> None:
    """Labels are normalized, sub-rows dropped, provisional '(p)' years detected."""
    parsed = parc.parse_eapl_categories(eapl_frame(VALID_ROWS, ["1982", "1983 (p)"]))
    assert list(parsed.counts.columns) == [RP, RS, VAC, parc.TOTAL]
    assert list(parsed.counts.index) == [1982, 1983]
    assert parsed.provisional_years == (1983,)
    assert parsed.counts.loc[1982, VAC] == 10.0


def test_parse_eapl_categories_rejects_broken_sum() -> None:
    """The category-sum invariant is enforced, not silently accepted."""
    rows = {**VALID_ROWS, "Ensemble": [140.0, 143.0]}  # off by 10 in 1982
    with pytest.raises(parc.ParcError, match="differ from the total"):
        parc.parse_eapl_categories(eapl_frame(rows, ["1982", "1983"]))


def test_parse_eapl_categories_rejects_missing_category() -> None:
    """A sheet without one of the expected categories is a loud error."""
    rows = {k: v for k, v in VALID_ROWS.items() if k != "Logements vacants"}
    with pytest.raises(parc.ParcError, match="missing EAPL categories"):
        parc.parse_eapl_categories(eapl_frame(rows, ["1982", "1983"]))


def menages_frame() -> pd.DataFrame:
    """Build a raw frame shaped like S-03's 'France' sheet read with header=None."""
    return pd.DataFrame(
        [
            ["Nombre de personnes par ménage", None, None],
            [None, None, None],
            [None, "1982", "1990"],
            ["   1  personne", "4865.2", "5916.9"],
            ["   Total", "n.d.", "21945.8"],
        ]
    )


def test_parse_menages_totals_drops_nd() -> None:
    """'n.d.' vintages disappear; numeric ones survive with int year index."""
    series = parc.parse_menages_totals(menages_frame())
    assert series.to_dict() == {1990: 21945.8}


def test_parse_population_index_handles_suffixed_years() -> None:
    """'2025p' and footnote rows are handled by extracting the 4-digit year."""
    raw = pd.DataFrame(
        {"Année": ["1982", "2025p", "Champ : France."], "Population": ["100", "121.9", None]}
    )
    series = parc.parse_population_index(raw)
    assert series.to_dict() == {1982: 100.0, 2025: 121.9}


@given(
    values=st.lists(st.floats(min_value=1, max_value=1e6, allow_nan=False), min_size=2, max_size=8)
)
def test_index_to_base_is_100_at_base(values: list[float]) -> None:
    """Property: any rebased series is exactly 100 at its base year."""
    series = pd.Series(values, index=range(2000, 2000 + len(values)))
    rebased = parc.index_to_base(series, 2000)
    assert rebased[2000] == pytest.approx(100.0)


@given(value=st.floats(min_value=1, max_value=1e6, allow_nan=False), years=st.integers(1, 50))
def test_constant_series_has_zero_growth(value: float, years: int) -> None:
    """Property: a constant series has a 0 %/year mean growth over any period."""
    series = pd.Series([value, value], index=[2000, 2000 + years])
    assert parc.mean_annual_growth(series, 2000, 2000 + years) == pytest.approx(0.0)


def test_build_summary_shape() -> None:
    """The R-01 payload carries the expected keys and a coherent base year."""
    parsed = parc.parse_eapl_categories(eapl_frame(VALID_ROWS, ["1982", "1983 (p)"]))
    menages = pd.Series([120.0, 130.0], index=[1982, 1983])
    population = pd.Series([100.0, 101.0], index=[1982, 1983])
    summary = parc.build_summary(parsed, menages, population)
    assert summary["base_year"] == 1982
    assert summary["provisional_years"] == [1983]
    indices = summary["indices_at_last_common_vintage"]
    assert isinstance(indices, dict)
    assert indices["year"] == 1983
    assert indices["dwellings"] == pytest.approx(110.0, abs=0.1)
