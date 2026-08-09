"""Pure transforms for the transaction-cost cross (stabilized from
notebooks/exploration/15_cout_transaction.py, reworked by the 2026-08-09
adversarial review).

Fourth instruction of the framing hypothesis H-04 (mobilités empêchées):
every purchase pays a non-recoverable toll — transfer taxes (per-department
rates from the DGFiP table S-31, territorialized since the review's HD-4),
the notary's proportional fee (exact schedule from S-32) and the
contribution de sécurité immobilière (0.10 %, S-37 — the floor got
tighter, SA-5). Filters the DVF 2025 sales (S-30) down to single-dwelling
mutations (convention C-10) while PUBLISHING what the convention removes
(HD-6/HD-7), computes median prices by ZE and expresses the toll in
months of median living standard per consumption unit (C-04). The
uniform H-13 scenarios (5.09 / 5.81 / 6.32) stay published as
sensitivity — 5.81 % is both the pre-2025 common-law rate and the
first-time-buyer rate (HD-3/HD-5). No I/O, no clock.
"""

from __future__ import annotations

import pandas as pd

from logement.core import stats
from logement.core.lovac import plm_parent

DVF_COLUMNS = (
    "id_mutation",
    "nature_mutation",
    "valeur_fonciere",
    "code_commune",
    "type_local",
    "surface_reelle_bati",
)
DWELLING_TYPES = ("Maison", "Appartement")
COMMERCIAL_TYPE = "Local industriel. commercial ou assimilé"
# C-10 plausibility bounds: below/above these, rows are apparatus noise
# (symbolic-euro sales, garage-only surfaces, data-entry slips).
MIN_PRICE_EUR = 5_000.0
MIN_SURFACE_M2 = 10.0
PRICE_M2_BOUNDS = (200.0, 30_000.0)
# ZE whose plausibility bounds remove more than this share of their
# unitary sales get a published warning (HD-7: in the thin Guadeloupe
# ZE the convention makes the median).
BOUNDS_WARNING_SHARE = 0.10
# Sale-count floor for rankings, symmetric with the R-12 social-stock
# floor (HD-7): thin ZE stay in the frame, medians and correlations
# (shown robust to this floor) but out of the published rankings.
MIN_VENTES_CLASSEMENT = 100

# Notary proportional-fee schedule (S-32, per-bracket rates on the price,
# in force since 2021-01-01), VAT on top.
EMOLUMENTS_BRACKETS = (
    (0.0, 6_500.0, 0.03870),
    (6_500.0, 17_000.0, 0.01596),
    (17_000.0, 60_000.0, 0.01064),
    (60_000.0, float("inf"), 0.00799),
)
VAT = 1.20

# Contribution de sécurité immobilière (S-37, art. 879-881 CGI): 0.10 %
# of the price, 15 € minimum — as deterministic as the duties.
CSI_RATE = 0.001
CSI_MIN_EUR = 15.0

# Per-department voted DMTO rates read off the frozen S-31 table
# (01/02/2026, verified line by line on the PDF): the vast majority
# voted the temporary 5.00 % (art. 116 LF2025, acts from 2025-04-01),
# eleven departments stayed at the 4.50 % common law — 05, 06, 07, 16,
# 26, 27, 48, 60, 65, 71, 971 (the registry note's « une dizaine »
# missed 65, caught by the review) — and Indre (36) plus Mayotte (976)
# kept 3.80 %. The full toll rate adds the 1.20 % communal tax and the
# 2.37 % assessment fee on the departmental duty:
# total = departemental × 1.0237 + 1.20 (checks: 5.00 → 6.32,
# 4.50 → 5.81, 3.80 → 5.09).
DMTO_DEPARTEMENTAL_DEFAULT_PCT = 5.00
DMTO_DEPARTEMENTAL_EXCEPTIONS_PCT = {
    "05": 4.50,
    "06": 4.50,
    "07": 4.50,
    "16": 4.50,
    "26": 4.50,
    "27": 4.50,
    "36": 3.80,
    "48": 4.50,
    "60": 4.50,
    "65": 4.50,
    "71": 4.50,
    "971": 4.50,
    "976": 3.80,
}
ASSESSMENT_FEE_FACTOR = 1.0237
COMMUNAL_TAX_PCT = 1.20
# Total rate at the 4.50 % common law — the pre-2025 rate everywhere,
# still the first-time-buyer rate today (HD-5), and the return rate if
# the temporary faculty lapses on 2028-03-31.
DMTO_COMMON_LAW_TOTAL_PCT = round(4.50 * ASSESSMENT_FEE_FACTOR + COMMUNAL_TAX_PCT, 2)

# Annualization views (SE-9): the toll is paid once per move, so its
# yearly weight depends on how often the household moves. Descriptive
# arithmetic over a grid of holding durations — deliberately NOT a
# hypothesis (no frozen source elects a central duration).
HOLDING_YEARS_GRID = (5, 10, 20)


class TransactionError(Exception):
    """A DVF payload does not have the expected shape."""


def departement_of(code_commune: str) -> str:
    """Department code of a five-character commune code (97x for the DOM)."""
    return code_commune[:3] if code_commune.startswith("97") else code_commune[:2]


def dmto_total_rate_pct(departement: str) -> float:
    """Full transfer-tax rate (departmental + communal + assessment fee)."""
    voted = DMTO_DEPARTEMENTAL_EXCEPTIONS_PCT.get(departement, DMTO_DEPARTEMENTAL_DEFAULT_PCT)
    return voted * ASSESSMENT_FEE_FACTOR + COMMUNAL_TAX_PCT


def csi_eur(prix_eur: float) -> float:
    """Contribution de sécurité immobilière (S-37): 0.10 %, 15 € minimum."""
    if prix_eur < 0:
        raise TransactionError(f"negative price {prix_eur}")
    return max(prix_eur * CSI_RATE, CSI_MIN_EUR)


def parse_dvf_sales(raw: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, int]]:
    """Filter the DVF rows to single-dwelling sales (convention C-10).

    Keeps sales mutations carrying exactly ONE dwelling (Maison or
    Appartement) and no commercial unit — dependencies are fine — and
    flags (instead of dropping) the rows outside the plausibility
    bounds. Returns the kept sales plus the exclusion counts the
    convention removes (HD-6: a third of the dwellings sold change
    hands in multi-dwelling mutations — the reader must see it).
    """
    for col in DVF_COLUMNS:
        if col not in raw.columns:
            raise TransactionError(f"missing DVF column {col}")
    ventes = raw[raw["nature_mutation"] == "Vente"]
    if ventes.empty:
        raise TransactionError("no sale row in the DVF payload")
    is_dwelling = ventes["type_local"].isin(DWELLING_TYPES)
    per_mut = ventes.groupby("id_mutation").agg(
        n_dwellings=("type_local", lambda s: int(s.isin(DWELLING_TYPES).sum())),
        n_commercial=("type_local", lambda s: int((s == COMMERCIAL_TYPE).sum())),
    )
    multi = per_mut[per_mut["n_dwellings"] >= 2]
    mixed = per_mut[(per_mut["n_dwellings"] == 1) & (per_mut["n_commercial"] > 0)]
    keep = per_mut[(per_mut["n_dwellings"] == 1) & (per_mut["n_commercial"] == 0)].index
    sales = ventes[is_dwelling & ventes["id_mutation"].isin(keep)].copy()
    if sales.empty:
        raise TransactionError("no single-dwelling sale left")
    sales["valeur"] = pd.to_numeric(sales["valeur_fonciere"], errors="coerce")
    sales["surface"] = pd.to_numeric(sales["surface_reelle_bati"], errors="coerce")
    sales["prix_m2"] = sales["valeur"] / sales["surface"]
    plausible = (
        (sales["valeur"] >= MIN_PRICE_EUR)
        & (sales["surface"] >= MIN_SURFACE_M2)
        & sales["prix_m2"].between(*PRICE_M2_BOUNDS)
    )
    sales["hors_bornes"] = ~plausible
    sales["code"] = sales["code_commune"].astype("string").str.strip().str.zfill(5).map(plm_parent)
    sales["taux_dmto_pct"] = sales["code"].map(lambda c: dmto_total_rate_pct(departement_of(c)))
    counts = {
        "n_lignes_vente": len(ventes),
        "n_mutations_vente": len(per_mut),
        "n_mutations_un_logement": len(keep),
        "n_mutations_multi_logements": len(multi),
        "n_logements_en_mutations_multi": int(multi["n_dwellings"].sum()),
        "n_mutations_un_logement_avec_commercial": len(mixed),
        "n_ventes_hors_bornes": int(sales["hors_bornes"].sum()),
        "n_ventes_retenues": int(plausible.sum()),
    }
    if counts["n_ventes_retenues"] == 0:
        raise TransactionError("no plausible single-dwelling sale left")
    return (
        sales[
            ["code", "type_local", "valeur", "surface", "prix_m2", "taux_dmto_pct", "hors_bornes"]
        ],
        counts,
    )


def emoluments_ttc(prix_eur: float) -> float:
    """Notary proportional fee, VAT included, from the S-32 bracket schedule."""
    if prix_eur < 0:
        raise TransactionError(f"negative price {prix_eur}")
    hors_tva = sum(
        (min(prix_eur, hi) - lo) * rate for lo, hi, rate in EMOLUMENTS_BRACKETS if prix_eur > lo
    )
    return hors_tva * VAT


def prices_by_ze(
    sales: pd.DataFrame, commune_ze: pd.DataFrame
) -> tuple[pd.DataFrame, dict[str, object]]:
    """Median sale price, price/m², counts and DMTO rate by ZE.

    Medians use the in-bounds sales only; the out-of-bounds count is
    kept per ZE so the published warning list (HD-7) can name the ZE
    where the bounds carry the median. Sales joining no ZE are counted,
    never silently dropped (ST-8).
    """
    merged = sales.merge(commune_ze, on="code", how="left")
    unjoined = merged[merged["ze"].isna()]
    joined = merged[merged["ze"].notna()]
    if joined.empty:
        raise TransactionError("no sale joined between DVF and membership table")
    retained = joined[~joined["hors_bornes"]]
    frame = retained.groupby("ze").agg(
        prix_median=("valeur", "median"),
        prix_m2_median=("prix_m2", "median"),
        n_ventes=("valeur", "size"),
        taux_dmto_pct=("taux_dmto_pct", "mean"),
    )
    frame["n_ventes_hors_bornes"] = (
        joined[joined["hors_bornes"]]
        .groupby("ze")["valeur"]
        .size()
        .reindex(frame.index)
        .fillna(0)
        .astype(int)
    )
    coverage = {
        "n_ventes_sans_ze": int((~unjoined["hors_bornes"]).sum()),
        "n_communes_sans_ze": int(unjoined["code"].nunique()),
    }
    return frame, coverage


def transaction_frame(
    prix: pd.DataFrame, niveau_vie: pd.Series, rates: dict[str, float]
) -> pd.DataFrame:
    """Attach the territorialized toll and the uniform H-13 scenarios.

    The headline toll uses the per-ZE DMTO rate (sale-weighted mean of
    the S-31 departmental rates, HD-4) plus the exact emoluments (S-32)
    and the CSI (S-37); the uniform scenarios stay as sensitivity.
    """
    if "central" not in rates:
        raise TransactionError("H-13 scenarios must include a central rate")
    frame = prix.join(niveau_vie.rename("niveau_vie_median"), how="left")
    if "taux_dmto_pct" not in frame.columns:
        raise TransactionError("prices frame must carry the territorialized DMTO rate")
    frais_fixes = frame["prix_median"].map(emoluments_ttc) + frame["prix_median"].map(csi_eur)
    for label, rate in rates.items():
        if not 0 < rate < 100:
            raise TransactionError(f"implausible transfer-tax rate {rate}")
        frame[f"cout_transaction_{label}"] = frame["prix_median"] * rate / 100 + frais_fixes
    frame["cout_transaction_territorialise"] = (
        frame["prix_median"] * frame["taux_dmto_pct"] / 100 + frais_fixes
    )
    frame["cout_pct_prix"] = frame["cout_transaction_territorialise"] / frame["prix_median"] * 100
    frame["part_fiscale_pct"] = (
        (frame["prix_median"] * frame["taux_dmto_pct"] / 100 + frame["prix_median"].map(csi_eur))
        / frame["cout_transaction_territorialise"]
        * 100
    )
    frame["cout_en_mois_niveau_vie"] = frame["cout_transaction_territorialise"] / (
        frame["niveau_vie_median"] / 12
    )
    for label in rates:
        frame[f"cout_en_mois_{label}"] = frame[f"cout_transaction_{label}"] / (
            frame["niveau_vie_median"] / 12
        )
    return frame


def build_summary(
    frame: pd.DataFrame,
    national: dict[str, object],
    assiette: dict[str, int],
    couverture: dict[str, object],
    tendue: pd.Series,
    indice_cout_pct: pd.Series,
    ze_names: pd.Series,
    hypothesis: dict[str, object],
    tendue_variants: dict[str, pd.Series] | None = None,
) -> dict[str, object]:
    """Assemble the R-14 payload: toll geography, tension medians, crosses."""
    full = (
        frame.join(tendue.rename("tendue"), how="left")
        .join(indice_cout_pct.rename("indice_cout_pct"), how="left")
        .join(ze_names.rename("ze_name"), how="left")
    )
    if full.empty:
        raise TransactionError("no ZE in the transaction frame")

    def entry(row: pd.Series) -> dict[str, object]:
        return {
            "ze": str(row.name),
            "name": row["ze_name"] if pd.notna(row["ze_name"]) else None,
            "prix_median_eur": round(float(row["prix_median"])),
            "cout_transaction_eur": round(float(row["cout_transaction_territorialise"])),
            "cout_en_mois_niveau_vie": round(float(row["cout_en_mois_niveau_vie"]), 1)
            if pd.notna(row["cout_en_mois_niveau_vie"])
            else None,
            "n_ventes": int(row["n_ventes"]),
        }

    classables = full[full["n_ventes"] >= MIN_VENTES_CLASSEMENT]

    def ranked(ascending: bool) -> pd.DataFrame:
        return classables.sort_values(
            ["cout_en_mois_niveau_vie", "ze_name"], ascending=[ascending, True], kind="stable"
        )

    known = full["tendue"].notna()
    tendues = known & full["tendue"].fillna(False).astype(bool)
    autres = known & ~full["tendue"].fillna(True).astype(bool)
    months = full["cout_en_mois_niveau_vie"]
    quantiles = months.quantile([0.25, 0.5, 0.75])

    def median_or_none(series: pd.Series) -> float | None:
        value = series.median()
        return None if pd.isna(value) else round(float(value), 2)

    def scenario_block(label: str) -> dict[str, float | None]:
        column = full[f"cout_en_mois_{label}"]
        return {
            "mediane_mois": median_or_none(column),
            "tendues_mois": median_or_none(column[tendues]),
            "autres_mois": median_or_none(column[autres]),
        }

    def annualisation_block(years: int) -> dict[str, float | None]:
        annual = months / 12.0 / years * 100.0
        return {
            "mediane_pct_niveau_vie_annuel": median_or_none(annual),
            "tendues_pct": median_or_none(annual[tendues]),
            "autres_pct": median_or_none(annual[autres]),
        }

    bornes_warning = full[
        full["n_ventes_hors_bornes"]
        > BOUNDS_WARNING_SHARE * (full["n_ventes"] + full["n_ventes_hors_bornes"])
    ]
    return {
        "hypothesis": hypothesis,
        "national": national,
        "assiette_c10": assiette,
        "couverture": couverture,
        "n_ze": len(full),
        "n_ze_avec_niveau_vie": int(months.notna().sum()),
        "seuil_ventes_classement": MIN_VENTES_CLASSEMENT,
        "n_ze_sous_seuil_classement": int((full["n_ventes"] < MIN_VENTES_CLASSEMENT).sum()),
        "ze_bornes_sensibles": [
            {
                "ze": str(idx),
                "name": row["ze_name"] if pd.notna(row["ze_name"]) else None,
                "n_ventes_retenues": int(row["n_ventes"]),
                "n_ventes_hors_bornes": int(row["n_ventes_hors_bornes"]),
            }
            for idx, row in bornes_warning.sort_index().iterrows()
        ],
        "cout_pct_prix": {
            "min": round(float(full["cout_pct_prix"].min()), 2),
            "mediane": round(float(full["cout_pct_prix"].median()), 2),
            "max": round(float(full["cout_pct_prix"].max()), 2),
        },
        "part_fiscale_mediane_pct": round(float(full["part_fiscale_pct"].median()), 1),
        "distribution_mois_niveau_vie": {
            "min": round(float(months.min()), 2),
            "q25": round(float(quantiles.loc[0.25]), 2),
            "mediane": round(float(quantiles.loc[0.5]), 2),
            "q75": round(float(quantiles.loc[0.75]), 2),
            "max": round(float(months.max()), 2),
        },
        "scenarios_h13_mois": {
            label: scenario_block(label)
            for label in ("bas", "droit_commun_primo", "central")
            if f"cout_en_mois_{label}" in full.columns
        },
        "peage_annualise": {
            f"detention_{years}_ans": annualisation_block(years) for years in HOLDING_YEARS_GRID
        },
        "peage_le_plus_lourd": [entry(r) for _, r in ranked(False).head(8).iterrows()],
        "peage_le_plus_leger": [entry(r) for _, r in ranked(True).head(8).iterrows()],
        "mediane_par_tension": {
            "tendues_mois": median_or_none(months[tendues]),
            "autres_mois": median_or_none(months[autres]),
            "tendues_prix_median_eur": _price_median(full, tendues),
            "autres_prix_median_eur": _price_median(full, autres),
            "n_tendues": int(tendues.sum()),
            "n_tension_inconnue": int((~known).sum()),
            "mann_whitney_p_mois": stats.mann_whitney_p(months[tendues], months[autres]),
        },
        "sensibilite_h08": {
            label: _variant_block(full, months, variant)
            for label, variant in (tendue_variants or {}).items()
        },
        "spearman_mois_vs_cout_locatif": stats.spearman_by_perimeter(
            full, "cout_en_mois_niveau_vie", "indice_cout_pct"
        ),
        "spearman_prix_vs_cout_locatif": stats.spearman_by_perimeter(
            full, "prix_median", "indice_cout_pct"
        ),
        # SE-9: the months metric is essentially a re-ranking of the
        # price (the rate is nearly flat) — published so the reader can
        # see how mechanical the +0.81 gradient is.
        "spearman_mois_vs_prix": stats.spearman_by_perimeter(
            full, "cout_en_mois_niveau_vie", "prix_median"
        ),
    }


def _price_median(full: pd.DataFrame, mask: pd.Series) -> int | None:
    value = full.loc[mask, "prix_median"].median()
    return None if pd.isna(value) else round(float(value))


def _variant_block(full: pd.DataFrame, months: pd.Series, variant: pd.Series) -> dict[str, object]:
    aligned = variant.reindex(full.index)
    known = aligned.notna()
    tendues = known & aligned.fillna(False).astype(bool)
    autres = known & ~aligned.fillna(True).astype(bool)

    def median_or_none(series: pd.Series) -> float | None:
        value = series.median()
        return None if pd.isna(value) else round(float(value), 2)

    return {
        "tendues_mois": median_or_none(months[tendues]),
        "autres_mois": median_or_none(months[autres]),
        "n_tendues": int(tendues.sum()),
    }
