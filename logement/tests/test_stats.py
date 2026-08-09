"""Tests for the shared statistical helpers (core/stats.py).

The partial correlation and the Mann-Whitney test were added by the
2026-08-09 adversarial review (SE-1/SE-4/SE-6 and the R-11 median
contrast): the partial is the honest companion of any published rank
correlation whose covariate is suspected, and the median contrasts now
carry a distributional test instead of bare medians.
"""

from __future__ import annotations

import pandas as pd
import pytest
from hypothesis import given
from hypothesis import strategies as st

from logement.core import stats


def _frame() -> pd.DataFrame:
    # x trends upward; y follows z (pairwise-swapped trend) except for
    # its last two values — y's correlation with x is mostly carried
    # by z, so the partial collapses far below the raw rho.
    return pd.DataFrame(
        {
            "x": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            "z": [2, 1, 4, 3, 6, 5, 8, 7, 10, 9],
            "y": [3, 2, 5, 4, 7, 6, 9, 8, 10, 11],
        }
    )


def test_partial_collapses_a_covariate_driven_correlation() -> None:
    """Controlling the driver removes most of the raw association."""
    frame = _frame()
    assert stats.spearman(frame, "x", "y") == pytest.approx(0.9515, abs=1e-4)
    assert stats.partial_spearman(frame, "x", "y", "z") == pytest.approx(0.4417, abs=1e-4)


def test_partial_summary_carries_control_and_interval() -> None:
    """The publishable block names its control and keeps n − 4 dof."""
    block = stats.partial_spearman_summary(_frame(), "x", "y", "z")
    assert block == {"rho": 0.44, "n": 10, "controle": "z", "ci95": [-0.31, 0.86]}


def test_partial_degenerate_covariate_is_a_definite_reject() -> None:
    """A covariate rank-identical to a variable cannot be controlled for."""
    frame = _frame()
    frame["y"] = frame["z"] + 1  # same ranks as z
    with pytest.raises(stats.StatsError, match="degenerate partial"):
        stats.partial_spearman(frame, "x", "y", "z")


def test_partial_summary_unknown_keeps_on_tiny_samples() -> None:
    """Too few rows degrade to a null block instead of failing."""
    tiny = _frame().head(2)
    assert stats.partial_spearman_summary(tiny, "x", "y", "z")["rho"] is None


def test_mann_whitney_separated_groups() -> None:
    """Fully separated groups give a very small two-sided p."""
    a = pd.Series(range(1, 11), dtype=float)
    b = pd.Series(range(11, 21), dtype=float)
    assert stats.mann_whitney_p(a, b) == pytest.approx(0.0002, abs=1e-4)


def test_mann_whitney_interleaved_groups() -> None:
    """Interleaved groups are compatible with the null."""
    c = pd.Series([1, 3, 5, 7, 9, 11, 13, 15], dtype=float)
    d = pd.Series([2, 4, 6, 8, 10, 12, 14, 16], dtype=float)
    p = stats.mann_whitney_p(c, d)
    assert p is not None and p > 0.5


def test_mann_whitney_unknown_keeps() -> None:
    """Small groups and all-tie inputs return None, never a fake p."""
    a = pd.Series([1.0, 2.0, 3.0])
    b = pd.Series(range(11, 21), dtype=float)
    assert stats.mann_whitney_p(a, b) is None
    ties = pd.Series([1.0] * 10)
    assert stats.mann_whitney_p(ties, ties) is None


@given(
    st.lists(st.floats(min_value=-100, max_value=100), min_size=8, max_size=30, unique=True),
    st.lists(st.floats(min_value=-100, max_value=100), min_size=8, max_size=30, unique=True),
)
def test_property_mann_whitney_symmetric_and_bounded(xs: list[float], ys: list[float]) -> None:
    """P is a probability and does not depend on the argument order."""
    a, b = pd.Series(xs), pd.Series(ys)
    p_ab = stats.mann_whitney_p(a, b)
    p_ba = stats.mann_whitney_p(b, a)
    assert p_ab is not None and 0.0 <= p_ab <= 1.0
    assert p_ab == p_ba


@given(st.integers(min_value=5, max_value=25))
def test_property_partial_of_independent_control_matches_raw(n: int) -> None:
    """A control uncorrelated by construction leaves the raw rho intact.

    x and y are the same trend with adjacent pairs swapped (raw rho < 1);
    z alternates low/high independently of the trend, so controlling it
    moves the correlation only marginally.
    """
    trend = list(range(2 * n))
    swapped = [i + 1 if i % 2 == 0 else i - 1 for i in trend]
    frame = pd.DataFrame(
        {
            "x": trend,
            "y": swapped,
            "z": [i // 2 + (n + 10) * (i % 2) for i in trend],
        }
    )
    raw = stats.spearman(frame, "x", "y")
    partial = stats.partial_spearman(frame, "x", "y", "z")
    assert partial == pytest.approx(raw, abs=0.35)
