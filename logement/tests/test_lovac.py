"""Behaviour tests for the pure LOVAC core (parsing, PLM aggregation, rates)."""

from __future__ import annotations

import pandas as pd
import pytest
from hypothesis import given
from hypothesis import strategies as st

from logement.core import lovac


def test_parse_counts_handles_secrecy_and_separators() -> None:
    """'s' becomes NA; nbsp/space thousands separators are stripped."""
    raw = pd.Series([" 26\xa0755    ", "s", " 3\xa0160\xa0235 ", None])
    parsed = lovac.parse_counts(raw)
    assert parsed[0] == 26755
    assert pd.isna(parsed[1])
    assert parsed[2] == 3160235
    assert pd.isna(parsed[3])


def test_parse_france_indexes_by_millesime() -> None:
    """The France file becomes a millésime-indexed numeric frame."""
    raw = pd.DataFrame(
        {
            " FR ": ["France", None],
            "Millésime": ["2026", "2025"],
            "ff_pp_total": [None, " 33\xa0194\xa0351 "],
            "pp_vacant": [" 3\xa0160\xa0235 ", " 2\xa0380\xa0076 "],
            "pp_vacant_plus_2ans": [" 1\xa0179\xa0845 ", " 1\xa0348\xa0470 "],
        }
    )
    france = lovac.parse_france(raw)
    assert list(france.index) == [2025, 2026]
    assert france.loc[2026, "pp_vacant_plus_2ans"] == 1179845
    assert pd.isna(france.loc[2026, "ff_pp_total"])


def test_parse_france_rejects_missing_columns() -> None:
    """A France file without the expected columns is a loud error."""
    with pytest.raises(lovac.LovacError, match="missing France columns"):
        lovac.parse_france(pd.DataFrame({"Millésime": ["2026"]}))


TERR = pd.DataFrame(
    {
        " DEP ": ["01", "02"],
        " LIB_DEP ": [" Ain ", "Aisne"],
        " pp_vacant_plus_2ans_24 ": [" 10\xa0877 ", "s"],
        " ff_pp_total_24 ": [" 293\xa0837 ", " 230\xa0105 "],
    }
)


def test_parse_territories_normalizes_millesimes_to_four_digits() -> None:
    """Count columns are renamed <var>_<20xx> and parsed numeric."""
    out = lovac.parse_territories(TERR, code_col="DEP", name_col="LIB_DEP")
    assert list(out.columns) == ["code", "name", "pp_vacant_plus_2ans_2024", "ff_pp_total_2024"]
    assert out.loc[0, "name"] == "Ain"
    assert out.loc[0, "pp_vacant_plus_2ans_2024"] == 10877
    assert pd.isna(out.loc[1, "pp_vacant_plus_2ans_2024"])


def test_structural_rate_requires_available_millesime() -> None:
    """Asking for a millésime the frame doesn't carry raises."""
    out = lovac.parse_territories(TERR, code_col="DEP", name_col="LIB_DEP")
    assert lovac.structural_rate(out, 2024)[0] == pytest.approx(10877 / 293837 * 100)
    with pytest.raises(lovac.LovacError, match="2026 not available"):
        lovac.structural_rate(out, 2026)


def _city_frame(values: dict[str, float | None]) -> pd.DataFrame:
    return pd.DataFrame(
        {
            "code": list(values.keys()),
            "name": [f"name-{c}" for c in values],
            "n_2024": pd.array(list(values.values()), dtype="Float64"),
        }
    )


def test_aggregate_plm_sums_arrondissements() -> None:
    """Paris arrondissements collapse into a single 75056 'Paris' row."""
    cities = lovac.aggregate_plm(_city_frame({"75101": 100, "75102": 50, "33063": 7}), ["n_2024"])
    paris = cities[cities["code"] == "75056"].iloc[0]
    assert paris["n_2024"] == 150
    assert paris["name"] == "Paris"
    assert len(cities) == 2


def test_aggregate_plm_propagates_secrecy() -> None:
    """A masked arrondissement masks the parent sum instead of understating it."""
    cities = lovac.aggregate_plm(_city_frame({"13201": 100, "13202": None}), ["n_2024"])
    assert pd.isna(cities.loc[cities["code"] == "13055", "n_2024"]).all()


@given(
    st.dictionaries(
        st.sampled_from(["75101", "75102", "75103", "69381", "69382", "13201", "33063"]),
        st.integers(min_value=0, max_value=10_000),
        min_size=1,
    )
)
def test_aggregate_plm_preserves_totals(values: dict[str, int]) -> None:
    """Property: with no masked value, PLM aggregation never changes the total."""
    frame = _city_frame({k: float(v) for k, v in values.items()})
    cities = lovac.aggregate_plm(frame, ["n_2024"])
    assert cities["n_2024"].sum() == sum(values.values())
