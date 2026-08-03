"""Parse-at-the-boundary types (pydantic v2).

Two base classes encode the trust boundary:
- `StrictModel` (`extra="forbid"`) for data WE own — the evidence registries
  (`sources.yaml`, `definitions.yaml`, `hypotheses.yaml`), claims, artifacts we
  parse back. A stray/typo'd key is an error, not a silent drop.
- `SubsetModel` (`extra="ignore"`, `from_attributes`) for third-party payloads we
  don't control (INSEE/SDES files, API responses) — read the fields we need.

Never flow a raw dict downstream: `model_validate` it at the edge, then work with
types. `Any` is banned in signatures (ANN401) — type a raw payload as `object` and
parse it.

The record schemas mirror the method INTRO (§7 sources, §8 definitions,
§9 hypotheses); epistemic-status ids (`S-01`, `D-01`, `H-03`, …) are validated
by pattern so a claim can never reference a malformed id.
"""

from __future__ import annotations

import datetime as dt
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


class StrictModel(BaseModel):
    """Base for data we own — unknown keys are a hard error."""

    model_config = ConfigDict(extra="forbid")


class SubsetModel(BaseModel):
    """Base for third-party payloads — read the fields we need, ignore the rest."""

    model_config = ConfigDict(extra="ignore", from_attributes=True)


# ------------------------------------------------------------------ epistemic ids
# One pattern per status used in the registries; claims will reuse them later.

SourceId = Annotated[str, Field(pattern=r"^S-\d{2,}$")]
DefinitionId = Annotated[str, Field(pattern=r"^D-\d{2,}$")]
HypothesisId = Annotated[str, Field(pattern=r"^H-\d{2,}$")]
# Justifications / affected results may point at any status (S/D/O/T/M/H/R/I/V/C/P/L).
EvidenceId = Annotated[str, Field(pattern=r"^[SDOTMHRIVCPL]-\d{2,}$")]


# --------------------------------------------------------------- sources.yaml (§7)


class FrozenFile(StrictModel):
    """One frozen file of a source: repo-relative path + sha256 of its bytes."""

    path: str
    checksum: str = Field(pattern=r"^sha256:[0-9a-f]{64}$")


class SourceRecord(StrictModel):
    """One retained source: identified, dated, scoped, checksummed (INTRO §7)."""

    id: SourceId
    publisher: str
    title: str
    source_url: str
    # None for living collections (e.g. a definitions registry) that have no
    # single publication date — each derived record then carries its own date.
    publication_date: dt.date | None
    retrieved_at: dt.date
    geographic_scope: str
    temporal_scope: str
    license: str
    dataset_id: str | None = None
    # Single-file sources: path relative to the project root + checksum.
    # None while the source is registered but not yet frozen locally.
    local_file: str | None = None
    checksum: str | None = Field(default=None, pattern=r"^sha256:[0-9a-f]{64}$")
    # Multi-file sources (e.g. a dataset shipping data + schema + summaries).
    files: list[FrozenFile] = Field(default_factory=list)
    notes: str = ""

    @model_validator(mode="after")
    def _frozen_files_are_checksummed(self) -> SourceRecord:
        """Reject a frozen local file without a checksum — it can't prove its version."""
        if self.local_file is not None and self.checksum is None:
            msg = f"{self.id}: local_file is set but checksum is missing"
            raise ValueError(msg)
        if self.local_file is not None and self.files:
            msg = f"{self.id}: use either local_file or files, not both"
            raise ValueError(msg)
        return self

    @property
    def frozen_files(self) -> list[FrozenFile]:
        """All frozen files of this source, whatever the declaration style."""
        if self.local_file is not None and self.checksum is not None:
            return [FrozenFile(path=self.local_file, checksum=self.checksum)]
        return self.files


# ----------------------------------------------------------- definitions.yaml (§8)


class DefinitionRecord(StrictModel):
    """One statistical/legal/conceptual definition, tied to its source (INTRO §8)."""

    id: DefinitionId
    term: str
    source: SourceId
    definition: str
    # The definition's own page within the source (e.g. an INSEE metadata page)
    # and its "dernière mise à jour" date as published there.
    url: str | None = None
    last_updated: dt.date | None = None
    caveats: list[str] = Field(default_factory=list)


# ------------------------------------------------------------ hypotheses.yaml (§9)


class HypothesisRecord(StrictModel):
    """One named model parameter: central value, plausible range, lineage (INTRO §9)."""

    id: HypothesisId
    name: str
    description: str
    central_value: float
    plausible_range: tuple[float, float]
    unit: str
    confidence: Literal["low", "medium", "high"]
    justification: list[EvidenceId] = Field(default_factory=list)
    affects: list[EvidenceId] = Field(default_factory=list)

    @model_validator(mode="after")
    def _central_value_inside_range(self) -> HypothesisRecord:
        """Require an ordered plausible range that contains the central value."""
        low, high = self.plausible_range
        if not low <= high:
            msg = f"{self.id}: plausible_range is not ordered ({low} > {high})"
            raise ValueError(msg)
        if not low <= self.central_value <= high:
            msg = f"{self.id}: central_value {self.central_value} outside [{low}, {high}]"
            raise ValueError(msg)
        return self


# ------------------------------------------------------------- claims.yaml (§10)

ClaimType = Literal[
    "observation",
    "transformation",
    "measure",
    "result",
    "interpretation",
    "value",
    "choice",
    "proposition",
    "limit",
]

# Claims carry the non-registry statuses; S/D/H live in their own registries.
CLAIM_PREFIXES: dict[str, ClaimType] = {
    "O": "observation",
    "T": "transformation",
    "M": "measure",
    "R": "result",
    "I": "interpretation",
    "V": "value",
    "C": "choice",
    "P": "proposition",
    "L": "limit",
}


class ClaimRecord(StrictModel):
    """One node of the evidence graph: what it is, what it depends on (INTRO §10)."""

    id: EvidenceId
    type: ClaimType
    title: str
    depends_on: list[EvidenceId] = Field(default_factory=list)
    # For computed nodes: the code that produces it and the artifact written.
    produced_by: str | None = None
    output: str | None = None
    limitations: list[EvidenceId] = Field(default_factory=list)
    notes: str = ""

    @model_validator(mode="after")
    def _type_matches_id_prefix(self) -> ClaimRecord:
        """Require the declared type to agree with the id's status prefix."""
        expected = CLAIM_PREFIXES.get(self.id[0])
        if expected is None:
            msg = f"{self.id}: S/D/H ids belong to the sources/ registries, not claims"
            raise ValueError(msg)
        if self.type != expected:
            msg = f"{self.id}: type '{self.type}' does not match prefix ('{expected}' expected)"
            raise ValueError(msg)
        return self
