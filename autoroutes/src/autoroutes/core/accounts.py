"""Pure transforms from transcribed accounts to D-15 concession-years.

The frozen sources are PDFs (group accounts, ART syntheses); their figures
are transcribed by hand into `data/transcribed/comptes-2023.csv`, one row
per (entity, year, item) with the source id and page (T-01). This module
turns those rows into the `ConcessionYear` inputs of `core/rent.py` under
explicit choices:

- cash operating costs exclude the sector-specific levies (TAT, redevance
  domaniale, AFITF contribution, TEITLD): they are a DESTINATION of the
  surplus — the State's share — not a cost of an efficient supply (C-03).
  Where the accounts do not detail them (ASF-Escota, Cofiroute), their share
  of "impôts et taxes" is the parameter H-08, read from APRR-Area's note;
- two asset bases are computed for every group (D-02): the accounting NET
  value of the concession assets (subsidies netted, depreciated over the
  contract by the "caducité" rule) and the GROSS historical cost net of
  subsidies (as if nothing had been depreciated) — the widest plausible base;
- two depreciation charges: the accounting one (contract life) and a
  TECHNICAL one that spreads the gross infrastructure cost over the life H-06.

No I/O, no clock. Money in M€.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from autoroutes.core.rent import ConcessionYear

Base = Literal["net", "gross"]
Depreciation = Literal["accounting", "technical"]

REQUIRED_ITEMS = (
    "revenue",
    "ancillary_income",
    "construction_revenue",
    "purchases",
    "external_services",
    "subcontracting_incl_construction",
    "taxes",
    "personnel",
    "other_operating",
    "depreciation",
    "depreciation_domain",
    "provisions",
    "gross_domain",
    "subsidies_gross",
    "accumulated_amortisation",
    "net_domain",
    "tangible_net",
)


@dataclass(frozen=True)
class GroupAccounts:
    """One concession group's transcribed accounts for one year, M€ (T-01)."""

    entity: str
    year: int
    items: dict[str, float]

    def __getitem__(self, item: str) -> float:
        return self.items[item]

    def get(self, item: str) -> float | None:
        """Return an item or None when the accounts do not carry it."""
        return self.items.get(item)


def group_accounts(entity: str, year: int, rows: list[dict[str, object]]) -> GroupAccounts:
    """Collect the (item → value) pairs of one entity-year from the transcribed rows.

    Missing required items are an error: a measure must not silently run on
    a partial transcription.
    """
    items = {
        str(row["item"]): float(str(row["value_meur"]))
        for row in rows
        if row["entity"] == entity and int(str(row["year"])) == year
    }
    missing = [item for item in REQUIRED_ITEMS if item not in items]
    if missing:
        msg = f"{entity} {year}: missing transcribed items {missing}"
        raise ValueError(msg)
    return GroupAccounts(entity=entity, year=year, items=items)


def specific_levies(acc: GroupAccounts, levy_share: float) -> float:
    """Sector-specific levies, M€: transcribed when detailed, else H-08 × taxes."""
    detailed = acc.get("specific_levies")
    return detailed if detailed is not None else levy_share * acc["taxes"]


def cash_operating_costs(acc: GroupAccounts, levy_share: float) -> float:
    """Cash costs of running the network, M€, excluding the State's specific levies.

    Construction costs (IFRIC 12, billed at cost as construction revenue)
    are removed from subcontracting; provisions are kept (they fund the
    maintenance obligations); the net "other operating" income is deducted.
    """
    subcontracting = acc["subcontracting_incl_construction"] - acc["construction_revenue"]
    general_taxes = acc["taxes"] - specific_levies(acc, levy_share)
    return (
        acc["purchases"]
        + acc["external_services"]
        + subcontracting
        + acc["personnel"]
        + general_taxes
        + acc["provisions"]
        - acc["other_operating"]
        - acc["ancillary_income"]
    )


def asset_base(acc: GroupAccounts, base: Base) -> float:
    """D-02 asset base, M€: accounting net value, or gross historical cost net of subsidies."""
    if base == "net":
        return acc["net_domain"] + acc["tangible_net"]
    return acc["gross_domain"] - acc["subsidies_gross"]


def depreciation(acc: GroupAccounts, mode: Depreciation, technical_life_years: float) -> float:
    """Depreciation charge, M€: as booked (contract life), or the gross cost over H-06."""
    if mode == "accounting":
        return acc["depreciation"]
    other_assets = acc["depreciation"] - acc["depreciation_domain"]
    return other_assets + (acc["gross_domain"] - acc["subsidies_gross"]) / technical_life_years


def concession_year(
    acc: GroupAccounts,
    *,
    base: Base,
    dep: Depreciation,
    technical_life_years: float,
    levy_share: float,
) -> ConcessionYear:
    """Assemble the D-15 inputs of one group-year under the named choices."""
    return ConcessionYear(
        company=acc.entity,
        year=acc.year,
        revenue=acc["revenue"],
        operating_costs=cash_operating_costs(acc, levy_share),
        depreciation=depreciation(acc, dep, technical_life_years),
        asset_base=asset_base(acc, base),
    )


def balance_sheet_closes(acc: GroupAccounts, tolerance_meur: float = 1.0) -> bool:
    """Check gross − amortisation − net subsidies + work in progress ≈ published net value.

    A transcription error (wrong page, wrong column) shows up here before it
    reaches any measure.
    """
    rebuilt = (
        acc["gross_domain"]
        - acc["accumulated_amortisation"]
        - (acc["subsidies_gross"] - acc.items.get("subsidies_amortised", 0.0))
        + acc.items.get("work_in_progress", 0.0)
    )
    return abs(rebuilt - acc["net_domain"]) <= tolerance_meur
