"""Build stages — rebuild the R-xx artifacts from the frozen raw files.

Each stage reads its sources from data/raw/, runs the pure core and writes
the committed artifact declared by the matching result in evidence/claims.yaml.
"""

from __future__ import annotations

import json
import zipfile
from pathlib import Path

import pandas as pd
import yaml

from logement.core import (
    bati,
    cout,
    effort,
    foncier,
    lovac,
    parc,
    registry,
    remob,
    rs,
    tension,
    ze,
)
from logement.models import HypothesisRecord

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

LOYERS_FILE = "carte-loyers-2025-appartement.csv"
FILOSOFI_ZIP = "insee-filosofi-2021-geo2025.zip"
FILOSOFI_CSV = "DS_FILOSOFI_CC_data.csv"
COUT_OUTPUT = Path("data") / "processed" / "cout-residentiel-ze.json"

CENSUS_ZIP = "insee-rp-base-cc-logement-2022.zip"
CENSUS_CSV = "base-cc-logement-2022.CSV"
RS_OUTPUT = Path("data") / "processed" / "residences-secondaires-ze.json"

LOYERS_MAISON_FILE = "carte-loyers-2025-maison.csv"
EFFORT_OUTPUT = Path("data") / "processed" / "taux-effort-relocation-ze.json"

TLV_FILE = "zonage-tlv-decret-2025-12-22.csv"
TENSION_OUTPUT = Path("data") / "processed" / "tension-manque-absolu-ze.json"

DPE_FILE = "ademe-dpe-existants-communes-etiquettes.csv"
BATI_OUTPUT = Path("data") / "processed" / "etat-bati-ze.json"

IPEA_FILE = "insee-ipea-residentiel-011779962.xml"
REMOB_OUTPUT = Path("data") / "processed" / "cout-remobilisation-ze.json"

FRICHES_FILE = "cerema-cartofriches-2026-06-15.csv"
COMPARATEUR_ZIP = "insee-comparateur-territoires-2026.zip"
COMPARATEUR_CSV = "comparateur.csv"
FONCIER_OUTPUT = Path("data") / "processed" / "foncier-friches-ze.json"


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


def _read_membership(root: Path) -> pd.DataFrame:
    raw = root / "data" / "raw"
    with zipfile.ZipFile(raw / APPARTENANCE_ZIP) as zf, zf.open(APPARTENANCE_XLSX) as fh:
        return pd.read_excel(fh, sheet_name="COM", header=5, engine="calamine", dtype=str)


def _cost_frame(root: Path) -> pd.DataFrame:
    """Build the per-ZE cost frame shared by the R-04 and R-05 stages."""
    raw = root / "data" / "raw"
    loyers = cout.parse_loyers(
        pd.read_csv(raw / LOYERS_FILE, sep=";", encoding="cp1252", dtype=str)
    )
    with zipfile.ZipFile(raw / FILOSOFI_ZIP) as zf, zf.open(FILOSOFI_CSV) as fh:
        filosofi = pd.read_csv(
            fh, sep=";", dtype=str, usecols=["GEO", "GEO_OBJECT", "FILOSOFI_MEASURE", "OBS_VALUE"]
        )
    niveau_vie = cout.parse_filosofi(filosofi, geo_object="ZE2020", measure="MED_SL")
    commune_ze = ze.parse_commune_ze(_read_membership(root))
    communes = lovac.parse_territories(
        _read_lovac(root, LOVAC_COMMUNES), code_col="CODGEO_26", name_col="LIBGEO_26"
    )
    return cout.cost_index_by_ze(loyers, communes, commune_ze, niveau_vie)


def _ze_names(root: Path) -> pd.Series:
    return ze.parse_emploi_ze(
        pd.read_excel(
            root / "data" / "raw" / EMPLOI_ZE_FILE,
            sheet_name="Emploi total - ZE",
            header=4,
            engine="calamine",
        )
    )["ze_name"]


def build_cout_residentiel(root: Path) -> dict[str, object]:
    """Compute the R-04 summary payload (cost-pressure index × vacancy by ZE)."""
    return cout.build_summary(_cost_frame(root), _ze_names(root))


def run_cout(root: Path) -> int:
    """Rebuild data/processed/cout-residentiel-ze.json; return a process exit code."""
    payload = build_cout_residentiel(root)
    _write_json(root, COUT_OUTPUT, payload)
    print(
        f"cout-residentiel: wrote {COUT_OUTPUT} — spearman "
        f"{payload['spearman_cost_vs_vacancy']}, medians {payload['median_vacancy_rate_pct']}"
    )
    return 0


def build_residences_secondaires(root: Path) -> dict[str, object]:
    """Compute the R-05 summary payload (secondary-residence share × cost/vacancy)."""
    raw = root / "data" / "raw"
    with zipfile.ZipFile(raw / CENSUS_ZIP) as zf, zf.open(CENSUS_CSV) as fh:
        census_raw = pd.read_csv(fh, sep=";", dtype=str, usecols=["CODGEO", *rs.CENSUS_COLS])
    census = rs.parse_census_housing(census_raw)
    commune_ze = ze.parse_commune_ze(_read_membership(root))
    rs_ze = rs.rs_by_ze(census, commune_ze)
    return rs.build_summary(rs_ze, _cost_frame(root), _ze_names(root))


def _load_hypothesis(root: Path, hypothesis_id: str) -> HypothesisRecord:
    """Load one named hypothesis from the registry (single source of truth)."""
    payload = yaml.safe_load((root / "sources" / "hypotheses.yaml").read_text(encoding="utf-8"))
    for record in registry.parse_hypotheses(payload):
        if record.id == hypothesis_id:
            return record
    raise effort.EffortError(f"hypothesis {hypothesis_id} not found in sources/hypotheses.yaml")


def build_taux_effort(root: Path) -> dict[str, object]:
    """Compute the R-06 summary payload (gross relocation effort rate by ZE)."""
    raw = root / "data" / "raw"
    loyers_appart = cout.parse_loyers(
        pd.read_csv(raw / LOYERS_FILE, sep=";", encoding="cp1252", dtype=str)
    )
    loyers_maison = cout.parse_loyers(
        pd.read_csv(raw / LOYERS_MAISON_FILE, sep=";", encoding="cp1252", dtype=str)
    )
    with zipfile.ZipFile(raw / CENSUS_ZIP) as zf, zf.open(CENSUS_CSV) as fh:
        census_raw = pd.read_csv(
            fh, sep=";", dtype=str, usecols=["CODGEO", *effort.CENSUS_MIX_COLS]
        )
    census_mix = effort.parse_census_mix(census_raw)
    with zipfile.ZipFile(raw / FILOSOFI_ZIP) as zf, zf.open(FILOSOFI_CSV) as fh:
        filosofi = pd.read_csv(
            fh, sep=";", dtype=str, usecols=["GEO", "GEO_OBJECT", "FILOSOFI_MEASURE", "OBS_VALUE"]
        )
    households = effort.household_frame(
        cout.parse_filosofi(filosofi, geo_object="ZE2020", measure="MED_SL"),
        cout.parse_filosofi(filosofi, geo_object="ZE2020", measure="NUM_PER"),
        cout.parse_filosofi(filosofi, geo_object="ZE2020", measure="NUM_CU"),
    )
    commune_ze = ze.parse_commune_ze(_read_membership(root))
    communes = lovac.parse_territories(
        _read_lovac(root, LOVAC_COMMUNES), code_col="CODGEO_26", name_col="LIBGEO_26"
    )
    h07 = _load_hypothesis(root, "H-07")
    frame = effort.effort_by_ze(
        loyers_appart,
        loyers_maison,
        census_mix,
        communes,
        commune_ze,
        households,
        h07.central_value,
    )
    return effort.build_summary(frame, _ze_names(root), h07)


def build_tension(root: Path) -> dict[str, object]:
    """Compute the R-07 summary payload (tension, absolute shortage, coverage)."""
    raw = root / "data" / "raw"
    with zipfile.ZipFile(raw / CENSUS_ZIP) as zf, zf.open(CENSUS_CSV) as fh:
        census_raw = pd.read_csv(fh, sep=";", dtype=str, usecols=["CODGEO", *rs.CENSUS_COLS])
    census = rs.parse_census_housing(census_raw)
    tlv = tension.parse_tlv(pd.read_csv(raw / TLV_FILE, sep=";", dtype=str))
    commune_ze = ze.parse_commune_ze(_read_membership(root))
    communes = lovac.parse_territories(
        _read_lovac(root, LOVAC_COMMUNES), code_col="CODGEO_26", name_col="LIBGEO_26"
    )
    h08 = _load_hypothesis(root, "H-08")
    frame = tension.tension_by_ze(census, tlv, communes, commune_ze, h08.central_value)
    return tension.build_summary(frame, _ze_names(root), h08)


def run_tension(root: Path) -> int:
    """Rebuild data/processed/tension-manque-absolu-ze.json; return an exit code."""
    payload = build_tension(root)
    _write_json(root, TENSION_OUTPUT, payload)
    print(
        f"tension: wrote {TENSION_OUTPUT} — national {payload['national']}, "
        f"couvertes {payload['ze_couvertes']}"
    )
    return 0


def build_etat_bati(root: Path) -> dict[str, object]:
    """Compute the R-08 summary payload (building condition × vacancy by ZE)."""
    raw = root / "data" / "raw"
    with zipfile.ZipFile(raw / CENSUS_ZIP) as zf, zf.open(CENSUS_CSV) as fh:
        census_raw = pd.read_csv(fh, sep=";", dtype=str, usecols=["CODGEO", *bati.CENSUS_BATI_COLS])
    census = bati.parse_census_bati(census_raw)
    dpe_raw = pd.read_csv(raw / DPE_FILE, sep=";", dtype=str)
    dpe_counts = bati.parse_dpe_counts(dpe_raw)
    commune_ze = ze.parse_commune_ze(_read_membership(root))
    communes = lovac.parse_territories(
        _read_lovac(root, LOVAC_COMMUNES), code_col="CODGEO_26", name_col="LIBGEO_26"
    )
    vacancy_ze, _unmatched = ze.aggregate_vacancy_by_ze(communes, commune_ze)
    return bati.build_summary(
        bati.bati_by_ze(census, commune_ze),
        bati.dpe_by_ze(dpe_counts, commune_ze),
        vacancy_ze,
        _ze_names(root),
        dpe_dropped_rows=dpe_counts.attrs["dropped_rows"],
    )


def run_bati(root: Path) -> int:
    """Rebuild data/processed/etat-bati-ze.json; return a process exit code."""
    payload = build_etat_bati(root)
    _write_json(root, BATI_OUTPUT, payload)
    print(
        f"etat-bati: wrote {BATI_OUTPUT} — spearman age×vacance "
        f"{payload['spearman_age_vs_vacancy']}, F+G×vacance {payload['spearman_fg_vs_vacancy']}"
    )
    return 0


def build_cout_remobilisation(root: Path) -> dict[str, object]:
    """Compute the R-09 summary payload (remobilisation cost vs building new)."""
    raw = root / "data" / "raw"
    with zipfile.ZipFile(raw / CENSUS_ZIP) as zf, zf.open(CENSUS_CSV) as fh:
        census_raw = pd.read_csv(fh, sep=";", dtype=str, usecols=["CODGEO", *rs.CENSUS_COLS])
    census = rs.parse_census_housing(census_raw)
    with zipfile.ZipFile(raw / CENSUS_ZIP) as zf, zf.open(CENSUS_CSV) as fh:
        mix_raw = pd.read_csv(fh, sep=";", dtype=str, usecols=["CODGEO", *effort.CENSUS_MIX_COLS])
    census_mix = effort.parse_census_mix(mix_raw)
    tlv = tension.parse_tlv(pd.read_csv(raw / TLV_FILE, sep=";", dtype=str))
    commune_ze = ze.parse_commune_ze(_read_membership(root))
    communes = lovac.parse_territories(
        _read_lovac(root, LOVAC_COMMUNES), code_col="CODGEO_26", name_col="LIBGEO_26"
    )
    h08 = _load_hypothesis(root, "H-08")
    frame = tension.tension_by_ze(census, tlv, communes, commune_ze, h08.central_value)
    tense = frame[frame["tendue"]]
    mix = (
        census_mix.merge(commune_ze, on="code", how="left")
        .dropna(subset=["ze"])
        .groupby("ze")[["rp_maison", "rp_appart"]]
        .sum()
    )
    part_maison = mix["rp_maison"] / (mix["rp_maison"] + mix["rp_appart"])
    annual_means = remob.parse_ipea_annual_means((raw / IPEA_FILE).read_text(encoding="utf-8"))
    return remob.build_summary(
        tense,
        part_maison,
        _ze_names(root),
        _load_hypothesis(root, "H-09"),
        _load_hypothesis(root, "H-10"),
        annual_means,
    )


def run_remob(root: Path) -> int:
    """Rebuild data/processed/cout-remobilisation-ze.json; return an exit code."""
    payload = build_cout_remobilisation(root)
    _write_json(root, REMOB_OUTPUT, payload)
    print(
        f"cout-remobilisation: wrote {REMOB_OUTPUT} — couts {payload['couts']}, "
        f"comparateur {payload['comparateur_neuf']}"
    )
    return 0


def build_foncier(root: Path) -> dict[str, object]:
    """Compute the R-10 summary payload (immobilised land in tense zones)."""
    raw = root / "data" / "raw"
    friches = foncier.parse_friches(
        pd.read_csv(raw / FRICHES_FILE, sep=";", dtype=str, na_values=["NA"])
    )
    with zipfile.ZipFile(raw / CENSUS_ZIP) as zf, zf.open(CENSUS_CSV) as fh:
        census_raw = pd.read_csv(fh, sep=";", dtype=str, usecols=["CODGEO", *rs.CENSUS_COLS])
    census = rs.parse_census_housing(census_raw)
    with zipfile.ZipFile(raw / CENSUS_ZIP) as zf, zf.open(CENSUS_CSV) as fh:
        paris_census = pd.read_csv(
            fh,
            sep=";",
            dtype=str,
            usecols=["CODGEO", "P22_LOG", "P22_RP_ACHTOT", "P22_RP_ACH1919"],
        )
    paris_census = paris_census[paris_census["CODGEO"].str.match(r"^751\d\d$")]
    with zipfile.ZipFile(raw / COMPARATEUR_ZIP) as zf, zf.open(COMPARATEUR_CSV) as fh:
        comp = pd.read_csv(
            fh,
            sep=";",
            dtype=str,
            usecols=["GEO_OBJECT", "GEO", "TIME_PERIOD", "TAB_MEASURE", "OBS_VALUE"],
        )
    sup = comp[
        (comp["GEO_OBJECT"] == "ARM")
        & (comp["TAB_MEASURE"] == "SUP")
        & comp["GEO"].str.match(r"^751\d\d$")
    ].copy()
    sup["km2"] = pd.to_numeric(sup["OBS_VALUE"], errors="coerce")
    superficies = sup.sort_values("TIME_PERIOD").groupby("GEO")["km2"].last()

    tlv = tension.parse_tlv(pd.read_csv(raw / TLV_FILE, sep=";", dtype=str))
    commune_ze = ze.parse_commune_ze(_read_membership(root))
    communes = lovac.parse_territories(
        _read_lovac(root, LOVAC_COMMUNES), code_col="CODGEO_26", name_col="LIBGEO_26"
    )
    h08 = _load_hypothesis(root, "H-08")
    frame = tension.tension_by_ze(census, tlv, communes, commune_ze, h08.central_value)
    tense_besoin = frame.loc[frame["tendue"], "besoin_mobilisation"]

    density_frame = foncier.haussmann_density(paris_census, superficies)
    return foncier.foncier_summary(
        friches,
        commune_ze,
        tense_besoin,
        density_frame,
        _ze_names(root),
        _load_hypothesis(root, "H-11"),
    )


def run_foncier(root: Path) -> int:
    """Rebuild data/processed/foncier-friches-ze.json; return an exit code."""
    payload = build_foncier(root)
    _write_json(root, FONCIER_OUTPUT, payload)
    print(
        f"foncier-friches: wrote {FONCIER_OUTPUT} — gisement {payload['gisement_central']}, "
        f"capacite {payload['capacite_centrale']}"
    )
    return 0


def run_effort(root: Path) -> int:
    """Rebuild data/processed/taux-effort-relocation-ze.json; return an exit code."""
    payload = build_taux_effort(root)
    _write_json(root, EFFORT_OUTPUT, payload)
    print(
        f"taux-effort: wrote {EFFORT_OUTPUT} — median effort "
        f"{payload['median_effort_by_h07_pct']}, spearman vs vacancy "
        f"{payload['spearman_effort_vs_vacancy']}"
    )
    return 0


def run_rs(root: Path) -> int:
    """Rebuild data/processed/residences-secondaires-ze.json; return an exit code."""
    payload = build_residences_secondaires(root)
    _write_json(root, RS_OUTPUT, payload)
    print(
        f"residences-secondaires: wrote {RS_OUTPUT} — spearman RS×vacance "
        f"{payload['spearman_rs_vs_structural_vacancy']}, touristic {payload['touristic_ze']}"
    )
    return 0
