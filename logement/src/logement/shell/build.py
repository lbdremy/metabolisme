"""Stage 'parc-menages' — rebuild R-01 from the frozen raw files.

Reads S-01/S-02/S-03 from data/raw/, runs the pure core (core/parc.py) and
writes the committed artifact data/processed/parc-menages.json (the output
declared by R-01 in evidence/claims.yaml).
"""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from logement.core import parc

S01_FILE = "insee-focus-359-parc-logements-2025.xlsx"
S02_FILE = "insee-eapl-parc-residence-2025.xlsx"
S03_FILE = "insee-rp-menages-series-longues-2022.xlsx"
OUTPUT = Path("data") / "processed" / "parc-menages.json"


def build_parc_menages(root: Path) -> dict[str, object]:
    """Compute the R-01 summary payload from the frozen raw files."""
    raw = root / "data" / "raw"
    categories = parc.parse_eapl_categories(
        pd.read_excel(raw / S02_FILE, sheet_name="Données", header=3)
    )
    menages = parc.parse_menages_totals(
        pd.read_excel(raw / S03_FILE, sheet_name="France", header=None)
    )
    population_index = parc.parse_population_index(
        pd.read_excel(raw / S01_FILE, sheet_name="Figure 2", header=2)
    )
    return parc.build_summary(categories, menages, population_index)


def run(root: Path) -> int:
    """Rebuild data/processed/parc-menages.json; return a process exit code."""
    payload = build_parc_menages(root)
    out = root / OUTPUT
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    indices = payload["indices_at_last_common_vintage"]
    print(f"parc-menages: wrote {OUTPUT} — indices {indices}")
    return 0
