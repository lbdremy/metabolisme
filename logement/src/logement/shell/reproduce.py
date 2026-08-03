"""`logement reproduce` — replay every stabilized pipeline stage from raw data.

Each stabilized stage is listed here and re-run in order, so
`uv run logement reproduce` always rebuilds every published result from the
frozen raw files (method INTRO §6.8). The regression test in
tests/test_reproduce.py asserts the committed artifacts match a rebuild.
"""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path

from logement.shell import build

STAGES: tuple[tuple[str, Callable[[Path], int]], ...] = (
    ("parc-menages", build.run),
    ("vacance-structurelle", build.run_vacance),
)


def run(root: Path) -> int:
    """Re-run every stage of the evidence chain; return a process exit code."""
    for name, stage in STAGES:
        print(f"reproduce: stage {name}")
        code = stage(root)
        if code != 0:
            print(f"reproduce: stage {name} FAILED ({code})")
            return code
    print(f"reproduce: {len(STAGES)} stage(s) rebuilt.")
    return 0
