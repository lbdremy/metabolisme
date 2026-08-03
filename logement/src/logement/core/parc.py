"""Pure parsing and transforms of the parc/ménages series (stabilized from
notebooks/exploration/01_parc_population.py).

All functions take already-loaded DataFrames (pandas' `read_excel` happens in
the shell) and return validated data — no I/O, no clock. Units: thousands of
dwellings / households, as published by INSEE.
"""

from __future__ import annotations

import itertools
from dataclasses import dataclass

import pandas as pd

CATEGORIES = (
    "Résidences principales",
    "Résidences secondaires, logements occasionnels",
    "Logements vacants",
)
TOTAL = "Ensemble"
# Rounding tolerance: EAPL publishes thousands, so category sums may differ
# from the published total by at most one unit.
SUM_TOLERANCE = 1.0


class ParcError(Exception):
    """A source payload does not have the expected shape or breaks an invariant."""


@dataclass(frozen=True)
class ParcCategories:
    """EAPL yearly counts (thousands): rows = years, columns = categories + total."""

    counts: pd.DataFrame
    provisional_years: tuple[int, ...]


def _normalize_label(label: str) -> str:
    return " ".join(label.replace("\xa0", " ").split())


def parse_eapl_categories(raw: pd.DataFrame) -> ParcCategories:
    """Parse S-02's 'Données' sheet (header row on the year line) into yearly counts.

    Keeps only top-level category rows (sub-rows are indented with non-breaking
    spaces), normalizes labels, reads '(p)'-marked columns as provisional years,
    and enforces the sum invariant: categories must add up to the total.
    """
    first_col = raw.columns[0]
    labels = raw[first_col].astype("string")
    top = raw[~labels.str.startswith("\xa0", na=True)].copy()
    top[first_col] = top[first_col].map(_normalize_label)
    top = top.set_index(first_col)

    years = {c: int(str(c)[:4]) for c in top.columns if str(c)[:4].isdigit()}
    if not years:
        raise ParcError("no year columns found in the EAPL sheet")
    counts = top[list(years)].apply(pd.to_numeric, errors="coerce").dropna(how="all")
    counts.columns = list(years.values())
    counts = counts.T

    missing = [c for c in (*CATEGORIES, TOTAL) if c not in counts.columns]
    if missing:
        raise ParcError(f"missing EAPL categories: {missing}")
    counts = counts[[*CATEGORIES, TOTAL]]

    gap = (counts[list(CATEGORIES)].sum(axis=1) - counts[TOTAL]).abs().max()
    if gap > SUM_TOLERANCE:
        raise ParcError(f"category sums differ from the total by up to {gap:.1f} thousand")

    provisional = tuple(sorted(y for c, y in years.items() if "(p)" in str(c)))
    return ParcCategories(counts=counts, provisional_years=provisional)


def parse_menages_totals(raw: pd.DataFrame, *, year_row: int = 2) -> pd.Series:
    """Parse S-03's 'France' sheet (read with header=None) into households per vintage.

    Reads the census years on `year_row` and the first 'Total' row (the
    'Nombre de ménages selon le nombre de personnes' block); 'n.d.' vintages
    are dropped.
    """
    years = raw.iloc[year_row, 1:].tolist()
    labels = raw[raw.columns[0]].astype("string").str.strip()
    total_rows = raw[labels == "Total"]
    if total_rows.empty:
        raise ParcError("no 'Total' row found in the ménages sheet")
    totals = total_rows.iloc[0, 1:].tolist()
    series = pd.Series(totals, index=[int(y) for y in years], name="menages")
    series = pd.to_numeric(series, errors="coerce").dropna()
    if series.empty:
        raise ParcError("the ménages 'Total' row contains no numeric value")
    return series


def parse_population_index(raw: pd.DataFrame) -> pd.Series:
    """Parse S-01's 'Figure 2' sheet (header on the 'Année' line) into a population index.

    Years arrive as text, sometimes suffixed ('2025p') or followed by footnote
    rows; both are handled by extracting the leading 4-digit year.
    """
    if "Année" not in raw.columns or "Population" not in raw.columns:
        raise ParcError("expected 'Année' and 'Population' columns in Figure 2")
    years = pd.to_numeric(
        raw["Année"].astype("string").str.extract(r"^(\d{4})")[0], errors="coerce"
    )
    population = pd.to_numeric(raw["Population"], errors="coerce")
    series = pd.Series(population.values, index=years.values, name="population")
    series = series[series.index.notna()].dropna()
    series.index = series.index.astype(int)
    return series


def index_to_base(series: pd.Series, base_year: int) -> pd.Series:
    """Rebase a series to 100 at `base_year` (single-axis comparisons, no dual axis)."""
    if base_year not in series.index:
        raise ParcError(f"base year {base_year} not in series")
    return series / series[base_year] * 100


def mean_annual_growth(series: pd.Series, start: int, end: int) -> float:
    """Mean annual growth rate (%) of a series between two of its years."""
    if end <= start:
        raise ParcError(f"invalid period {start}-{end}")
    for year in (start, end):
        if year not in series.index:
            raise ParcError(f"year {year} not in series")
    return (float(series[end] / series[start]) ** (1 / (end - start)) - 1) * 100


def build_summary(
    parc: ParcCategories, menages: pd.Series, population_index: pd.Series
) -> dict[str, object]:
    """Assemble the R-01 payload: indices, vacancy trajectory, growth by period, RP gap.

    The base year is the first year common to the parc and ménages series.
    """
    counts = parc.counts
    principal, secondary, vacant = CATEGORIES
    vintages = [int(y) for y in menages.index if y in counts.index]
    if not vintages:
        raise ParcError("no common year between the parc and ménages series")
    base = vintages[0]
    last_vintage = vintages[-1]
    last_year = int(counts.index.max())

    dwellings_idx = index_to_base(counts[TOTAL], base)
    menages_idx = index_to_base(menages[menages.index >= base], base)
    vacancy_share = counts[vacant] / counts[TOTAL] * 100
    secondary_share = counts[secondary] / counts[TOTAL] * 100

    growth = [
        {
            "period": f"{start}-{end}",
            "dwellings_pct_per_year": round(mean_annual_growth(counts[TOTAL], start, end), 2),
            "menages_pct_per_year": round(mean_annual_growth(menages, start, end), 2),
        }
        for start, end in itertools.pairwise(vintages)
    ]

    rp_gap_pct = {
        str(year): round(
            float((counts.loc[year, principal] - menages[year]) / menages[year] * 100), 2
        )
        for year in vintages
    }

    return {
        "base_year": base,
        "last_year": last_year,
        "provisional_years": list(parc.provisional_years),
        "indices_at_last_common_vintage": {
            "year": last_vintage,
            "dwellings": round(float(dwellings_idx[last_vintage]), 1),
            "menages": round(float(menages_idx[last_vintage]), 1),
            "population": round(float(population_index[last_vintage]), 1),
        },
        "vacancy": {
            "count_thousands": {
                str(base): round(float(counts.loc[base, vacant])),
                str(last_year): round(float(counts.loc[last_year, vacant])),
            },
            "share_pct": {
                str(base): round(float(vacancy_share[base]), 1),
                "min": round(float(vacancy_share.min()), 1),
                "min_year": int(vacancy_share.idxmin()),
                str(last_year): round(float(vacancy_share[last_year]), 1),
            },
        },
        "secondary_share_pct": {
            str(base): round(float(secondary_share[base]), 1),
            str(last_year): round(float(secondary_share[last_year]), 1),
        },
        "mean_annual_growth_by_period": growth,
        "rp_vs_menages_gap_pct": rp_gap_pct,
    }
