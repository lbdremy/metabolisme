"""Behaviour tests for the pure registry core (parse + cross-check)."""

from __future__ import annotations

import pytest
from hypothesis import given
from hypothesis import strategies as st

from logement.core import registry
from logement.models import HypothesisRecord

SOURCE = {
    "id": "S-01",
    "publisher": "INSEE",
    "title": "Parc de logements par catégorie",
    "source_url": "https://example.invalid/parc-logements",
    "publication_date": "2025-06-12",
    "retrieved_at": "2026-08-03",
    "geographic_scope": "France",
    "temporal_scope": "2023",
    "license": "Licence Ouverte 2.0",
}

DEFINITION = {
    "id": "D-01",
    "term": "logement vacant",
    "source": "S-01",
    "definition": "Logement inoccupé au sens de la source.",
    "caveats": ["Peut inclure une vacance temporaire."],
}

HYPOTHESIS = {
    "id": "H-01",
    "name": "frictional_vacancy_rate",
    "description": "Part de la vacance correspondant à une rotation normale",
    "central_value": 0.10,
    "plausible_range": [0.07, 0.15],
    "unit": "ratio",
    "confidence": "medium",
    "justification": ["S-01"],
    "affects": ["R-01"],
}


def test_empty_registries_parse_to_empty_lists() -> None:
    """A `[]` (or missing → None) payload is a valid, empty registry."""
    assert registry.parse_sources([]) == []
    assert registry.parse_definitions(None) == []
    assert registry.parse_hypotheses([]) == []


def test_full_records_round_trip() -> None:
    """The INTRO's example records parse into typed models."""
    (source,) = registry.parse_sources([SOURCE])
    (definition,) = registry.parse_definitions([DEFINITION])
    (hypothesis,) = registry.parse_hypotheses([HYPOTHESIS])
    assert source.id == "S-01"
    assert definition.source == "S-01"
    assert hypothesis.plausible_range == (0.07, 0.15)
    assert registry.cross_check([source], [definition], [hypothesis]) == []


@pytest.mark.parametrize(
    ("payload", "registry_name"),
    [
        ({"not": "a list"}, "sources"),
        ([{**SOURCE, "typo_key": 1}], "sources"),
        ([{**SOURCE, "id": "X-01"}], "sources"),
        ([{**SOURCE, "local_file": "data/raw/x.csv"}], "sources"),  # frozen but unchecksummed
        (  # local_file and files are mutually exclusive declaration styles
            [
                {
                    **SOURCE,
                    "local_file": "data/raw/x.csv",
                    "checksum": "sha256:" + "0" * 64,
                    "files": [{"path": "data/raw/y.csv", "checksum": "sha256:" + "0" * 64}],
                }
            ],
            "sources",
        ),
        ([{**HYPOTHESIS, "central_value": 0.5}], "hypotheses"),  # outside plausible_range
        ([{**HYPOTHESIS, "plausible_range": [0.15, 0.07]}], "hypotheses"),  # unordered
        ([{**HYPOTHESIS, "confidence": "certain"}], "hypotheses"),  # not a valid level
    ],
)
def test_invalid_payloads_are_rejected(payload: object, registry_name: str) -> None:
    """Strict models make malformed registry entries loud errors, not silent drops."""
    parse = {
        "sources": registry.parse_sources,
        "hypotheses": registry.parse_hypotheses,
    }[registry_name]
    with pytest.raises(registry.RegistryError):
        parse(payload)


def test_cross_check_flags_duplicates_and_dangling_references() -> None:
    """Duplicate ids and references to unregistered sources must surface."""
    source = registry.parse_sources([SOURCE])[0]
    orphan_def = registry.parse_definitions([{**DEFINITION, "source": "S-99"}])[0]
    hypothesis = registry.parse_hypotheses([{**HYPOTHESIS, "justification": ["S-99"]}])[0]
    errors = registry.cross_check([source, source], [orphan_def], [hypothesis])
    assert any("duplicate id S-01" in e for e in errors)
    assert any("D-01: unknown source S-99" in e for e in errors)
    assert any("H-01: unknown source S-99" in e for e in errors)


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
    """Property: a hypothesis validates iff low <= central <= high."""
    low, central, high = values
    payload = {**HYPOTHESIS, "central_value": central, "plausible_range": [low, high]}
    if low <= central <= high:
        assert HypothesisRecord.model_validate(payload).central_value == central
    else:
        with pytest.raises(ValueError, match="plausible_range|outside"):
            HypothesisRecord.model_validate(payload)
