"""Behaviour and property tests for the pure D-15 core (core/rent.py)."""

from __future__ import annotations

import math

import pytest
from hypothesis import given
from hypothesis import strategies as st

from autoroutes.core import rent
from autoroutes.core.rent import ConcessionYear

ROW = ConcessionYear(
    company="ASF",
    year=2023,
    revenue=1000.0,
    operating_costs=300.0,
    depreciation=200.0,
    asset_base=5000.0,
)

money = st.floats(min_value=0.0, max_value=1e6, allow_nan=False, allow_infinity=False)
rates = st.floats(min_value=0.0, max_value=20.0, allow_nan=False, allow_infinity=False)


def test_surplus_is_margin_minus_return_on_asset_base() -> None:
    """Worked example: 1000 − 300 − 200 − 5 % × 5000 = 250 M€, i.e. 25 % of revenue."""
    assert rent.operating_margin(ROW) == 500.0
    assert rent.surplus(ROW, 5.0) == pytest.approx(250.0)
    assert rent.surplus_share(ROW, 5.0) == pytest.approx(0.25)
    assert rent.break_even_rate(ROW) == pytest.approx(10.0)
    assert rent.surplus(ROW, 10.0) == pytest.approx(0.0)


def test_asset_base_nets_depreciation_and_subsidies() -> None:
    """The base is the historical cost net of what was already paid for or amortised."""
    assert rent.asset_base(10_000.0, 4_000.0, 500.0) == 5_500.0


def test_zero_denominators_yield_none_not_errors() -> None:
    """A zero revenue or asset base is kept and flagged as None, never divided."""
    empty = ConcessionYear("x", 2023, 0.0, 0.0, 0.0, 0.0)
    assert rent.surplus_share(empty, 5.0) is None
    assert rent.break_even_rate(empty) is None


def test_surplus_table_names_every_rate() -> None:
    """Each named rate yields a surplus and a share column; the inputs are echoed."""
    (record,) = rent.surplus_table([ROW], {"reference": 5.0, "high": 8.8})
    assert record["company"] == "ASF"
    assert record["surplus_reference"] == pytest.approx(250.0)
    assert record["surplus_high"] == pytest.approx(500.0 - 0.088 * 5000.0)
    assert record["surplus_share_high"] == pytest.approx((500.0 - 440.0) / 1000.0)


def test_aggregate_sums_companies_per_year() -> None:
    """Aggregation is a plain sum of the four money fields, one row per year, sorted."""
    other = ConcessionYear("APRR", 2023, 500.0, 100.0, 100.0, 2000.0)
    earlier = ConcessionYear("APRR", 2022, 400.0, 100.0, 100.0, 2100.0)
    total_2022, total_2023 = rent.aggregate([ROW, other, earlier])
    assert (total_2022.year, total_2022.revenue) == (2022, 400.0)
    assert total_2023 == ConcessionYear("ensemble", 2023, 1500.0, 400.0, 300.0, 7000.0)


def test_tri_gap_conversion_reproduces_the_art_anchor() -> None:
    """ART: 0,7 point of TRI ≈ 5,5 % of revenue — the anchor must round-trip exactly."""
    assert rent.rent_share_from_tri_gap(7.9, 7.2) == pytest.approx(5.5)
    # 7,9 % TRI at the 5,0 % reference rate on 10 000 M€ of revenue.
    assert rent.rent_from_tri_gap(7.9, 5.0, 10_000.0) == pytest.approx(2.9 * 5.5 / 0.7 * 100.0)
    # A rate above the TRI gives a negative rent: the sign flips between the bounds.
    assert rent.rent_from_tri_gap(7.9, 8.8, 10_000.0) < 0


@given(revenue=money, opex=money, depreciation=money, base=money, low=rates, high=rates)
def test_surplus_is_non_increasing_in_the_rate(
    revenue: float, opex: float, depreciation: float, base: float, low: float, high: float
) -> None:
    """Property: a higher return on capital never raises the surplus."""
    low, high = min(low, high), max(low, high)
    row = ConcessionYear("x", 2023, revenue, opex, depreciation, base)
    assert rent.surplus(row, high) <= rent.surplus(row, low) + 1e-6


@given(revenue=money, opex=money, depreciation=money, base=st.floats(min_value=1.0, max_value=1e6))
def test_surplus_vanishes_at_the_break_even_rate(
    revenue: float, opex: float, depreciation: float, base: float
) -> None:
    """Property: the surplus at the break-even rate is zero (within float tolerance)."""
    row = ConcessionYear("x", 2023, revenue, opex, depreciation, base)
    rate = rent.break_even_rate(row)
    assert rate is not None
    assert math.isclose(rent.surplus(row, rate), 0.0, abs_tol=1e-6 * max(1.0, revenue, base))
