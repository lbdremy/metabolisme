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


def test_committed_cout_artifact_matches_rebuild() -> None:
    """data/processed/cout-residentiel-ze.json is exactly what the chain rebuilds."""
    root = project_root()
    committed = json.loads((root / build.COUT_OUTPUT).read_text(encoding="utf-8"))
    assert build.build_cout_residentiel(root) == committed


def test_committed_rs_artifact_matches_rebuild() -> None:
    """data/processed/residences-secondaires-ze.json matches a rebuild."""
    root = project_root()
    committed = json.loads((root / build.RS_OUTPUT).read_text(encoding="utf-8"))
    assert build.build_residences_secondaires(root) == committed


def test_committed_effort_artifact_matches_rebuild() -> None:
    """data/processed/taux-effort-relocation-ze.json matches a rebuild."""
    root = project_root()
    committed = json.loads((root / build.EFFORT_OUTPUT).read_text(encoding="utf-8"))
    assert build.build_taux_effort(root) == committed


def test_committed_tension_artifact_matches_rebuild() -> None:
    """data/processed/tension-manque-absolu-ze.json matches a rebuild."""
    root = project_root()
    committed = json.loads((root / build.TENSION_OUTPUT).read_text(encoding="utf-8"))
    assert build.build_tension(root) == committed


def test_committed_bati_artifact_matches_rebuild() -> None:
    """data/processed/etat-bati-ze.json matches a rebuild."""
    root = project_root()
    committed = json.loads((root / build.BATI_OUTPUT).read_text(encoding="utf-8"))
    assert build.build_etat_bati(root) == committed


def test_committed_remob_artifact_matches_rebuild() -> None:
    """data/processed/cout-remobilisation-ze.json matches a rebuild."""
    root = project_root()
    committed = json.loads((root / build.REMOB_OUTPUT).read_text(encoding="utf-8"))
    assert build.build_cout_remobilisation(root) == committed


def test_committed_foncier_artifact_matches_rebuild() -> None:
    """data/processed/foncier-friches-ze.json matches a rebuild."""
    root = project_root()
    committed = json.loads((root / build.FONCIER_OUTPUT).read_text(encoding="utf-8"))
    assert build.build_foncier(root) == committed


def test_committed_mobilite_artifact_matches_rebuild() -> None:
    """data/processed/mobilite-residentielle-ze.json matches a rebuild."""
    root = project_root()
    committed = json.loads((root / build.MOBILITE_OUTPUT).read_text(encoding="utf-8"))
    assert build.build_mobilite(root) == committed


def test_committed_social_artifact_matches_rebuild() -> None:
    """data/processed/mobilite-parc-social-ze.json matches a rebuild."""
    root = project_root()
    committed = json.loads((root / build.SOCIAL_OUTPUT).read_text(encoding="utf-8"))
    assert build.build_social(root) == committed
