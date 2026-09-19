"""Build stages — rebuild the M-xx artifacts from the frozen and transcribed data.

The only stage so far, `run_rent`, reads the transcribed accounts (T-01),
the parameters of `sources/hypotheses.yaml`, runs the pure core and writes
`data/processed/rente-d15.json` — the artifact declared by M-01..M-04 in
evidence/claims.yaml.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path

import yaml

from autoroutes.core import accounts, registry, rent
from autoroutes.models import HypothesisRecord, TranscribedRow

TRANSCRIBED = Path("data") / "transcribed" / "comptes-2023.csv"
RENT_OUTPUT = Path("data") / "processed" / "rente-d15.json"

MEASURED_GROUPS = ("ASF-Escota", "Cofiroute", "APRR-Area")
YEAR = 2023
# ART, S-02 p. 94 : TRI projet à terminaison 2023 des sept concessions.
ART_TRI_SEVEN_PCT = 7.9
CONTROLS = ("Vinci-Energies", "Vinci-Construction", "Vinci-Autoroutes")


def _read_transcribed(root: Path) -> list[dict[str, object]]:
    with (root / TRANSCRIBED).open(encoding="utf-8", newline="") as handle:
        rows = [TranscribedRow.model_validate(raw) for raw in csv.DictReader(handle)]
    return [row.model_dump() for row in rows]


def _hypotheses(root: Path) -> dict[str, HypothesisRecord]:
    raw = yaml.safe_load((root / "sources" / "hypotheses.yaml").read_text(encoding="utf-8"))
    return {h.id: h for h in registry.parse_hypotheses(raw)}


def _quantified(h: HypothesisRecord) -> tuple[float, float, float]:
    assert h.central_value is not None and h.plausible_range is not None
    return h.central_value, h.plausible_range[0], h.plausible_range[1]


def _rates(hyps: dict[str, HypothesisRecord]) -> dict[str, float]:
    reference, low, high = _quantified(hyps["H-01"])
    art, _, _ = _quantified(hyps["H-02"])
    state, _, _ = _quantified(hyps["H-03"])
    market, _, _ = _quantified(hyps["H-04"])
    return {
        "market_edhec": market,
        "reference_low": low,
        "reference": reference,
        "state_2017": state,
        "art": art,
        "reference_high": high,
    }


def _item(rows: list[dict[str, object]], entity: str, year: int, item: str) -> float:
    for row in rows:
        if row["entity"] == entity and row["year"] == year and row["item"] == item:
            return float(str(row["value_meur"]))
    msg = f"{entity} {year}: item {item} not transcribed"
    raise KeyError(msg)


def build_rent(root: Path) -> dict[str, object]:
    """Compute M-01..M-04 from the transcribed accounts and the registered parameters."""
    rows = _read_transcribed(root)
    hyps = _hypotheses(root)
    rates = _rates(hyps)
    life, life_low, life_high = _quantified(hyps["H-06"])
    levy_share, levy_low, levy_high = _quantified(hyps["H-08"])
    sanef_share, sanef_low, sanef_high = _quantified(hyps["H-07"])
    share_per_point, _, share_per_point_high = _quantified(hyps["H-05"])

    groups = [accounts.group_accounts(g, YEAR, rows) for g in MEASURED_GROUPS]
    balance_checks = {g.entity: accounts.balance_sheet_closes(g) for g in groups}

    # M-01 — the accounting form of D-15, per group, under four (base × depreciation)
    # variants, at every named rate; plus sensitivities on H-06 and H-08.
    variants: dict[str, list[dict[str, object]]] = {}
    for base in ("net", "gross"):
        for dep in ("accounting", "technical"):
            years = [
                accounts.concession_year(
                    g, base=base, dep=dep, technical_life_years=life, levy_share=levy_share
                )
                for g in groups
            ]
            years += rent.aggregate(years, company="Trois groupes mesurés")
            variants[f"{base}_{dep}"] = rent.surplus_table(years, rates)
    sensitivity: dict[str, dict[str, float]] = {}
    for label, kwargs in (
        ("technical_life_low", {"technical_life_years": life_low, "levy_share": levy_share}),
        ("technical_life_high", {"technical_life_years": life_high, "levy_share": levy_share}),
        ("levy_share_low", {"technical_life_years": life, "levy_share": levy_low}),
        ("levy_share_high", {"technical_life_years": life, "levy_share": levy_high}),
    ):
        dep = "technical" if label.startswith("technical") else "accounting"
        years = [accounts.concession_year(g, base="net", dep=dep, **kwargs) for g in groups]
        (total,) = rent.aggregate(years)
        sensitivity[label] = {name: rent.surplus(total, r) for name, r in rates.items()}

    # Extrapolation to the seven (H-07, H-09), on the central variant (net base,
    # accounting depreciation): Sanef-SAPN's revenue is the seven's share H-07;
    # its surplus share is bounded by the measured groups.
    central = [
        accounts.concession_year(
            g, base="net", dep="accounting", technical_life_years=life, levy_share=levy_share
        )
        for g in groups
    ]
    (measured_total,) = rent.aggregate(central)
    seven: dict[str, dict[str, float]] = {}
    for name, r in rates.items():
        shares = [s for g in central if (s := rent.surplus_share(g, r)) is not None]
        total_share = rent.surplus_share(measured_total, r) or 0.0
        sanef_revenue = measured_total.revenue * sanef_share / (100.0 - sanef_share)
        sanef_revenue_low = measured_total.revenue * sanef_low / (100.0 - sanef_low)
        sanef_revenue_high = measured_total.revenue * sanef_high / (100.0 - sanef_high)
        seven[name] = {
            "measured_surplus": rent.surplus(measured_total, r),
            "measured_revenue": measured_total.revenue,
            "sanef_sapn_revenue_central": sanef_revenue,
            "seven_surplus_central": rent.surplus(measured_total, r) + sanef_revenue * total_share,
            "seven_surplus_low": rent.surplus(measured_total, r) + sanef_revenue_low * min(shares),
            "seven_surplus_high": rent.surplus(measured_total, r)
            + sanef_revenue_high * max(shares),
            "seven_revenue_central": measured_total.revenue + sanef_revenue,
        }

    # M-02 — the sector's own aggregates (all SCA, ART): what is left before any
    # return on capital, once the State's specific levies are put back.
    sector: dict[str, dict[str, float]] = {}
    for year in (2023, 2024):
        revenue = _item(rows, "Secteur-SCA", year, "revenue")
        charges = _item(rows, "Secteur-SCA", year, "charges")
        taxes = _item(rows, "Secteur-SCA", year, "taxes")
        dep = _item(rows, "Secteur-SCA", year, "depreciation")
        levies = levy_share * taxes
        margin = revenue - (charges - levies) - dep
        sector[str(year)] = {
            "revenue": revenue,
            "charges_excluding_specific_levies": charges - levies,
            "specific_levies_estimate": levies,
            "depreciation": dep,
            "margin_before_capital": margin,
            "margin_share_of_revenue": margin / revenue,
            "income_tax": _item(rows, "Secteur-SCA", year, "income_tax"),
            "dividends": _item(rows, "Secteur-SCA", year, "dividends"),
            "net_income": _item(rows, "Secteur-SCA", year, "net_income"),
        }

    # M-03 — the regulator's form: TRI gap × H-05 × revenue of the seven (ASFA 2024).
    seven_revenue_2024 = sum(
        _item(rows, "Secteur-sept", 2024, f"revenue_{k}")
        for k in ("asf_escota", "aprr_area", "cofiroute", "sanef_sapn")
    )
    tri_gap = {
        name: {
            "rate_pct": r,
            "rent_share_of_revenue_pct": rent.rent_share_from_tri_gap(
                ART_TRI_SEVEN_PCT, r, share_per_point
            ),
            "rent_meur_per_year": rent.rent_from_tri_gap(
                ART_TRI_SEVEN_PCT, r, seven_revenue_2024, share_per_point
            ),
            "rent_meur_per_year_high_share": rent.rent_from_tri_gap(
                ART_TRI_SEVEN_PCT, r, seven_revenue_2024, share_per_point_high
            ),
        }
        for name, r in rates.items()
    }

    # M-04 — the control: the same form on VINCI's substitutable divisions and,
    # as a caveat, on VINCI Autoroutes at its acquisition-price capital base.
    control: dict[str, dict[str, object]] = {}
    for entity in CONTROLS:
        ropa = _item(rows, entity, YEAR, "ropa")
        ratio = _item(rows, entity, YEAR, "ropa_share_of_revenue")
        capital = _item(rows, entity, YEAR, "capital_employed")
        revenue = ropa / (ratio / 100.0)
        row = rent.ConcessionYear(entity, YEAR, revenue, revenue - ropa, 0.0, capital)
        control[entity] = {
            "revenue_derived": revenue,
            "ropa": ropa,
            "capital_employed": capital,
            "break_even_rate_pct": rent.break_even_rate(row),
            **{f"surplus_{name}": rent.surplus(row, r) for name, r in rates.items()},
            **{f"surplus_share_{name}": rent.surplus_share(row, r) for name, r in rates.items()},
        }

    return {
        "year": YEAR,
        "rates_pct": rates,
        "parameters": {
            "technical_life_years": life,
            "specific_levies_share_of_taxes": levy_share,
            "sanef_sapn_revenue_share_pct": sanef_share,
            "tri_seven_pct": ART_TRI_SEVEN_PCT,
            "share_per_tri_point_pct": share_per_point,
        },
        "balance_sheet_checks": balance_checks,
        "m01_groups": variants,
        "m01_sensitivity_total_net_base": sensitivity,
        "m01_seven": seven,
        "m02_sector": sector,
        "m03_tri_gap": {"seven_revenue_2024": seven_revenue_2024, "by_rate": tri_gap},
        "m04_control": control,
    }


def run_rent(root: Path) -> int:
    """Rebuild data/processed/rente-d15.json; return a process exit code."""
    payload = build_rent(root)
    checks = payload["balance_sheet_checks"]
    if not isinstance(checks, dict) or not all(checks.values()):
        print(f"build: balance sheet does not close: {checks}")
        return 1
    out = root / RENT_OUTPUT
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"build: wrote {RENT_OUTPUT}")
    return 0
