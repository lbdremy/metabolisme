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
# 04xx La Réunion, 06xx Mayotte (0601, absent from every source until
# S-28 — added 2026-08-08 so the métropole perimeter stays honest for
# France-entière datasets) ; the 00xx codes are metropolitan
# multi-region zones.
DOM_ZE_PREFIXES = ("01", "02", "03", "04", "06")


class StatsError(Exception):
    """A statistical helper received an input it cannot honestly handle."""


def spearman(frame: pd.DataFrame, x: str, y: str) -> float:
    """Spearman rank correlation as Pearson-on-ranks (no scipy dependency)."""
    sub = frame[[x, y]].dropna()
    if len(sub) < 2:
        raise StatsError(f"not enough observations for a correlation ({len(sub)})")
    return float(sub[x].rank().corr(sub[y].rank()))


def fisher_ci95(rho: float, n: int) -> tuple[float, float]:
    """95 % confidence interval of a SPEARMAN rho via the Fisher z-transform.

    Uses the Bonett-Wright (2000) variance (1 + rho²/2)/(n − 3) — the
    plain Pearson 1/(n − 3) is anti-conservative for rank correlations
    at high |rho| (ST-4, 2026-08-09 review: ~15 % too narrow at 0.8;
    the correction moves published bounds by ≤ 0.01 at 2 decimals).
    """
    if not -1.0 < rho < 1.0:
        raise StatsError(f"degenerate correlation {rho}")
    if n < 4:
        raise StatsError(f"not enough observations for an interval ({n})")
    z = math.atanh(rho)
    half = 1.959964 * math.sqrt((1 + rho**2 / 2) / (n - 3))
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


def partial_spearman(frame: pd.DataFrame, x: str, y: str, z: str) -> float:
    """First-order partial rank correlation of x and y given z.

    Added by the 2026-08-09 adversarial review (SE-1/SE-4/SE-6): a raw
    rank correlation between a change and a gradient can be manufactured
    entirely by the initial level (or by a shared axis) — the partial is
    the honest companion figure whenever the covariate is suspected.
    """
    sub = frame[[x, y, z]].dropna()
    if len(sub) < 3:
        raise StatsError(f"not enough observations for a partial correlation ({len(sub)})")
    ranks = sub.rank()
    corr = ranks.corr()
    rxy = float(corr.loc[x, y])
    rxz = float(corr.loc[x, z])
    ryz = float(corr.loc[y, z])
    denom = math.sqrt((1.0 - rxz**2) * (1.0 - ryz**2))
    if denom == 0.0:
        raise StatsError("degenerate partial correlation (covariate fully explains a variable)")
    return (rxy - rxz * ryz) / denom


def partial_spearman_summary(frame: pd.DataFrame, x: str, y: str, z: str) -> dict[str, object]:
    """Build the publishable partial-correlation block (rho, n, control, CI).

    The interval uses n − 4 degrees of freedom (one covariate); the same
    unknown-keeps degradation as spearman_summary applies.
    """
    sub = frame[[x, y, z]].dropna()
    if len(sub) < 3:
        return {"rho": None, "n": len(sub), "controle": z, "ci95": None}
    rho = partial_spearman(sub, x, y, z)
    if len(sub) < 5 or not -1.0 < rho < 1.0:
        return {"rho": round(rho, 2), "n": len(sub), "controle": z, "ci95": None}
    zt = math.atanh(rho)
    half = 1.959964 * math.sqrt((1 + rho**2 / 2) / (len(sub) - 4))
    return {
        "rho": round(rho, 2),
        "n": len(sub),
        "controle": z,
        "ci95": [round(math.tanh(zt - half), 2), round(math.tanh(zt + half), 2)],
    }


def mann_whitney_p(a: pd.Series, b: pd.Series) -> float | None:
    """Two-sided Mann-Whitney p-value (normal approximation, tie-corrected).

    Deterministic and scipy-free; the normal approximation is accurate
    for the ZE-sized groups it is published on (n ≥ ~20 each). Returns
    None when a group is too small for the approximation to be honest.
    """
    a = a.dropna()
    b = b.dropna()
    n1, n2 = len(a), len(b)
    if min(n1, n2) < 8:
        return None
    combined = pd.concat([a, b], ignore_index=True)
    ranks = combined.rank()
    r1 = float(ranks.iloc[:n1].sum())
    u1 = r1 - n1 * (n1 + 1) / 2
    mu = n1 * n2 / 2
    n = n1 + n2
    ties = combined.value_counts()
    tie_term = float(((ties**3) - ties).sum()) / (n * (n - 1))
    sigma2 = n1 * n2 / 12 * ((n + 1) - tie_term)
    if sigma2 <= 0:
        return None
    z = max(0.0, abs(u1 - mu) - 0.5) / math.sqrt(sigma2)
    return round(math.erfc(z / math.sqrt(2.0)), 4)


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


def partial_spearman_by_perimeter(
    frame: pd.DataFrame, x: str, y: str, z: str
) -> dict[str, dict[str, object]]:
    """Compute the partial companion of spearman_by_perimeter (same discipline)."""
    dom = is_dom_index(frame)
    return {
        "france_entiere": partial_spearman_summary(frame, x, y, z),
        "metropole": partial_spearman_summary(frame[~dom], x, y, z),
    }
