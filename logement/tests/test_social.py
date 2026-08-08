"""Behaviour tests for the pure social-housing mobility core (S-28 RPLS)."""

from __future__ import annotations

import pandas as pd
import pytest
from hypothesis import given
from hypothesis import strategies as st

from logement.core import social


def _communes(rows: list[dict[str, object]]) -> pd.DataFrame:
    defaults = {
        "nb_ls": 100,
        "nb_ls2019": 100,
        "nb_ls2013": 100,
        "tx_mob": 8.0,
        "tx_mob_2019": 10.0,
        "tx_mob_2013": 10.0,
        "tx_vac": 2.0,
        "tx_vac3": 1.0,
    }
    return pd.DataFrame([{"DEPCOM_ARM": r["code"], **{**defaults, **r}} for r in rows]).drop(
        columns=["code"]
    )


def test_parse_rpls_requires_columns() -> None:
    """A missing column is a definite reject, not a silent skip."""
    with pytest.raises(social.SocialError, match="missing RPLS column"):
        social.parse_rpls_communes(pd.DataFrame({"DEPCOM_ARM": ["01001"]}))


def test_parse_rpls_maps_plm_and_keeps_missing() -> None:
    """PLM arrondissements map to the parent; secret cells stay missing."""
    raw = _communes([{"code": "75101"}, {"code": "01001", "tx_mob": None}])
    out = social.parse_rpls_communes(raw)
    assert out.loc[0, "code"] == "75056"
    assert pd.isna(out.loc[1, "tx_mob"])


def _national(serie_2025: float = 8.0, serie_2019: float = 10.0) -> dict[str, object]:
    serie = {str(y): 10.0 for y in range(2013, 2025)}
    serie["2019"] = serie_2019
    serie["2025"] = serie_2025
    return {
        "serie_mobilite_pct": serie,
        "vacance_pct": 2.0,
        "vacance_plus_3_mois_pct": 1.0,
        "parc_social": 200,
    }


def test_control_aggregation_passes_within_tolerance() -> None:
    """The C-09 control returns per-vintage drifts when they stay small."""
    communes = social.parse_rpls_communes(_communes([{"code": "01001"}, {"code": "01002"}]))
    drifts = social.control_aggregation(communes, _national())
    assert drifts["2025"] == 0.0


def test_control_aggregation_rejects_drift() -> None:
    """A weighted aggregate that drifts from the published rate is a hard error."""
    communes = social.parse_rpls_communes(_communes([{"code": "01001"}]))
    with pytest.raises(social.SocialError, match="C-09 aggregation drifts"):
        social.control_aggregation(communes, _national(serie_2025=9.0))


def test_social_by_ze_weights_by_vintage_stock() -> None:
    """Each vintage rate is weighted by that vintage's stock, not today's."""
    communes = social.parse_rpls_communes(
        _communes(
            [
                {
                    "code": "01001",
                    "tx_mob": 4.0,
                    "nb_ls": 300,
                    "tx_mob_2019": 20.0,
                    "nb_ls2019": 100,
                },
                {
                    "code": "01002",
                    "tx_mob": 8.0,
                    "nb_ls": 100,
                    "tx_mob_2019": 10.0,
                    "nb_ls2019": 300,
                },
            ]
        )
    )
    commune_ze = pd.DataFrame({"code": ["01001", "01002"], "ze": ["0051", "0051"]})
    frame = social.social_by_ze(communes, commune_ze)
    assert frame.loc["0051", "tx_mob_2025"] == pytest.approx(5.0)  # (4*300+8*100)/400
    assert frame.loc["0051", "tx_mob_2019"] == pytest.approx(12.5)  # (20*100+10*300)/400
    assert frame.loc["0051", "delta_2019_2025"] == pytest.approx(-7.5)


def _summary(parc_small: int = 50) -> dict[str, object]:
    communes = social.parse_rpls_communes(
        _communes(
            [
                {"code": "01001", "tx_mob": 4.0, "nb_ls": 1000},
                {"code": "01002", "tx_mob": 9.0, "nb_ls": 800},
                {"code": "01003", "tx_mob": 18.0, "nb_ls": parc_small},
            ]
        )
    )
    commune_ze = pd.DataFrame({"code": ["01001", "01002", "01003"], "ze": ["0051", "0052", "0053"]})
    frame = social.social_by_ze(communes, commune_ze)
    idx = pd.Index(["0051", "0052", "0053"], name="ze")
    rotation = pd.DataFrame(
        {"part_recents_pct": [12.0, 10.0, 11.0], "delta_pts": [-2.0, -1.0, -1.5]}, index=idx
    )
    return social.build_summary(
        frame,
        _national(),
        {"2025": 0.0},
        tendue=pd.Series([True, False, False], index=idx),
        structural_rate_pct=pd.Series([2.0, 5.0, 4.0], index=idx),
        indice_cout_pct=pd.Series([0.9, 0.4, 0.5], index=idx),
        rotation=rotation,
        ze_names=pd.Series(["Alpha", "Beta", "Gamma"], index=idx),
    )


def test_build_summary_applies_stock_threshold() -> None:
    """ZE under the social-stock floor stay out of rankings and counts."""
    payload = _summary()
    assert payload["n_ze_total"] == 3
    assert payload["n_ze_sous_seuil"] == 1
    assert payload["n_ze"] == 2
    listed = {e["ze"] for e in payload["mobilite_la_plus_faible"]}
    assert "0053" not in listed


def test_build_summary_tension_medians() -> None:
    """Tension medians read straight off the filtered frame."""
    payload = _summary()
    assert payload["mediane_par_tension"]["tendues"]["tx_mob_2025_pct"] == 4.0
    assert payload["mediane_par_tension"]["autres"]["tx_mob_2025_pct"] == 9.0
    assert payload["mediane_par_tension"]["n_tendues"] == 1
    assert payload["n_ze_en_baisse_2019_2025"] == 2


@given(
    st.lists(
        st.tuples(
            st.floats(min_value=0.0, max_value=30.0),
            st.integers(min_value=1, max_value=10_000),
        ),
        min_size=1,
        max_size=6,
    )
)
def test_property_weighted_rate_bounded(pairs: list[tuple[float, int]]) -> None:
    """A stock-weighted mean stays within the min-max envelope of the rates."""
    rows = [
        {"code": f"010{i:02d}", "tx_mob": rate, "nb_ls": stock}
        for i, (rate, stock) in enumerate(pairs)
    ]
    communes = social.parse_rpls_communes(_communes(rows))
    commune_ze = pd.DataFrame({"code": communes["code"], "ze": "0051"})
    frame = social.social_by_ze(communes, commune_ze)
    rates = [rate for rate, _ in pairs]
    assert min(rates) - 1e-9 <= frame.loc["0051", "tx_mob_2025"] <= max(rates) + 1e-9
