"""Pure statistical helpers shared by the R-xx summaries.

Added by the 2026-08-07 adversarial review: every published rank
correlation now carries its Fisher 95 % confidence interval and its
sample size, and the France-entière / métropole split is computable
everywhere — the review showed that comparing correlations published on
different perimeters (R-08 métropole vs R-03/R-04 France entière)
manufactured a « strongest correlate » that an equal-perimeter reading
does not support. No I/O, no clock.
"""

from __future__ import annotations

import math

import pandas as pd

# ZE 2020 codes: 01xx Guadeloupe, 02xx Martinique, 03xx Guyane,
# 04xx La Réunion ; the 00xx codes are metropolitan multi-region zones.
DOM_ZE_PREFIXES = ("01", "02", "03", "04")


class StatsError(Exception):
    """A statistical helper received an input it cannot honestly handle."""


def spearman(frame: pd.DataFrame, x: str, y: str) -> float:
    """Spearman rank correlation as Pearson-on-ranks (no scipy dependency)."""
    sub = frame[[x, y]].dropna()
    if len(sub) < 2:
        raise StatsError(f"not enough observations for a correlation ({len(sub)})")
    return float(sub[x].rank().corr(sub[y].rank()))


def fisher_ci95(rho: float, n: int) -> tuple[float, float]:
    """95 % confidence interval of a correlation via the Fisher z-transform."""
    if not -1.0 < rho < 1.0:
        raise StatsError(f"degenerate correlation {rho}")
    if n < 4:
        raise StatsError(f"not enough observations for an interval ({n})")
    z = math.atanh(rho)
    half = 1.959964 / math.sqrt(n - 3)
    return (math.tanh(z - half), math.tanh(z + half))


def spearman_summary(frame: pd.DataFrame, x: str, y: str) -> dict[str, object]:
    """Build the publishable correlation block: rho, n, Fisher 95 % interval.

    A degenerate case (n < 4, or |rho| = 1 on tiny samples) keeps a null
    interval instead of failing: unknown keeps, definite rejects.
    """
    sub = frame[[x, y]].dropna()
    if len(sub) < 2:
        return {"rho": None, "n": len(sub), "ci95": None}
    rho = spearman(sub, x, y)
    if len(sub) < 4 or not -1.0 < rho < 1.0:
        return {"rho": round(rho, 2), "n": len(sub), "ci95": None}
    low, high = fisher_ci95(rho, len(sub))
    return {
        "rho": round(rho, 2),
        "n": len(sub),
        "ci95": [round(low, 2), round(high, 2)],
    }


def is_dom_index(frame: pd.DataFrame) -> pd.Series:
    """Boolean mask of DOM rows from a ZE-coded index."""
    return frame.index.astype(str).str.startswith(DOM_ZE_PREFIXES)


def spearman_by_perimeter(frame: pd.DataFrame, x: str, y: str) -> dict[str, dict[str, object]]:
    """Compute the same correlation on both perimeters — never compare across them."""
    dom = is_dom_index(frame)
    return {
        "france_entiere": spearman_summary(frame, x, y),
        "metropole": spearman_summary(frame[~dom], x, y),
    }
