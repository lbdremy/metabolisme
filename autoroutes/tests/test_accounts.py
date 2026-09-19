"""Behaviour tests for the transcribed-accounts core (core/accounts.py)."""

from __future__ import annotations

import pytest

from autoroutes.core import accounts

ROWS: list[dict[str, object]] = [
    {"entity": "X", "year": 2023, "item": item, "value_meur": value}
    for item, value in {
        "revenue": 1000.0,
        "ancillary_income": 10.0,
        "construction_revenue": 100.0,
        "purchases": 20.0,
        "external_services": 80.0,
        "subcontracting_incl_construction": 130.0,
        "taxes": 100.0,
        "personnel": 60.0,
        "other_operating": 5.0,
        "depreciation": 200.0,
        "depreciation_domain": 180.0,
        "provisions": 5.0,
        "gross_domain": 6000.0,
        "work_in_progress": 100.0,
        "subsidies_gross": 200.0,
        "subsidies_amortised": 50.0,
        "accumulated_amortisation": 3000.0,
        "net_domain": 2950.0,
        "tangible_net": 50.0,
    }.items()
]


def test_group_accounts_requires_every_item() -> None:
    """A partial transcription is an error, not a silent measure on missing zeros."""
    with pytest.raises(ValueError, match="missing transcribed items"):
        accounts.group_accounts("X", 2023, ROWS[:5])
    acc = accounts.group_accounts("X", 2023, ROWS)
    assert acc["revenue"] == 1000.0 and acc.get("specific_levies") is None


def test_cash_costs_exclude_construction_and_specific_levies() -> None:
    """Construction is billed at cost; the State's levies are a destination (C-03)."""
    acc = accounts.group_accounts("X", 2023, ROWS)
    # 20 + 80 + (130 − 100) + 60 + (100 − 0,8 × 100) + 5 − 5 − 10 = 200
    assert accounts.cash_operating_costs(acc, levy_share=0.8) == pytest.approx(200.0)
    detailed = accounts.group_accounts(
        "X",
        2023,
        [*ROWS, {"entity": "X", "year": 2023, "item": "specific_levies", "value_meur": 90.0}],
    )
    assert accounts.specific_levies(detailed, levy_share=0.8) == 90.0


def test_two_bases_and_two_depreciations() -> None:
    """Net accounting base vs gross historical cost; booked vs technical depreciation."""
    acc = accounts.group_accounts("X", 2023, ROWS)
    assert accounts.asset_base(acc, "net") == 3000.0
    assert accounts.asset_base(acc, "gross") == 5800.0
    assert accounts.depreciation(acc, "accounting", 60.0) == 200.0
    # other assets 20 + (6000 − 200) / 58 = 120
    assert accounts.depreciation(acc, "technical", 58.0) == pytest.approx(120.0)


def test_balance_sheet_check_catches_a_wrong_column() -> None:
    """6000 − 3000 − (200 − 50) + 100 = 2950: closes; a shifted net value does not."""
    acc = accounts.group_accounts("X", 2023, ROWS)
    assert accounts.balance_sheet_closes(acc)
    wrong = accounts.group_accounts(
        "X", 2023, [r if r["item"] != "net_domain" else {**r, "value_meur": 3100.0} for r in ROWS]
    )
    assert not accounts.balance_sheet_closes(wrong)


def test_concession_year_carries_the_choices() -> None:
    """The assembled row is exactly the four D-15 inputs under the named choices."""
    acc = accounts.group_accounts("X", 2023, ROWS)
    row = accounts.concession_year(
        acc, base="gross", dep="technical", technical_life_years=58.0, levy_share=0.8
    )
    assert (row.company, row.year, row.revenue) == ("X", 2023, 1000.0)
    assert (row.operating_costs, row.depreciation, row.asset_base) == (200.0, 120.0, 5800.0)
