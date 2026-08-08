"""Pure transforms for the person-level residential-migration cross
(stabilized from notebooks/exploration/14_migrations_residentielles.py).

Third instruction of the framing hypothesis H-04 (mobilités empêchées):
R-11 and R-12 measure DWELLINGS; the MIGCOM detail file (S-29) measures
PERSONS — mobile means living in a different dwelling than on January 1st
of the year before the survey (D-18, indicator IRAN). Computes the annual
person-mobility rate by ZE, the tenure split of movers (the bridge to
R-12), and the origin→destination flows between ZE. No I/O, no clock.
"""

from __future__ import annotations

import pandas as pd

from logement.core import stats
from logement.core.lovac import plm_parent

REQUIRED_COLUMNS = ("COMMUNE", "DCRAN", "IRAN", "IPONDI", "STOCD")
# IRAN (D-18): 0 = commune de rattachement (out of the mobile/settled
# field), 1 = same dwelling, 2 = other dwelling same commune, 3-7 = other
# French commune, 8-9 = abroad.
IRAN_RATTACHEMENT = "0"
IRAN_SAME_DWELLING = "1"
IRAN_OTHER_COMMUNE = ("3", "4", "5", "6", "7")
IRAN_ABROAD = ("8", "9")
STOCD_LABELS = {
    "10": "proprietaire",
    "21": "locataire_prive",
    "22": "locataire_hlm",
    "23": "locataire_meuble",
    "30": "loge_gratuitement",
}
STOCD_OUT_OF_SCOPE = "ZZ"


class MigrationsError(Exception):
    """A MIGCOM payload does not have the expected shape."""


def parse_migcom(raw: pd.DataFrame) -> pd.DataFrame:
    """Validate the MIGCOM cut: typed codes, positive weights, known IRAN."""
    for col in REQUIRED_COLUMNS:
        if col not in raw.columns:
            raise MigrationsError(f"missing MIGCOM column {col}")
    out = raw[list(REQUIRED_COLUMNS)].copy()
    for col in ("COMMUNE", "DCRAN", "IRAN", "STOCD"):
        out[col] = out[col].astype("string").str.strip()
    out["IPONDI"] = pd.to_numeric(out["IPONDI"], errors="coerce")
    if out["IPONDI"].isna().any() or (out["IPONDI"] < 0).any():
        raise MigrationsError("IPONDI weights must be present and non-negative")
    known = {IRAN_RATTACHEMENT, IRAN_SAME_DWELLING, "2", *IRAN_OTHER_COMMUNE, *IRAN_ABROAD}
    unknown = set(out["IRAN"].dropna().unique()) - known
    if unknown:
        raise MigrationsError(f"unknown IRAN modalities {sorted(unknown)}")
    return out


def _settled(frame: pd.DataFrame) -> pd.DataFrame:
    """Restrict to the mobile/settled field: drop the rattachement rows (D-18)."""
    return frame[frame["IRAN"] != IRAN_RATTACHEMENT]


def national_summary(frame: pd.DataFrame) -> dict[str, object]:
    """National mobility block: overall rate, decomposition, tenure split."""
    base = _settled(frame)
    if base.empty:
        raise MigrationsError("no observation outside the rattachement field")
    pop = float(base["IPONDI"].sum())
    mobile = base["IRAN"] != IRAN_SAME_DWELLING

    def share(mask: pd.Series) -> float:
        return round(float(base.loc[mask, "IPONDI"].sum() / pop * 100), 2)

    seg = base[base["STOCD"] != STOCD_OUT_OF_SCOPE]
    par_statut = {}
    for code, label in STOCD_LABELS.items():
        rows = seg[seg["STOCD"] == code]
        weight = float(rows["IPONDI"].sum())
        movers = float(rows.loc[rows["IRAN"] != IRAN_SAME_DWELLING, "IPONDI"].sum())
        par_statut[label] = {
            "personnes": round(weight),
            "part_mobiles_pct": round(movers / weight * 100, 2) if weight else None,
        }
    return {
        "population": round(pop),
        "poids_rattachement_exclu": round(
            float(frame.loc[frame["IRAN"] == IRAN_RATTACHEMENT, "IPONDI"].sum())
        ),
        "taux_mobilite_pct": share(mobile),
        "dont_meme_commune_pct": share(base["IRAN"] == "2"),
        "dont_autre_commune_france_pct": share(base["IRAN"].isin(IRAN_OTHER_COMMUNE)),
        "dont_etranger_pct": share(base["IRAN"].isin(IRAN_ABROAD)),
        "part_mobiles_par_statut": par_statut,
    }


def migrations_by_ze(
    frame: pd.DataFrame, commune_ze: pd.DataFrame
) -> tuple[pd.DataFrame, dict[str, object]]:
    """Per-ZE mobility rates and inter-ZE flows; unmatched weights published."""
    ze_of = commune_ze.set_index("code")["ze"]
    base = _settled(frame).copy()
    base["ze"] = base["COMMUNE"].map(ze_of)
    unmatched_residence = base["ze"].isna()
    coverage = {
        "communes_sans_ze": int(base.loc[unmatched_residence, "COMMUNE"].nunique()),
        "poids_sans_ze": round(float(base.loc[unmatched_residence, "IPONDI"].sum())),
    }
    base = base.dropna(subset=["ze"])
    if base.empty:
        raise MigrationsError("no commune joined between MIGCOM and membership table")

    movers = base[base["IRAN"].isin(IRAN_OTHER_COMMUNE)].copy()
    movers["ze_origine"] = movers["DCRAN"].map(plm_parent).map(ze_of)
    coverage["poids_mobiles_sans_ze_origine"] = round(
        float(movers.loc[movers["ze_origine"].isna(), "IPONDI"].sum())
    )
    inter = movers.dropna(subset=["ze_origine"])
    inter = inter[inter["ze_origine"] != inter["ze"]]
    coverage["flux_inter_ze"] = round(float(inter["IPONDI"].sum()))

    # Index on residence ∪ origin ZE: an origin ZE without any surveyed
    # resident keeps its outgoing flow (rates stay missing, never zero) —
    # the per-ZE soldes must re-sum to zero.
    population = base.groupby("ze")["IPONDI"].sum()
    sortants = inter.groupby("ze_origine")["IPONDI"].sum()
    index = population.index.union(sortants.index)
    out = pd.DataFrame(index=index)
    out.index.name = "ze"
    out["population"] = population
    mobile = base["IRAN"] != IRAN_SAME_DWELLING
    out["mobiles"] = base[mobile].groupby("ze")["IPONDI"].sum()
    out["taux_mobilite_pct"] = out["mobiles"] / out["population"] * 100
    out["entrants"] = inter.groupby("ze")["IPONDI"].sum()
    out["sortants"] = sortants
    out[["entrants", "sortants"]] = out[["entrants", "sortants"]].fillna(0.0)
    out["solde"] = out["entrants"] - out["sortants"]
    out["solde_pct_pop"] = out["solde"] / out["population"] * 100
    out["taux_entree_pct"] = out["entrants"] / out["population"] * 100
    return out, coverage


def build_summary(
    ze_frame: pd.DataFrame,
    national: dict[str, object],
    coverage: dict[str, object],
    tendue: pd.Series,
    indice_cout_pct: pd.Series,
    rotation: pd.DataFrame,
    ze_names: pd.Series,
) -> dict[str, object]:
    """Assemble the R-13 payload: national block, ZE geography, flows, crosses."""
    frame = (
        ze_frame.join(tendue.rename("tendue"), how="left")
        .join(indice_cout_pct.rename("indice_cout_pct"), how="left")
        .join(rotation["part_recents_pct"].rename("rotation_rp_pct"), how="left")
        .join(ze_names.rename("ze_name"), how="left")
    )
    if frame.empty:
        raise MigrationsError("no ZE in the migrations frame")

    def entry(row: pd.Series, *fields: str) -> dict[str, object]:
        base: dict[str, object] = {
            "ze": str(row.name),
            "name": row["ze_name"] if pd.notna(row["ze_name"]) else None,
        }
        for field in fields:
            value = float(row[field])
            base[field] = round(value) if field in ("entrants", "sortants") else round(value, 2)
        return base

    def ranked(by: str, ascending: bool) -> pd.DataFrame:
        return frame.sort_values([by, "ze_name"], ascending=[ascending, True], kind="stable")

    tendues = frame["tendue"].fillna(False).astype(bool)
    quantiles = frame["taux_mobilite_pct"].quantile([0.25, 0.5, 0.75])
    return {
        "national": national,
        "couverture": coverage,
        "n_ze": len(frame),
        "distribution_taux_mobilite_pct": {
            "min": round(float(frame["taux_mobilite_pct"].min()), 2),
            "q25": round(float(quantiles.loc[0.25]), 2),
            "mediane": round(float(quantiles.loc[0.5]), 2),
            "q75": round(float(quantiles.loc[0.75]), 2),
            "max": round(float(frame["taux_mobilite_pct"].max()), 2),
        },
        "mobilite_la_plus_faible": [
            entry(r, "taux_mobilite_pct", "solde_pct_pop")
            for _, r in ranked("taux_mobilite_pct", True).head(8).iterrows()
        ],
        "mobilite_la_plus_forte": [
            entry(r, "taux_mobilite_pct", "solde_pct_pop")
            for _, r in ranked("taux_mobilite_pct", False).head(8).iterrows()
        ],
        "soldes_les_plus_negatifs": [
            entry(r, "entrants", "sortants", "solde_pct_pop")
            for _, r in ranked("solde_pct_pop", True).head(8).iterrows()
        ],
        "soldes_les_plus_positifs": [
            entry(r, "entrants", "sortants", "solde_pct_pop")
            for _, r in ranked("solde_pct_pop", False).head(8).iterrows()
        ],
        "mediane_par_tension": {
            "tendues": {
                "taux_mobilite_pct": round(
                    float(frame.loc[tendues, "taux_mobilite_pct"].median()), 2
                ),
                "solde_pct_pop": round(float(frame.loc[tendues, "solde_pct_pop"].median()), 2),
            },
            "autres": {
                "taux_mobilite_pct": round(
                    float(frame.loc[~tendues, "taux_mobilite_pct"].median()), 2
                ),
                "solde_pct_pop": round(float(frame.loc[~tendues, "solde_pct_pop"].median()), 2),
            },
            "n_tendues": int(tendues.sum()),
        },
        "spearman_mobilite_vs_rotation_rp": stats.spearman_by_perimeter(
            frame, "taux_mobilite_pct", "rotation_rp_pct"
        ),
        "spearman_mobilite_vs_cout": stats.spearman_by_perimeter(
            frame, "taux_mobilite_pct", "indice_cout_pct"
        ),
        "spearman_solde_vs_cout": stats.spearman_by_perimeter(
            frame, "solde_pct_pop", "indice_cout_pct"
        ),
        "spearman_entree_vs_cout": stats.spearman_by_perimeter(
            frame, "taux_entree_pct", "indice_cout_pct"
        ),
    }
