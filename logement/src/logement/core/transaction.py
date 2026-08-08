"""Pure transforms for the transaction-cost cross (stabilized from
notebooks/exploration/15_cout_transaction.py).

Fourth instruction of the framing hypothesis H-04 (mobilités empêchées):
every purchase pays a non-recoverable toll — transfer taxes (H-13, from
the DGFiP per-department table S-31) plus the notary's proportional fee
(exact schedule from S-32). Filters the DVF 2025 sales (S-30) down to
single-dwelling mutations (convention C-10), computes median prices by
ZE and expresses the toll in months of median living standard per
consumption unit (C-04: no reference household). No I/O, no clock.
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

# Notary proportional-fee schedule (S-32, per-bracket rates on the price,
# in force since 2021-01-01), VAT on top.
EMOLUMENTS_BRACKETS = (
    (0.0, 6_500.0, 0.03870),
    (6_500.0, 17_000.0, 0.01596),
    (17_000.0, 60_000.0, 0.01064),
    (60_000.0, float("inf"), 0.00799),
)
VAT = 1.20


class TransactionError(Exception):
    """A DVF payload does not have the expected shape."""


def parse_dvf_sales(raw: pd.DataFrame) -> pd.DataFrame:
    """Filter the DVF rows to single-dwelling sales (convention C-10).

    Keeps sales mutations carrying exactly ONE dwelling (Maison or
    Appartement) and no commercial unit — dependencies are fine; then
    applies the plausibility bounds. Commune codes are zero-padded and
    PLM arrondissements mapped to their parent.
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
    keep = per_mut[(per_mut["n_dwellings"] == 1) & (per_mut["n_commercial"] == 0)].index
    sales = ventes[is_dwelling & ventes["id_mutation"].isin(keep)].copy()
    sales["valeur"] = pd.to_numeric(sales["valeur_fonciere"], errors="coerce")
    sales["surface"] = pd.to_numeric(sales["surface_reelle_bati"], errors="coerce")
    sales["prix_m2"] = sales["valeur"] / sales["surface"]
    sales = sales[
        (sales["valeur"] >= MIN_PRICE_EUR)
        & (sales["surface"] >= MIN_SURFACE_M2)
        & sales["prix_m2"].between(*PRICE_M2_BOUNDS)
    ]
    if sales.empty:
        raise TransactionError("no plausible single-dwelling sale left")
    sales["code"] = sales["code_commune"].astype("string").str.strip().str.zfill(5).map(plm_parent)
    return sales[["code", "type_local", "valeur", "surface", "prix_m2"]]


def emoluments_ttc(prix_eur: float) -> float:
    """Notary proportional fee, VAT included, from the S-32 bracket schedule."""
    if prix_eur < 0:
        raise TransactionError(f"negative price {prix_eur}")
    hors_tva = sum(
        (min(prix_eur, hi) - lo) * rate for lo, hi, rate in EMOLUMENTS_BRACKETS if prix_eur > lo
    )
    return hors_tva * VAT


def prices_by_ze(sales: pd.DataFrame, commune_ze: pd.DataFrame) -> pd.DataFrame:
    """Median sale price, price/m² and sale count by ZE."""
    merged = sales.merge(commune_ze, left_on="code", right_on="code", how="inner")
    if merged.empty:
        raise TransactionError("no sale joined between DVF and membership table")
    return merged.groupby("ze").agg(
        prix_median=("valeur", "median"),
        prix_m2_median=("prix_m2", "median"),
        n_ventes=("valeur", "size"),
    )


def transaction_frame(
    prix: pd.DataFrame, niveau_vie: pd.Series, rates: dict[str, float]
) -> pd.DataFrame:
    """Attach the toll (per H-13 scenario) and its weight in living standard."""
    if "central" not in rates:
        raise TransactionError("H-13 scenarios must include a central rate")
    frame = prix.join(niveau_vie.rename("niveau_vie_median"), how="left")
    for label, rate in rates.items():
        if not 0 < rate < 100:
            raise TransactionError(f"implausible transfer-tax rate {rate}")
        frame[f"cout_transaction_{label}"] = frame["prix_median"] * rate / 100 + frame[
            "prix_median"
        ].map(emoluments_ttc)
    frame["cout_pct_prix"] = frame["cout_transaction_central"] / frame["prix_median"] * 100
    frame["cout_en_mois_niveau_vie"] = frame["cout_transaction_central"] / (
        frame["niveau_vie_median"] / 12
    )
    return frame


def build_summary(
    frame: pd.DataFrame,
    national: dict[str, object],
    tendue: pd.Series,
    indice_cout_pct: pd.Series,
    ze_names: pd.Series,
    hypothesis: dict[str, object],
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
            "cout_transaction_eur": round(float(row["cout_transaction_central"])),
            "cout_en_mois_niveau_vie": round(float(row["cout_en_mois_niveau_vie"]), 1)
            if pd.notna(row["cout_en_mois_niveau_vie"])
            else None,
            "n_ventes": int(row["n_ventes"]),
        }

    def ranked(ascending: bool) -> pd.DataFrame:
        return full.sort_values(
            ["cout_en_mois_niveau_vie", "ze_name"], ascending=[ascending, True], kind="stable"
        )

    tendues = full["tendue"].fillna(False).astype(bool)
    months = full["cout_en_mois_niveau_vie"]
    quantiles = months.quantile([0.25, 0.5, 0.75])
    return {
        "hypothesis": hypothesis,
        "national": national,
        "n_ze": len(full),
        "n_ze_avec_niveau_vie": int(months.notna().sum()),
        "cout_pct_prix": {
            "min": round(float(full["cout_pct_prix"].min()), 2),
            "mediane": round(float(full["cout_pct_prix"].median()), 2),
            "max": round(float(full["cout_pct_prix"].max()), 2),
        },
        "distribution_mois_niveau_vie": {
            "min": round(float(months.min()), 2),
            "q25": round(float(quantiles.loc[0.25]), 2),
            "mediane": round(float(quantiles.loc[0.5]), 2),
            "q75": round(float(quantiles.loc[0.75]), 2),
            "max": round(float(months.max()), 2),
        },
        "peage_le_plus_lourd": [entry(r) for _, r in ranked(False).head(8).iterrows()],
        "peage_le_plus_leger": [entry(r) for _, r in ranked(True).head(8).iterrows()],
        "mediane_par_tension": {
            "tendues_mois": round(float(months[tendues].median()), 2),
            "autres_mois": round(float(months[~tendues].median()), 2),
            "tendues_prix_median_eur": round(float(full.loc[tendues, "prix_median"].median())),
            "autres_prix_median_eur": round(float(full.loc[~tendues, "prix_median"].median())),
            "n_tendues": int(tendues.sum()),
        },
        "spearman_mois_vs_cout_locatif": stats.spearman_by_perimeter(
            full, "cout_en_mois_niveau_vie", "indice_cout_pct"
        ),
        "spearman_prix_vs_cout_locatif": stats.spearman_by_perimeter(
            full, "prix_median", "indice_cout_pct"
        ),
    }
