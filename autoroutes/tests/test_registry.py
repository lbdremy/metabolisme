"""Behaviour tests for the pure registry core (parse + cross-check)."""

from __future__ import annotations

import pytest
from hypothesis import given
from hypothesis import strategies as st

from autoroutes.core import registry
from autoroutes.models import HypothesisRecord

SOURCE = {
    "id": "S-01",
    "publisher": "ART",
    "title": "Économie des concessions autoroutières",
    "source_url": "https://example.invalid/egc",
    "publication_date": "2024-12-02",
    "retrieved_at": "2026-09-18",
    "geographic_scope": "France",
    "temporal_scope": "2017-2023",
    "license": "CRPA",
}

DEFINITION = {
    "id": "D-01",
    "term": "rente mesurable",
    "source": "S-01",
    "definition": "Surprofit sur base d'actifs au coût historique.",
    "caveats": ["Notion construite."],
}

HYPOTHESIS = {
    "id": "H-01",
    "name": "reference_return_on_capital",
    "description": "Taux de référence de rémunération du capital",
    "central_value": 5.0,
    "plausible_range": [4.0, 8.8],
    "unit": "% nominal avant impôts",
    "confidence": "medium",
    "justification": ["S-01"],
    "affects": ["M-01"],
}

QUALITATIVE = {
    "id": "H-02",
    "name": "motorway_is_not_duplicable",
    "description": "L'infrastructure autoroutière n'est pas duplicable",
    "statement": "Réfutée si une alternative gratuite de qualité comparable existe.",
    "confidence": "low",
    "justification": ["S-01"],
    "limitations": ["L-01"],
}


def test_empty_registries_parse_to_empty_lists() -> None:
    """A `[]` (or missing → None) payload is a valid, empty registry."""
    assert registry.parse_sources([]) == []
    assert registry.parse_definitions(None) == []
    assert registry.parse_hypotheses([]) == []
    assert registry.parse_claims(None) == []


def test_full_records_round_trip() -> None:
    """Numeric and qualitative hypotheses, constructed definitions all parse."""
    (source,) = registry.parse_sources([SOURCE])
    (definition,) = registry.parse_definitions([{**DEFINITION, "constructed_by": "C-01"}])
    numeric, qualitative = registry.parse_hypotheses([HYPOTHESIS, QUALITATIVE])
    assert source.id == "S-01"
    assert definition.constructed_by == "C-01"
    assert numeric.is_quantified and numeric.plausible_range == (4.0, 8.8)
    assert not qualitative.is_quantified and qualitative.limitations == ["L-01"]
    claims = registry.parse_claims(
        [
            {"id": "C-01", "type": "choice", "title": "construit D-01"},
            {"id": "L-01", "type": "limit", "title": "limite"},
            {"id": "M-01", "type": "measure", "title": "m", "depends_on": ["H-01", "D-01"]},
        ]
    )
    assert registry.cross_check([source], [definition], [numeric, qualitative], claims) == []


@pytest.mark.parametrize(
    ("payload", "registry_name"),
    [
        ({"not": "a list"}, "sources"),
        ([{**SOURCE, "typo_key": 1}], "sources"),
        ([{**SOURCE, "id": "X-01"}], "sources"),
        ([{**SOURCE, "local_file": "data/raw/x.csv"}], "sources"),  # frozen but unchecksummed
        ([{**HYPOTHESIS, "central_value": 9.5}], "hypotheses"),  # outside plausible_range
        ([{**HYPOTHESIS, "plausible_range": [8.8, 4.0]}], "hypotheses"),  # unordered
        ([{**HYPOTHESIS, "confidence": "certain"}], "hypotheses"),  # not a valid level
        ([{**QUALITATIVE, "central_value": 1.0}], "hypotheses"),  # incomplete numeric triple
        (  # neither a numeric parameter nor a statement
            [{k: v for k, v in QUALITATIVE.items() if k != "statement"}],
            "hypotheses",
        ),
        ([{**DEFINITION, "constructed_by": "S-01"}], "definitions"),  # must be a choice
        ([{"id": "R-01", "type": "measure", "title": "x"}], "claims"),  # prefix ≠ type
    ],
)
def test_invalid_payloads_are_rejected(payload: object, registry_name: str) -> None:
    """Strict models make malformed registry entries loud errors, not silent drops."""
    parse = {
        "sources": registry.parse_sources,
        "definitions": registry.parse_definitions,
        "hypotheses": registry.parse_hypotheses,
        "claims": registry.parse_claims,
    }[registry_name]
    with pytest.raises(registry.RegistryError):
        parse(payload)


def test_cross_check_flags_duplicates_and_dangling_references() -> None:
    """Duplicate ids and references to unregistered nodes must surface."""
    source = registry.parse_sources([SOURCE])[0]
    orphan_def = registry.parse_definitions([{**DEFINITION, "source": "S-99"}])[0]
    hypothesis = registry.parse_hypotheses([{**HYPOTHESIS, "justification": ["S-99"]}])[0]
    claims = registry.parse_claims(
        [{"id": "M-01", "type": "measure", "title": "m", "depends_on": ["H-77"]}]
    )
    errors = registry.cross_check([source, source], [orphan_def], [hypothesis], claims)
    assert any("duplicate id S-01" in e for e in errors)
    assert any("D-01: unknown source S-99" in e for e in errors)
    assert any("H-01: unknown source S-99" in e for e in errors)
    assert any("M-01: unknown dependency H-77" in e for e in errors)


@given(
    st.tuples(
        st.floats(allow_nan=False, allow_infinity=False, width=32),
        st.floats(allow_nan=False, allow_infinity=False, width=32),
        st.floats(allow_nan=False, allow_infinity=False, width=32),
    )
)
def test_hypothesis_validity_is_exactly_range_containment(
    values: tuple[float, float, float],
) -> None:
    """Property: a numeric hypothesis validates iff low <= central <= high."""
    low, central, high = values
    payload = {**HYPOTHESIS, "central_value": central, "plausible_range": [low, high]}
    if low <= central <= high:
        assert HypothesisRecord.model_validate(payload).central_value == central
    else:
        with pytest.raises(ValueError, match="plausible_range|outside"):
            HypothesisRecord.model_validate(payload)
