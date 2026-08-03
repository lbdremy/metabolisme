"""Build stages — rebuild the R-xx artifacts from the frozen raw files.

Each stage reads its sources from data/raw/, runs the pure core and writes
the committed artifact declared by the matching result in evidence/claims.yaml.
"""

from __future__ import annotations

import json
import zipfile
from pathlib import Path

import pandas as pd

from logement.core import lovac, parc, ze

S01_FILE = "insee-focus-359-parc-logements-2025.xlsx"
S02_FILE = "insee-eapl-parc-residence-2025.xlsx"
S03_FILE = "insee-rp-menages-series-longues-2022.xlsx"
OUTPUT = Path("data") / "processed" / "parc-menages.json"

LOVAC_FRANCE = "lovac-opendata-france26.csv"
LOVAC_DEPARTEMENTS = "lovac-opendata-departements26.csv"
LOVAC_COMMUNES = "lovac-opendata-communes26.csv"
LOVAC_OUTPUT = Path("data") / "processed" / "vacance-structurelle.json"

APPARTENANCE_ZIP = "insee-table-appartenance-geo-communes-2026.zip"
APPARTENANCE_XLSX = "table-appartenance-geo-communes-2026.xlsx"
EMPLOI_ZE_FILE = "insee-emploi-zone-1998-2018.xlsx"
ZE_OUTPUT = Path("data") / "processed" / "vacance-emploi-ze.json"


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


def _write_json(root: Path, output: Path, payload: dict[str, object]) -> None:
    out = root / output
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def run(root: Path) -> int:
    """Rebuild data/processed/parc-menages.json; return a process exit code."""
    payload = build_parc_menages(root)
    _write_json(root, OUTPUT, payload)
    indices = payload["indices_at_last_common_vintage"]
    print(f"parc-menages: wrote {OUTPUT} — indices {indices}")
    return 0


def _read_lovac(root: Path, name: str) -> pd.DataFrame:
    return pd.read_csv(root / "data" / "raw" / name, sep=";", encoding="cp1252", dtype=str)


def build_vacance_structurelle(root: Path) -> dict[str, object]:
    """Compute the R-02 summary payload from the frozen LOVAC files."""
    france = lovac.parse_france(_read_lovac(root, LOVAC_FRANCE))
    departements = lovac.parse_territories(
        _read_lovac(root, LOVAC_DEPARTEMENTS), code_col="DEP", name_col="LIB_DEP"
    )
    communes = lovac.parse_territories(
        _read_lovac(root, LOVAC_COMMUNES), code_col="CODGEO_26", name_col="LIBGEO_26"
    )
    return lovac.build_summary(france, departements, communes)


def run_vacance(root: Path) -> int:
    """Rebuild data/processed/vacance-structurelle.json; return a process exit code."""
    payload = build_vacance_structurelle(root)
    _write_json(root, LOVAC_OUTPUT, payload)
    national = payload["national"]
    print(f"vacance-structurelle: wrote {LOVAC_OUTPUT} — national {national}")
    return 0


def build_vacance_emploi(root: Path) -> dict[str, object]:
    """Compute the R-03 summary payload (vacancy × employment by ZE)."""
    raw = root / "data" / "raw"
    with zipfile.ZipFile(raw / APPARTENANCE_ZIP) as zf, zf.open(APPARTENANCE_XLSX) as fh:
        # The INSEE stylesheet breaks openpyxl; calamine reads it (S-06 note).
        membership = pd.read_excel(fh, sheet_name="COM", header=5, engine="calamine", dtype=str)
    commune_ze = ze.parse_commune_ze(membership)
    emploi = ze.parse_emploi_ze(
        pd.read_excel(
            raw / EMPLOI_ZE_FILE, sheet_name="Emploi total - ZE", header=4, engine="calamine"
        )
    )
    communes = lovac.parse_territories(
        _read_lovac(root, LOVAC_COMMUNES), code_col="CODGEO_26", name_col="LIBGEO_26"
    )
    vacancy_ze, unmatched = ze.aggregate_vacancy_by_ze(communes, commune_ze)
    return ze.build_summary(vacancy_ze, emploi, unmatched)


def run_vacance_emploi(root: Path) -> int:
    """Rebuild data/processed/vacance-emploi-ze.json; return a process exit code."""
    payload = build_vacance_emploi(root)
    _write_json(root, ZE_OUTPUT, payload)
    print(
        f"vacance-emploi: wrote {ZE_OUTPUT} — spearman "
        f"{payload['spearman_rate_vs_growth']}, declining {payload['declining_ze']}"
    )
    return 0
