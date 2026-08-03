"""`logement reproduce` — replay every stabilized pipeline stage from raw data.

No stage exists yet: the command says so honestly instead of faking work. As
transformations are stabilized into `core/`, each becomes a stage listed and
re-run here, so `uv run logement reproduce` always rebuilds every published
result (method INTRO §6.8).
"""

from __future__ import annotations


def run() -> int:
    """Re-run the (currently empty) evidence chain; return a process exit code.

    Will grow a `root: Path` argument with the first real stage.
    """
    print("reproduce: the evidence chain has no stabilized stage yet — nothing to rebuild.")
    print("reproduce: registries are gated separately by `logement validate`.")
    return 0
