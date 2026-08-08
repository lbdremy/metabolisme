"""Behaviour tests for the pure transaction-cost core (S-30/S-31/S-32)."""

from __future__ import annotations

import pandas as pd
import pytest
from hypothesis import given
from hypothesis import strategies as st

from logement.core import transaction


def _dvf(rows: list[dict[str, object]]) -> pd.DataFrame:
    defaults = {
        "id_mutation": "m1",
        "nature_mutation": "Vente",
        "valeur_fonciere": 200_000.0,
        "code_commune": "1001",
        "type_local": "Maison",
        "surface_reelle_bati": 100.0,
    }
    return pd.DataFrame([{**defaults, **r} for r in rows])


def test_parse_dvf_requires_columns() -> None:
    """A missing column is a definite reject, not a silent skip."""
    with pytest.raises(transaction.TransactionError, match="missing DVF column"):
        transaction.parse_dvf_sales(pd.DataFrame({"id_mutation": ["m1"]}))


def test_parse_dvf_keeps_single_dwelling_sales_only() -> None:
    """Multi-dwelling and commercial-mixed mutations are dropped whole."""
    raw = _dvf(
        [
            {"id_mutation": "m1"},
            {"id_mutation": "m2", "type_local": "Maison"},
            {"id_mutation": "m2", "type_local": "Appartement"},
            {"id_mutation": "m3", "type_local": "Maison"},
            {"id_mutation": "m3", "type_local": "Local industriel. commercial ou assimilé"},
            {"id_mutation": "m4", "type_local": "Dépendance", "surface_reelle_bati": None},
            {"id_mutation": "m4", "type_local": "Appartement", "surface_reelle_bati": 50.0},
        ]
    )
    sales = transaction.parse_dvf_sales(raw)
    assert sorted(sales["type_local"]) == ["Appartement", "Maison"]


def test_parse_dvf_applies_plausibility_bounds() -> None:
    """Symbolic prices and implausible price/m² are apparatus noise."""
    raw = _dvf(
        [
            {"id_mutation": "m1"},
            {"id_mutation": "m2", "valeur_fonciere": 1.0},
            {"id_mutation": "m3", "valeur_fonciere": 4_000_000.0, "surface_reelle_bati": 20.0},
        ]
    )
    sales = transaction.parse_dvf_sales(raw)
    assert len(sales) == 1
    assert sales.iloc[0]["valeur"] == 200_000.0


def test_parse_dvf_normalises_commune_codes() -> None:
    """Codes are zero-padded and PLM arrondissements mapped to the parent."""
    raw = _dvf(
        [
            {"id_mutation": "m1", "code_commune": "1001"},
            {"id_mutation": "m2", "code_commune": "75101"},
        ]
    )
    sales = transaction.parse_dvf_sales(raw)
    assert set(sales["code"]) == {"01001", "75056"}


def test_emoluments_match_service_public_example() -> None:
    """The S-32 fiche's own worked example: 200 000 € -> 1 995,25 € HT."""
    hors_tva = transaction.emoluments_ttc(200_000.0) / transaction.VAT
    assert hors_tva == pytest.approx(1_995.25, abs=0.01)


def test_transaction_frame_scenarios_and_months() -> None:
    """The toll carries every H-13 scenario and the living-standard weight."""
    prix = pd.DataFrame(
        {"prix_median": [200_000.0], "prix_m2_median": [2_500.0], "n_ventes": [100]},
        index=pd.Index(["0051"], name="ze"),
    )
    niveau_vie = pd.Series([24_000.0], index=prix.index)
    frame = transaction.transaction_frame(
        prix, niveau_vie, {"bas": 5.09, "central": 6.32, "haut": 6.32}
    )
    droits = 200_000.0 * 0.0632
    emoluments = transaction.emoluments_ttc(200_000.0)
    assert frame.loc["0051", "cout_transaction_central"] == pytest.approx(droits + emoluments)
    assert frame.loc["0051", "cout_en_mois_niveau_vie"] == pytest.approx(
        (droits + emoluments) / 2_000.0
    )
    assert frame.loc["0051", "cout_transaction_bas"] < frame.loc["0051", "cout_transaction_central"]


def test_transaction_frame_requires_central() -> None:
    """The scenario dict must carry a central rate (the published figure)."""
    prix = pd.DataFrame(
        {"prix_median": [100_000.0], "prix_m2_median": [2_000.0], "n_ventes": [10]},
        index=pd.Index(["0051"], name="ze"),
    )
    with pytest.raises(transaction.TransactionError, match="central"):
        transaction.transaction_frame(prix, pd.Series(dtype=float), {"bas": 5.0})


def test_build_summary_medians_by_tension() -> None:
    """Tension medians and toll rankings read straight off the frame."""
    idx = pd.Index(["0051", "0052"], name="ze")
    prix = pd.DataFrame(
        {
            "prix_median": [300_000.0, 80_000.0],
            "prix_m2_median": [4_000.0, 1_200.0],
            "n_ventes": [500, 200],
        },
        index=idx,
    )
    frame = transaction.transaction_frame(
        prix, pd.Series([24_000.0, 20_000.0], index=idx), {"central": 6.32}
    )
    payload = transaction.build_summary(
        frame,
        {"prix_median_eur": 182_000},
        tendue=pd.Series([True, False], index=idx),
        indice_cout_pct=pd.Series([0.9, 0.4], index=idx),
        ze_names=pd.Series(["Alpha", "Beta"], index=idx),
        hypothesis={"id": "H-13"},
    )
    assert payload["n_ze"] == 2
    assert payload["mediane_par_tension"]["n_tendues"] == 1
    assert payload["peage_le_plus_lourd"][0]["ze"] == "0051"
    assert (
        payload["mediane_par_tension"]["tendues_mois"]
        > payload["mediane_par_tension"]["autres_mois"]
    )


@given(st.floats(min_value=0.0, max_value=5_000_000.0))
def test_property_emoluments_monotone_and_bounded(prix: float) -> None:
    """Fees grow with the price and stay below the top marginal rate."""
    fee = transaction.emoluments_ttc(prix)
    assert fee >= 0.0
    assert fee <= prix * 0.03870 * transaction.VAT + 1e-6
    assert transaction.emoluments_ttc(prix + 1_000.0) >= fee
