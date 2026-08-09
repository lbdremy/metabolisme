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

REQUIRED_COLUMNS = ("COMMUNE", "DCRAN", "IRAN", "IPONDI", "STOCD", "AGEREVQ")
# Age groups for the life-cycle reading of the internal soldes (SE-8,
# 2026-08-09 review): entries at student ages vs net exits at family and
# retirement ages. AGEREVQ is the five-year age at the survey.
AGE_GROUPS = (
    (0, 14, "0-14"),
    (15, 24, "15-24"),
    (25, 39, "25-39"),
    (40, 59, "40-59"),
    (60, 200, "60+"),
)
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
    out["AGEREVQ"] = pd.to_numeric(out["AGEREVQ"], errors="coerce")
    if out["AGEREVQ"].isna().any() or (out["AGEREVQ"] < 0).any():
        raise MigrationsError("AGEREVQ ages must be present and non-negative")
    known = {IRAN_RATTACHEMENT, IRAN_SAME_DWELLING, "2", *IRAN_OTHER_COMMUNE, *IRAN_ABROAD}
    unknown = set(out["IRAN"].dropna().unique()) - known
    if unknown:
        raise MigrationsError(f"unknown IRAN modalities {sorted(unknown)}")
    return out


def _settled(frame: pd.DataFrame) -> pd.DataFrame:
    """Restrict to the mobile/settled field: drop the rattachement rows (D-18)."""
    return frame[frame["IRAN"] != IRAN_RATTACHEMENT]


def age_group(age: float) -> str:
    """Map a five-year age (AGEREVQ) to its published life-cycle group."""
    for low, high, label in AGE_GROUPS:
        if low <= age <= high:
            return label
    raise MigrationsError(f"age {age} outside every group")


def mobility_by_age(frame: pd.DataFrame) -> dict[str, dict[str, float]]:
    """National annual mobility rate per life-cycle age group (D-18 field)."""
    base = _settled(frame)
    if base.empty:
        raise MigrationsError("no observation outside the rattachement field")
    groups = base["AGEREVQ"].map(age_group)
    total = base.groupby(groups)["IPONDI"].sum()
    movers = base[base["IRAN"] != IRAN_SAME_DWELLING].groupby(groups)["IPONDI"].sum()
    return {
        label: {
            "personnes": round(float(total[label])),
            "taux_mobilite_pct": round(float(movers.get(label, 0.0) / total[label] * 100), 2),
        }
        for _low, _high, label in AGE_GROUPS
        if label in total.index
    }


def soldes_by_age(
    frame: pd.DataFrame, commune_ze: pd.DataFrame, target_ze: str
) -> dict[str, dict[str, float | None]]:
    """Split one ZE's internal entries, exits and soldes per age group (SE-8).

    Same field as the R-13 soldes: internal migrations between ZE
    (IRAN 3-7), origin mapped through the PLM parent. The life-cycle
    signature is entries concentrated at 15-24 and net exits at family
    and retirement ages.
    """
    ze_of = commune_ze.set_index("code")["ze"]
    base = _settled(frame).copy()
    base["ze"] = base["COMMUNE"].map(ze_of)
    movers = base[base["IRAN"].isin(IRAN_OTHER_COMMUNE)].copy()
    movers["ze_origine"] = movers["DCRAN"].map(plm_parent).map(ze_of)
    inter = movers.dropna(subset=["ze", "ze_origine"])
    inter = inter[inter["ze"] != inter["ze_origine"]]
    groups_in = inter.loc[inter["ze"] == target_ze, "AGEREVQ"].map(age_group)
    groups_out = inter.loc[inter["ze_origine"] == target_ze, "AGEREVQ"].map(age_group)
    entrants = inter[inter["ze"] == target_ze].groupby(groups_in)["IPONDI"].sum()
    sortants = inter[inter["ze_origine"] == target_ze].groupby(groups_out)["IPONDI"].sum()
    residents = base[base["ze"] == target_ze]
    population = residents.groupby(residents["AGEREVQ"].map(age_group))["IPONDI"].sum()
    if population.empty:
        raise MigrationsError(f"no resident in target ZE {target_ze}")
    blocks: dict[str, dict[str, float | None]] = {}
    for _low, _high, label in AGE_GROUPS:
        ent = float(entrants.get(label, 0.0))
        sor = float(sortants.get(label, 0.0))
        pop = float(population.get(label, 0.0))
        blocks[label] = {
            "entrants": round(ent),
            "sortants": round(sor),
            "solde": round(ent - sor),
            "solde_pct_pop_groupe": round((ent - sor) / pop * 100, 2) if pop else None,
        }
    return blocks


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
        "taux_mobilite_par_age": mobility_by_age(frame),
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
    tendue_variants: dict[str, pd.Series] | None = None,
    soldes_par_age_paris: dict[str, dict[str, float | None]] | None = None,
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

    # 2026-08-09 review (HD-2): unknown tension stays unknown — excluded
    # from both medians and counted.
    known = frame["tendue"].notna()
    tendues = known & frame["tendue"].fillna(False).astype(bool)
    autres = known & ~frame["tendue"].fillna(True).astype(bool)
    quantiles = frame["taux_mobilite_pct"].quantile([0.25, 0.5, 0.75])

    def median_or_none(mask: pd.Series, column: str) -> float | None:
        value = frame.loc[mask, column].median()
        return None if pd.isna(value) else round(float(value), 2)

    def variant_block(variant: pd.Series) -> dict[str, object]:
        aligned = variant.reindex(frame.index)
        v_known = aligned.notna()
        v_tendues = v_known & aligned.fillna(False).astype(bool)
        v_autres = v_known & ~aligned.fillna(True).astype(bool)
        return {
            "tendues_taux_mobilite_pct": median_or_none(v_tendues, "taux_mobilite_pct"),
            "autres_taux_mobilite_pct": median_or_none(v_autres, "taux_mobilite_pct"),
            "n_tendues": int(v_tendues.sum()),
        }

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
                "taux_mobilite_pct": median_or_none(tendues, "taux_mobilite_pct"),
                "solde_pct_pop": median_or_none(tendues, "solde_pct_pop"),
            },
            "autres": {
                "taux_mobilite_pct": median_or_none(autres, "taux_mobilite_pct"),
                "solde_pct_pop": median_or_none(autres, "solde_pct_pop"),
            },
            "n_tendues": int(tendues.sum()),
            "n_tension_inconnue": int((~known).sum()),
            "mann_whitney_p_taux": stats.mann_whitney_p(
                frame.loc[tendues, "taux_mobilite_pct"], frame.loc[autres, "taux_mobilite_pct"]
            ),
        },
        "sensibilite_h08": {
            label: variant_block(variant) for label, variant in (tendue_variants or {}).items()
        },
        # SE-8: the life-cycle reading of the Paris internal soldes —
        # entries at 15-24, net exits at family and retirement ages.
        "soldes_par_age_paris": soldes_par_age_paris or {},
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
