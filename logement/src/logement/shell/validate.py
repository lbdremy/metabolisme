"""`logement validate` — read the registries, run the pure checks, report.

Effects live here (file reads, hashing); the parsing and cross-checks are the
pure functions in `core/registry.py`.
"""

from __future__ import annotations

import hashlib
from pathlib import Path

import yaml

from logement.core import registry
from logement.models import SourceRecord


def _load_yaml(path: Path) -> object:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _check_local_files(root: Path, sources: list[SourceRecord]) -> list[str]:
    """Verify that each frozen source file exists and matches its recorded sha256."""
    errors: list[str] = []
    for source in sources:
        if source.local_file is None:
            continue
        path = root / source.local_file
        if not path.is_file():
            errors.append(f"{source.id}: local_file {source.local_file} not found")
            continue
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        recorded = (source.checksum or "").removeprefix("sha256:")
        if digest != recorded:
            errors.append(f"{source.id}: checksum mismatch for {source.local_file}")
    return errors


def run(root: Path) -> int:
    """Validate the three registries; return a process exit code."""
    paths = {
        "sources": root / "sources" / "sources.yaml",
        "definitions": root / "sources" / "definitions.yaml",
        "hypotheses": root / "sources" / "hypotheses.yaml",
        "claims": root / "evidence" / "claims.yaml",
    }
    missing = [str(p) for p in paths.values() if not p.is_file()]
    if missing:
        for path in missing:
            print(f"validate: missing registry file {path}")
        return 1

    try:
        sources = registry.parse_sources(_load_yaml(paths["sources"]))
        definitions = registry.parse_definitions(_load_yaml(paths["definitions"]))
        hypotheses = registry.parse_hypotheses(_load_yaml(paths["hypotheses"]))
        claims = registry.parse_claims(_load_yaml(paths["claims"]))
    except registry.RegistryError as exc:
        print(f"validate: {exc}")
        return 1

    errors = registry.cross_check(sources, definitions, hypotheses, claims)
    errors += _check_local_files(root, sources)
    errors += [
        f"{claim.id}: declared output {claim.output} not found"
        for claim in claims
        if claim.output is not None and not (root / claim.output).is_file()
    ]
    for error in errors:
        print(f"validate: {error}")

    print(
        f"validate: {len(sources)} source(s), {len(definitions)} definition(s), "
        f"{len(hypotheses)} hypothesis(es), {len(claims)} claim(s) — "
        f"{'RED' if errors else 'green'}"
    )
    return 1 if errors else 0
