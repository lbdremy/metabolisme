"""Regression test (method INTRO §6.7): the committed artifact must match a rebuild.

A legitimate change (new source, revised transcription, corrected transform)
shows up as a diff here and must be re-committed and explained — never silent.
"""

from __future__ import annotations

import json

from autoroutes.config import project_root
from autoroutes.shell import build


def test_committed_rent_artifact_matches_rebuild() -> None:
    """data/processed/rente-d15.json is exactly what the chain rebuilds."""
    root = project_root()
    committed = json.loads((root / build.RENT_OUTPUT).read_text(encoding="utf-8"))
    assert build.build_rent(root) == committed


def test_transcribed_balance_sheets_close() -> None:
    """Every transcribed group's gross − amortisation − subsidies ≈ its published net value."""
    payload = build.build_rent(project_root())
    checks = payload["balance_sheet_checks"]
    assert isinstance(checks, dict) and all(checks.values()), checks


def test_surplus_sign_is_stable_across_bases_and_rates() -> None:
    """The published headline: positive at both bounds of H-01, on both bases (2023)."""
    payload = build.build_rent(project_root())
    groups = payload["m01_groups"]
    assert isinstance(groups, dict)
    for records in groups.values():
        total = next(r for r in records if r["company"] == "Trois groupes mesurés")
        assert total["surplus_reference_low"] > 0 and total["surplus_reference_high"] > 0
