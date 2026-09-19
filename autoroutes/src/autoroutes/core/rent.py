"""Pure transforms for the measurable rent (D-15 of the framing, applied to motorways).

Two ways of measuring the surplus profit of the seven historical private
concessions, both presented at the two bounds of the reference rate (H-01,
copied from monopoles:H-06) and at the sector's own rates:

1. `surplus` — the accounting form of D-15 on one concession-year: what the
   users pay, minus the cost of an efficient supply (cash operating costs,
   depreciation over technical life, return on an asset base at historical
   cost net of subsidies), before corporate income tax.
2. `rent_from_tri_gap` — the regulator's form: the ART converts a gap of
   TRI points into a share of toll revenue over the concession (0.7 point
   ≈ 5.5 % of revenue per year over 2003-2036, S-02 p. 95). Linear in the
   gap by construction (H-05), so it is an order of magnitude, not a
   measure.

No I/O, no clock. Money in millions of euros, rates in percent.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ConcessionYear:
    """One concession (or group of concessions) over one accounting year, M€."""

    company: str
    year: int
    revenue: float
    operating_costs: float
    depreciation: float
    asset_base: float


def asset_base(
    gross_historical_cost: float, accumulated_depreciation: float, subsidies: float
) -> float:
    """Net asset base of D-15: historical cost, minus depreciation, minus subsidies received."""
    return gross_historical_cost - accumulated_depreciation - subsidies


def operating_margin(row: ConcessionYear) -> float:
    """Revenue minus cash operating costs minus depreciation (before capital and tax), M€."""
    return row.revenue - row.operating_costs - row.depreciation


def surplus(row: ConcessionYear, rate_pct: float) -> float:
    """D-15 surplus of one concession-year at a given return on capital, M€.

    Negative when the reference return exceeds what the year's margin can
    pay on the asset base; zero at the break-even rate.
    """
    return operating_margin(row) - rate_pct / 100.0 * row.asset_base


def break_even_rate(row: ConcessionYear) -> float | None:
    """Return on the asset base at which the D-15 surplus is exactly zero, in %.

    None when the asset base is zero (no rate makes sense).
    """
    if row.asset_base == 0:
        return None
    return 100.0 * operating_margin(row) / row.asset_base


def surplus_share(row: ConcessionYear, rate_pct: float) -> float | None:
    """D-15 surplus as a share of revenue (ratio), None when revenue is zero."""
    if row.revenue == 0:
        return None
    return surplus(row, rate_pct) / row.revenue


def surplus_table(
    rows: list[ConcessionYear], rates_pct: dict[str, float]
) -> list[dict[str, object]]:
    """One record per concession-year with the surplus at every named rate.

    Rates are named (e.g. `{"reference_low": 4.0, "reference": 5.0}`) so the
    published artifact says which rate each column carries.
    """
    records: list[dict[str, object]] = []
    for row in rows:
        record: dict[str, object] = {
            "company": row.company,
            "year": row.year,
            "revenue": row.revenue,
            "operating_costs": row.operating_costs,
            "depreciation": row.depreciation,
            "asset_base": row.asset_base,
            "operating_margin": operating_margin(row),
            "break_even_rate_pct": break_even_rate(row),
        }
        for name, rate in rates_pct.items():
            record[f"surplus_{name}"] = surplus(row, rate)
            record[f"surplus_share_{name}"] = surplus_share(row, rate)
        records.append(record)
    return records


def aggregate(rows: list[ConcessionYear], company: str = "ensemble") -> list[ConcessionYear]:
    """Sum the concession-years of every company into one row per year."""
    by_year: dict[int, list[ConcessionYear]] = {}
    for row in rows:
        by_year.setdefault(row.year, []).append(row)
    return [
        ConcessionYear(
            company=company,
            year=year,
            revenue=sum(r.revenue for r in group),
            operating_costs=sum(r.operating_costs for r in group),
            depreciation=sum(r.depreciation for r in group),
            asset_base=sum(r.asset_base for r in group),
        )
        for year, group in sorted(by_year.items())
    ]


# ----------------------------------------------------------- the regulator's form

# ART, S-02 p. 95: "0,7 point de pourcentage de TRI est à peu près équivalent
# à un chiffre d'affaires supérieur de 5,5 % par an sur la période 2003-2036".
ART_REVENUE_SHARE_PER_TRI_POINT = 5.5 / 0.7


def rent_share_from_tri_gap(
    tri_pct: float, rate_pct: float, share_per_point: float = ART_REVENUE_SHARE_PER_TRI_POINT
) -> float:
    """Share of revenue (in %) that a TRI above the rate represents, linearised (H-05)."""
    return (tri_pct - rate_pct) * share_per_point


def rent_from_tri_gap(
    tri_pct: float,
    rate_pct: float,
    revenue: float,
    share_per_point: float = ART_REVENUE_SHARE_PER_TRI_POINT,
) -> float:
    """Annual rent, M€, implied by a TRI gap applied to a year's revenue (H-05)."""
    return rent_share_from_tri_gap(tri_pct, rate_pct, share_per_point) / 100.0 * revenue
