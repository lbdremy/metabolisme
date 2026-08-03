"""Project-root resolution for the study's on-disk artifacts."""

from __future__ import annotations

from pathlib import Path


def project_root() -> Path:
    """Return the logement/ project root (the folder holding pyproject.toml).

    Resolved relative to this file — the package is installed editable by
    `uv sync`, so `src/logement/config.py` always sits two levels below root.
    """
    return Path(__file__).resolve().parents[2]
