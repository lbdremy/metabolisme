"""Parse-at-the-boundary types (pydantic v2).

Same trust boundary as `logement/src/logement/models.py`:
- `StrictModel` (`extra="forbid"`) for data WE own — the evidence registries
  (`sources.yaml`, `definitions.yaml`, `hypotheses.yaml`), claims, artifacts we
  parse back. A stray/typo'd key is an error, not a silent drop.
- `SubsetModel` (`extra="ignore"`, `from_attributes`) for third-party payloads we
  don't control (ART workbooks, company accounts) — read the fields we need.

This study's registries carry the four fields the `monopoles/` framing added
to the site contract and that logement's models do not know (monopoles/
CLAUDE.md): a hypothesis may be QUALITATIVE (`statement`, no numeric
triple) and carry `limitations`; a definition may be CONSTRUCTED
(`constructed_by`, a C-xx node); a source may be non-`redistributable`.
The schemas below accept exactly those extensions and nothing else.
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

SourceId = Annotated[str, Field(pattern=r"^S-\d{2,}$")]
DefinitionId = Annotated[str, Field(pattern=r"^D-\d{2,}$")]
HypothesisId = Annotated[str, Field(pattern=r"^H-\d{2,}$")]
ChoiceId = Annotated[str, Field(pattern=r"^C-\d{2,}$")]
# Justifications / dependencies may point at any status (S/D/O/T/M/H/R/I/V/C/P/L).
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
    publication_date: dt.date | None
    retrieved_at: dt.date
    geographic_scope: str
    temporal_scope: str
    license: str
    dataset_id: str | None = None
    local_file: str | None = None
    checksum: str | None = Field(default=None, pattern=r"^sha256:[0-9a-f]{64}$")
    files: list[FrozenFile] = Field(default_factory=list)
    # False when the frozen copy is kept for verification but must not be
    # served by the site (redistribution rights not established).
    redistributable: bool = True
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
    """One definition, tied to its source; constructed notions name their choice (INTRO §8)."""

    id: DefinitionId
    term: str
    source: SourceId
    definition: str
    # The C-xx node that formulates a notion the study builds (the source then
    # anchors the notion without defining it — monopoles/ convention).
    constructed_by: ChoiceId | None = None
    url: str | None = None
    last_updated: dt.date | None = None
    caveats: list[str] = Field(default_factory=list)


# ------------------------------------------------------------ hypotheses.yaml (§9)


class HypothesisRecord(StrictModel):
    """One hypothesis: a named parameter (value, range, unit) OR a qualitative statement."""

    id: HypothesisId
    name: str
    description: str
    central_value: float | None = None
    plausible_range: tuple[float, float] | None = None
    unit: str | None = None
    statement: str | None = None
    confidence: Literal["low", "medium", "high"]
    justification: list[EvidenceId] = Field(default_factory=list)
    limitations: list[EvidenceId] = Field(default_factory=list)
    affects: list[EvidenceId] = Field(default_factory=list)

    @model_validator(mode="after")
    def _quantified_or_stated(self) -> HypothesisRecord:
        """Require a complete numeric triple or a statement — never neither, never half."""
        numeric = (self.central_value, self.plausible_range, self.unit)
        quantified = all(field is not None for field in numeric)
        if not quantified and any(field is not None for field in numeric):
            msg = f"{self.id}: central_value, plausible_range and unit go together"
            raise ValueError(msg)
        if not quantified and self.statement is None:
            msg = f"{self.id}: a hypothesis is a numeric parameter or carries a statement"
            raise ValueError(msg)
        if quantified:
            assert self.plausible_range is not None
            assert self.central_value is not None
            low, high = self.plausible_range
            if not low <= high:
                msg = f"{self.id}: plausible_range is not ordered ({low} > {high})"
                raise ValueError(msg)
            if not low <= self.central_value <= high:
                msg = f"{self.id}: central_value {self.central_value} outside [{low}, {high}]"
                raise ValueError(msg)
        return self

    @property
    def is_quantified(self) -> bool:
        """True for a numeric parameter (value, range, unit all present)."""
        return self.central_value is not None


# ------------------------------------------------------------- claims.yaml (§10)

ClaimType = Literal[
    "observation",
    "transformation",
    "measure",
    "result",
    "interpretation",
    "value",
    "choice",
    "proposal",
    "limit",
]

CLAIM_PREFIXES: dict[str, ClaimType] = {
    "O": "observation",
    "T": "transformation",
    "M": "measure",
    "R": "result",
    "I": "interpretation",
    "V": "value",
    "C": "choice",
    "P": "proposal",
    "L": "limit",
}


class ClaimRecord(StrictModel):
    """One node of the evidence graph: what it is, what it depends on (INTRO §10)."""

    id: EvidenceId
    type: ClaimType
    title: str
    depends_on: list[EvidenceId] = Field(default_factory=list)
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


# ------------------------------------------------- data/transcribed/*.csv (T-01)


class TranscribedRow(StrictModel):
    """One hand-transcribed figure: entity, year, item, value (M€), source id and page."""

    entity: str
    year: int
    item: str
    value_meur: float
    source: SourceId
    page: int
    note: str = ""
