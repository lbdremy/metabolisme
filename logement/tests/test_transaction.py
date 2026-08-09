"""Behaviour tests for the pure transaction-cost core (S-30/S-31/S-32/S-37)."""

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
    """Multi-dwelling and commercial-mixed mutations are dropped whole — and counted."""
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
    sales, counts = transaction.parse_dvf_sales(raw)
    assert sorted(sales["type_local"]) == ["Appartement", "Maison"]
    # HD-6: what the convention removes is published, not silently lost.
    assert counts["n_mutations_multi_logements"] == 1
    assert counts["n_logements_en_mutations_multi"] == 2
    assert counts["n_mutations_un_logement_avec_commercial"] == 1
    assert counts["n_mutations_un_logement"] == 2


def test_parse_dvf_flags_implausible_rows_instead_of_dropping() -> None:
    """Symbolic prices and implausible price/m² are flagged (unknown keeps)."""
    raw = _dvf(
        [
            {"id_mutation": "m1"},
            {"id_mutation": "m2", "valeur_fonciere": 1.0},
            {"id_mutation": "m3", "valeur_fonciere": 4_000_000.0, "surface_reelle_bati": 20.0},
        ]
    )
    sales, counts = transaction.parse_dvf_sales(raw)
    assert len(sales) == 3
    assert counts["n_ventes_retenues"] == 1
    assert counts["n_ventes_hors_bornes"] == 2
    assert sales.loc[~sales["hors_bornes"], "valeur"].iloc[0] == 200_000.0


def test_parse_dvf_normalises_commune_codes_and_rates() -> None:
    """Codes are zero-padded, PLM mapped to the parent, S-31 rates attached."""
    raw = _dvf(
        [
            {"id_mutation": "m1", "code_commune": "1001"},
            {"id_mutation": "m2", "code_commune": "75101"},
            {"id_mutation": "m3", "code_commune": "6088"},
            {"id_mutation": "m4", "code_commune": "36044"},
        ]
    )
    sales, _counts = transaction.parse_dvf_sales(raw)
    by_code = sales.set_index("code")["taux_dmto_pct"]
    assert set(by_code.index) == {"01001", "75056", "06088", "36044"}
    assert by_code["01001"] == pytest.approx(6.3185)  # voted 5.00
    assert by_code["06088"] == pytest.approx(5.80665)  # Alpes-Maritimes at 4.50
    assert by_code["36044"] == pytest.approx(5.09006)  # Indre at 3.80


def test_dmto_rate_checks() -> None:
    """The three published rate levels come out of the exact formula."""
    assert transaction.dmto_total_rate_pct("13") == pytest.approx(6.3185)
    assert transaction.dmto_total_rate_pct("971") == pytest.approx(5.80665)
    assert transaction.dmto_total_rate_pct("976") == pytest.approx(5.09006)
    assert pytest.approx(5.81) == transaction.DMTO_COMMON_LAW_TOTAL_PCT


def test_csi_rate_and_floor() -> None:
    """S-37: 0.10 % of the price with a 15 € floor."""
    assert transaction.csi_eur(200_000.0) == pytest.approx(200.0)
    assert transaction.csi_eur(1_000.0) == pytest.approx(15.0)


def test_emoluments_match_service_public_example() -> None:
    """The S-32 fiche's own worked example: 200 000 € -> 1 995,25 € HT."""
    hors_tva = transaction.emoluments_ttc(200_000.0) / transaction.VAT
    assert hors_tva == pytest.approx(1_995.25, abs=0.01)


def _prices(sales_rows: list[dict[str, object]]) -> tuple[pd.DataFrame, dict[str, object]]:
    sales, _counts = transaction.parse_dvf_sales(_dvf(sales_rows))
    commune_ze = pd.DataFrame({"code": ["01001", "06088"], "ze": ["0051", "0052"]})
    return transaction.prices_by_ze(sales, commune_ze)


def test_prices_by_ze_counts_unjoined_and_out_of_bounds() -> None:
    """ST-8/HD-7: unjoined sales and per-ZE out-of-bounds counts are published."""
    frame, coverage = _prices(
        [
            {"id_mutation": "m1", "code_commune": "1001"},
            {"id_mutation": "m2", "code_commune": "1001", "valeur_fonciere": 1.0},
            {"id_mutation": "m3", "code_commune": "99999"},
        ]
    )
    assert coverage["n_ventes_sans_ze"] == 1
    assert coverage["n_communes_sans_ze"] == 1
    assert frame.loc["0051", "n_ventes"] == 1
    assert frame.loc["0051", "n_ventes_hors_bornes"] == 1


def _frame_for_summary() -> pd.DataFrame:
    frame, _coverage = _prices(
        [
            {"id_mutation": "m1", "code_commune": "1001", "valeur_fonciere": 300_000.0},
            {"id_mutation": "m2", "code_commune": "6088", "valeur_fonciere": 80_000.0},
        ]
    )
    niveau_vie = pd.Series([24_000.0, 20_000.0], index=frame.index)
    return transaction.transaction_frame(
        frame,
        niveau_vie,
        {"bas": 5.09, "droit_commun_primo": 5.81, "central": 6.32},
    )


def test_transaction_frame_territorialised_and_scenarios() -> None:
    """The headline toll uses the per-ZE S-31 rate; scenarios stay uniform."""
    frame = _frame_for_summary()
    prix = 300_000.0
    attendu = prix * 6.3185 / 100 + transaction.emoluments_ttc(prix) + transaction.csi_eur(prix)
    assert frame.loc["0051", "cout_transaction_territorialise"] == pytest.approx(attendu)
    # ZE 0052 is in the Alpes-Maritimes: territorialized BELOW the central scenario.
    assert (
        frame.loc["0052", "cout_transaction_territorialise"]
        < frame.loc["0052", "cout_transaction_central"]
    )
    assert frame.loc["0051", "cout_en_mois_niveau_vie"] == pytest.approx(attendu / 2_000.0)
    assert 0 < frame.loc["0051", "part_fiscale_pct"] < 100
    assert frame.loc["0051", "cout_en_mois_bas"] < frame.loc["0051", "cout_en_mois_central"]


def test_transaction_frame_requires_central() -> None:
    """The scenario dict must carry a central rate (the published figure)."""
    frame, _coverage = _prices([{"id_mutation": "m1", "code_commune": "1001"}])
    with pytest.raises(transaction.TransactionError, match="central"):
        transaction.transaction_frame(frame, pd.Series(dtype=float), {"bas": 5.0})


def _summary(tendue: pd.Series | None = None) -> dict[str, object]:
    frame = _frame_for_summary()
    idx = frame.index
    return transaction.build_summary(
        frame,
        {"prix_median_eur": 182_000},
        {"n_mutations_multi_logements": 0},
        {"n_ventes_sans_ze": 0},
        tendue if tendue is not None else pd.Series([True, False], index=idx),
        indice_cout_pct=pd.Series([0.9, 0.4], index=idx),
        ze_names=pd.Series(["Alpha", "Beta"], index=idx),
        hypothesis={"id": "H-13"},
        tendue_variants={"h08_5_pct": pd.Series([False, False], index=idx)},
    )


def test_build_summary_medians_scenarios_and_annualisation() -> None:
    """Tension medians, named scenarios and the annualisation grid are published."""
    payload = _summary()
    assert payload["n_ze"] == 2
    assert payload["mediane_par_tension"]["n_tendues"] == 1
    assert (
        payload["mediane_par_tension"]["tendues_mois"]
        > payload["mediane_par_tension"]["autres_mois"]
    )
    assert set(payload["scenarios_h13_mois"]) == {"bas", "droit_commun_primo", "central"}
    assert (
        payload["scenarios_h13_mois"]["bas"]["mediane_mois"]
        < payload["scenarios_h13_mois"]["central"]["mediane_mois"]
    )
    annualise = payload["peage_annualise"]["detention_20_ans"]
    assert annualise["mediane_pct_niveau_vie_annuel"] is not None
    assert payload["part_fiscale_mediane_pct"] > 50


def test_build_summary_ranking_threshold_and_bornes_warning() -> None:
    """Thin ZE stay out of rankings; bound-sensitive ZE are named."""
    payload = _summary()
    # Both fixture ZE carry a single sale — far under the ranking floor.
    assert payload["seuil_ventes_classement"] == transaction.MIN_VENTES_CLASSEMENT
    assert payload["n_ze_sous_seuil_classement"] == 2
    assert payload["peage_le_plus_lourd"] == []
    assert payload["assiette_c10"] == {"n_mutations_multi_logements": 0}
    assert payload["couverture"] == {"n_ventes_sans_ze": 0}
    assert payload["sensibilite_h08"]["h08_5_pct"]["n_tendues"] == 0


def test_build_summary_unknown_tension_excluded() -> None:
    """HD-2: a NaN tension flag leaves BOTH medians and is counted."""
    frame = _frame_for_summary()
    payload = _summary(tendue=pd.Series([True, None], index=frame.index))
    block = payload["mediane_par_tension"]
    assert block["n_tension_inconnue"] == 1
    assert block["autres_mois"] is None


@given(st.floats(min_value=0.0, max_value=5_000_000.0))
def test_property_emoluments_monotone_and_bounded(prix: float) -> None:
    """Fees grow with the price and stay below the top marginal rate."""
    fee = transaction.emoluments_ttc(prix)
    assert fee >= 0.0
    assert fee <= prix * 0.03870 * transaction.VAT + 1e-6
    assert transaction.emoluments_ttc(prix + 1_000.0) >= fee


@given(st.sampled_from(["01", "06", "13", "36", "48", "75", "971", "974", "976"]))
def test_property_dmto_rates_within_h13_range(dep: str) -> None:
    """Every territorialized rate stays inside the H-13 plausible range."""
    rate = transaction.dmto_total_rate_pct(dep)
    assert 5.09 <= round(rate, 2) <= 6.32
