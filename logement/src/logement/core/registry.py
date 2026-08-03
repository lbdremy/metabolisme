"""Pure parsing and cross-checking of the evidence registries.

Takes already-loaded YAML payloads (plain Python objects) and returns typed
records / error lists — no I/O, no clock. The imperative shell
(`shell/validate.py`) reads the files and reports.
"""

from __future__ import annotations

from typing import TypeVar

from pydantic import ValidationError

from logement.models import DefinitionRecord, HypothesisRecord, SourceRecord

T = TypeVar("T", SourceRecord, DefinitionRecord, HypothesisRecord)


class RegistryError(Exception):
    """A registry file's payload is structurally invalid."""


def _parse_entries(raw: object, model: type[T], registry: str) -> list[T]:
    if raw is None:
        return []
    if not isinstance(raw, list):
        msg = f"{registry}: expected a YAML list of records, got {type(raw).__name__}"
        raise RegistryError(msg)
    entries: list[T] = []
    for index, item in enumerate(raw):
        try:
            entries.append(model.model_validate(item))
        except ValidationError as exc:
            msg = f"{registry}[{index}]: {exc}"
            raise RegistryError(msg) from exc
    return entries


def parse_sources(raw: object) -> list[SourceRecord]:
    """Parse the sources.yaml payload into typed source records."""
    return _parse_entries(raw, SourceRecord, "sources")


def parse_definitions(raw: object) -> list[DefinitionRecord]:
    """Parse the definitions.yaml payload into typed definition records."""
    return _parse_entries(raw, DefinitionRecord, "definitions")


def parse_hypotheses(raw: object) -> list[HypothesisRecord]:
    """Parse the hypotheses.yaml payload into typed hypothesis records."""
    return _parse_entries(raw, HypothesisRecord, "hypotheses")


def cross_check(
    sources: list[SourceRecord],
    definitions: list[DefinitionRecord],
    hypotheses: list[HypothesisRecord],
) -> list[str]:
    """Referential checks across the three registries; returns human-readable errors.

    Checks: unique ids per registry, definitions pointing at registered sources,
    hypothesis justifications whose `S-xx` references exist. References to other
    statuses (O/T/M/R/I/…) will be checked once `evidence/claims.yaml` exists.
    """
    errors: list[str] = []

    for registry, ids in (
        ("sources", [s.id for s in sources]),
        ("definitions", [d.id for d in definitions]),
        ("hypotheses", [h.id for h in hypotheses]),
    ):
        seen: set[str] = set()
        for record_id in ids:
            if record_id in seen:
                errors.append(f"{registry}: duplicate id {record_id}")
            seen.add(record_id)

    source_ids = {s.id for s in sources}
    for definition in definitions:
        if definition.source not in source_ids:
            errors.append(f"{definition.id}: unknown source {definition.source}")
    for hypothesis in hypotheses:
        for ref in hypothesis.justification:
            if ref.startswith("S-") and ref not in source_ids:
                errors.append(f"{hypothesis.id}: unknown source {ref} in justification")

    return errors
