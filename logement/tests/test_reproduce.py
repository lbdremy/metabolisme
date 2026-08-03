"""Regression test (method INTRO §6.7): the committed R-01 artifact must match
a rebuild from the frozen raw files. A legitimate change (new source, revised
data, corrected transform) shows up as a diff here and must be re-committed
and explained — never silent.
"""

from __future__ import annotations

import json

from logement.config import project_root
from logement.shell import build


def test_committed_parc_menages_artifact_matches_rebuild() -> None:
    """data/processed/parc-menages.json is exactly what the chain rebuilds."""
    root = project_root()
    committed = json.loads((root / build.OUTPUT).read_text(encoding="utf-8"))
    assert build.build_parc_menages(root) == committed


def test_committed_vacance_artifact_matches_rebuild() -> None:
    """data/processed/vacance-structurelle.json is exactly what the chain rebuilds."""
    root = project_root()
    committed = json.loads((root / build.LOVAC_OUTPUT).read_text(encoding="utf-8"))
    assert build.build_vacance_structurelle(root) == committed


def test_committed_ze_artifact_matches_rebuild() -> None:
    """data/processed/vacance-emploi-ze.json is exactly what the chain rebuilds."""
    root = project_root()
    committed = json.loads((root / build.ZE_OUTPUT).read_text(encoding="utf-8"))
    assert build.build_vacance_emploi(root) == committed
