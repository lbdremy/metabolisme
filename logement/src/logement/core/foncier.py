"""Pure transforms for the immobilised-land cross (stabilized from
notebooks/exploration/11_foncier_friches.py).

Answers the question opened on 2026-08-05: how much land, in the tense
zones of R-07, is immobilised by vacant non-residential buildings?
Cartofriches sites (S-20, « friche sans projet » as the central
reservoir, + « friche potentielle » as the high variant, residential-
typed sites excluded, per-site area capped at 50 ha — C-08), converted
into a dwelling capacity at the Haussmannian reference density H-11 —
derived from frozen data (dwellings per Paris arrondissement S-11 over
areas S-21, arrondissements with ≥ 60 % pre-1919 stock) and re-computed
here so the registry value can never drift from the data. No I/O, no
clock; reads happen in the shell.
"""

from __future__ import annotations

import pandas as pd

from logement.core.lovac import plm_parent
from logement.models import HypothesisRecord

HAUSSMANN_PRE1919_MIN_PCT = 60.0  # C-08 selection criterion
CAP_SURFACE_M2 = 500_000.0  # C-08: beyond 50 ha a site is not one housing project
STATUT_CENTRAL = "friche sans projet"
STATUT_VARIANTE = "friche potentielle"


class FoncierError(Exception):
    """A land payload does not have the expected shape."""


def parse_friches(raw: pd.DataFrame) -> pd.DataFrame:
    """Parse Cartofriches: commune code, status, area, residential flag."""
    for col in ("comm_insee", "site_statut", "unite_fonciere_surface", "bati_type"):
        if col not in raw.columns:
            raise FoncierError(f"missing Cartofriches column {col}")
    out = pd.DataFrame(
        {
            "code": raw["comm_insee"].astype("string").str.strip().map(plm_parent),
            "statut": raw["site_statut"].astype("string").str.strip(),
            "surface_m2": pd.to_numeric(raw["unite_fonciere_surface"], errors="coerce"),
            "residentiel": raw["bati_type"]
            .astype("string")
            .str.lower()
            .str.startswith("r", na=False),
        }
    )
    return out.dropna(subset=["code", "surface_m2"])


def haussmann_density(paris_census: pd.DataFrame, superficies_km2: pd.Series) -> pd.DataFrame:
    """Per-arrondissement gross density and the C-08 selection flag."""
    for col in ("CODGEO", "P22_LOG", "P22_RP_ACHTOT", "P22_RP_ACH1919"):
        if col not in paris_census.columns:
            raise FoncierError(f"missing census column {col}")
    frame = paris_census.copy()
    for col in ("P22_LOG", "P22_RP_ACHTOT", "P22_RP_ACH1919"):
        frame[col] = pd.to_numeric(frame[col], errors="coerce")
    frame = frame.set_index(frame["CODGEO"].astype("string").str.strip()).join(
        superficies_km2.rename("km2"), how="inner"
    )
    if frame.empty:
        raise FoncierError("no arrondissement joined between census and areas")
    frame["part_avant_1919_pct"] = frame["P22_RP_ACH1919"] / frame["P22_RP_ACHTOT"] * 100
    frame["densite_logts_ha"] = frame["P22_LOG"] / (frame["km2"] * 100)
    frame["haussmannien"] = frame["part_avant_1919_pct"] >= HAUSSMANN_PRE1919_MIN_PCT
    return frame


def check_h11_against_data(frame: pd.DataFrame, h11: HypothesisRecord) -> dict[str, float]:
    """Recompute H-11 from the data and refuse any drift from the registry."""
    selected = frame.loc[frame["haussmannien"], "densite_logts_ha"]
    if selected.empty:
        raise FoncierError("no Haussmannian arrondissement selected")
    computed = {
        "n_arrondissements": float(len(selected)),
        "central": round(float(selected.median()), 1),
        "min": round(float(selected.min()), 1),
        "max": round(float(selected.max()), 1),
    }
    expected = (h11.central_value, h11.plausible_range[0], h11.plausible_range[1])
    got = (computed["central"], computed["min"], computed["max"])
    if any(abs(a - b) > 0.05 for a, b in zip(expected, got, strict=True)):
        raise FoncierError(
            f"H-11 drift: registry {expected} vs recomputed {got} — update the registry"
        )
    return computed


def foncier_summary(
    friches: pd.DataFrame,
    commune_ze: pd.DataFrame,
    tense_besoin: pd.Series,
    density_frame: pd.DataFrame,
    ze_names: pd.Series,
    h11: HypothesisRecord,
) -> dict[str, object]:
    """Assemble the R-10 payload: land reservoir, capacity, coverage."""
    computed_h11 = check_h11_against_data(density_frame, h11)
    besoin_total = float(tense_besoin.sum())
    if besoin_total <= 0:
        raise FoncierError("empty or non-positive detente need")

    non_res = friches[~friches["residentiel"]].copy()
    non_res["surface_capee_m2"] = non_res["surface_m2"].clip(upper=CAP_SURFACE_M2)
    localised = non_res.merge(commune_ze, on="code", how="left").dropna(subset=["ze"])
    in_tense = localised[localised["ze"].isin(set(tense_besoin.index))]

    def reservoir(statuts: list[str]) -> tuple[pd.DataFrame, int, dict[str, object]]:
        sub = in_tense[in_tense["statut"].isin(statuts)]
        ha_plafonnes = round(float(sub["surface_capee_m2"].sum()) / 1e4)
        return (
            sub,
            ha_plafonnes,
            {
                "n_sites": len(sub),
                "n_sites_plafonnes": int((sub["surface_m2"] > CAP_SURFACE_M2).sum()),
                "ha_plafonnes": ha_plafonnes,
                "ha_bruts": round(float(sub["surface_m2"].sum()) / 1e4),
                "n_ze": int(sub["ze"].nunique()),
            },
        )

    central_sub, central_ha, central_stats = reservoir([STATUT_CENTRAL])
    _, haute_ha, haute_stats = reservoir([STATUT_CENTRAL, STATUT_VARIANTE])

    def capacities(ha: float) -> dict[str, object]:
        return {
            label: {
                "logements": round(ha * dens),
                "ratio_besoin": round(ha * dens / besoin_total, 1),
            }
            for label, dens in (
                ("bas", h11.plausible_range[0]),
                ("central", h11.central_value),
                ("haut", h11.plausible_range[1]),
            )
        }

    per_ze = (
        central_sub.groupby("ze")["surface_capee_m2"]
        .agg(["sum", "count"])
        .join(ze_names.rename("ze_name"), how="left")
        .join(tense_besoin.rename("besoin"), how="left")
    )
    per_ze["ha"] = per_ze["sum"] / 1e4
    per_ze["capacite_centrale"] = per_ze["ha"] * h11.central_value
    covered = per_ze["capacite_centrale"] >= per_ze["besoin"]

    def entry(row: pd.Series) -> dict[str, object]:
        return {
            "ze": str(row.name),
            "name": row["ze_name"] if pd.notna(row["ze_name"]) else None,
            "n_sites": int(row["count"]),
            "ha_plafonnes": round(float(row["ha"])),
            "capacite_centrale": round(float(row["capacite_centrale"])),
            "besoin_mobilisation": round(float(row["besoin"])),
        }

    ranked = per_ze.sort_values(["ha", "ze_name"], ascending=[False, True], kind="stable")
    return {
        "h11_recalculee": computed_h11,
        "criteres": {
            "part_avant_1919_min_pct": HAUSSMANN_PRE1919_MIN_PCT,
            "cap_surface_m2": CAP_SURFACE_M2,
            "statut_central": STATUT_CENTRAL,
            "statut_variante": STATUT_VARIANTE,
        },
        "n_ze_tendues": len(tense_besoin),
        "besoin_total": round(besoin_total),
        "gisement_central": central_stats,
        "gisement_haute": haute_stats,
        "capacite_centrale": capacities(float(central_ha)),
        "capacite_haute": capacities(float(haute_ha)),
        "couverture": {
            "n_ze_avec_friche": len(per_ze),
            "n_ze_capacite_couvre_besoin": int(covered.sum()),
        },
        "top_gisements": [entry(r) for _, r in ranked.head(10).iterrows()],
    }
