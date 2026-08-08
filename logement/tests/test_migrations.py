"""Behaviour tests for the pure person-migration core (S-29 MIGCOM)."""

from __future__ import annotations

import pandas as pd
import pytest
from hypothesis import given
from hypothesis import strategies as st

from logement.core import migrations


def _raw(rows: list[dict[str, object]]) -> pd.DataFrame:
    defaults = {"COMMUNE": "01001", "DCRAN": "01001", "IRAN": "1", "IPONDI": 1.0, "STOCD": "10"}
    return pd.DataFrame([{**defaults, **r} for r in rows])


def test_parse_migcom_requires_columns() -> None:
    """A missing column is a definite reject, not a silent skip."""
    with pytest.raises(migrations.MigrationsError, match="missing MIGCOM column"):
        migrations.parse_migcom(pd.DataFrame({"COMMUNE": ["01001"]}))


def test_parse_migcom_rejects_unknown_iran() -> None:
    """An IRAN modality outside the documented codes is a parse error."""
    with pytest.raises(migrations.MigrationsError, match="unknown IRAN"):
        migrations.parse_migcom(_raw([{"IRAN": "X"}]))


def test_parse_migcom_rejects_bad_weights() -> None:
    """Missing or negative IPONDI weights cannot feed a weighted rate."""
    with pytest.raises(migrations.MigrationsError, match="IPONDI"):
        migrations.parse_migcom(_raw([{"IPONDI": None}]))


def test_national_summary_rates_and_tenure() -> None:
    """The national block decomposes the mobile share and the tenure split."""
    frame = migrations.parse_migcom(
        _raw(
            [
                {"IRAN": "1", "IPONDI": 60.0, "STOCD": "10"},
                {"IRAN": "2", "IPONDI": 20.0, "STOCD": "21"},
                {"IRAN": "3", "IPONDI": 15.0, "STOCD": "21"},
                {"IRAN": "8", "IPONDI": 5.0, "STOCD": "22"},
                {"IRAN": "0", "IPONDI": 7.0, "STOCD": "ZZ"},
            ]
        )
    )
    national = migrations.national_summary(frame)
    assert national["population"] == 100
    assert national["poids_rattachement_exclu"] == 7
    assert national["taux_mobilite_pct"] == 40.0
    assert national["dont_meme_commune_pct"] == 20.0
    assert national["dont_autre_commune_france_pct"] == 15.0
    assert national["dont_etranger_pct"] == 5.0
    prive = national["part_mobiles_par_statut"]["locataire_prive"]
    assert prive == {"personnes": 35, "part_mobiles_pct": 100.0}
    assert national["part_mobiles_par_statut"]["proprietaire"]["part_mobiles_pct"] == 0.0


def _commune_ze() -> pd.DataFrame:
    return pd.DataFrame({"code": ["01001", "01002", "02001"], "ze": ["0051", "0051", "0052"]})


def test_migrations_by_ze_rates_and_flows() -> None:
    """Per-ZE rates, inter-ZE flows and coverage weights are all published."""
    frame = migrations.parse_migcom(
        _raw(
            [
                {"COMMUNE": "01001", "IRAN": "1", "IPONDI": 80.0},
                # moved within the same ZE (0051): mobile, not an inter-ZE flow
                {"COMMUNE": "01001", "DCRAN": "01002", "IRAN": "3", "IPONDI": 10.0},
                # moved from ZE 0052 to ZE 0051: inter-ZE flow
                {"COMMUNE": "01001", "DCRAN": "02001", "IRAN": "4", "IPONDI": 10.0},
                {"COMMUNE": "02001", "IRAN": "1", "IPONDI": 100.0},
                # residence commune unknown to the membership table
                {"COMMUNE": "99999", "IRAN": "1", "IPONDI": 3.0},
            ]
        )
    )
    ze_frame, coverage = migrations.migrations_by_ze(frame, _commune_ze())
    assert ze_frame.loc["0051", "population"] == pytest.approx(100.0)
    assert ze_frame.loc["0051", "taux_mobilite_pct"] == pytest.approx(20.0)
    assert ze_frame.loc["0051", "entrants"] == pytest.approx(10.0)
    assert ze_frame.loc["0052", "sortants"] == pytest.approx(10.0)
    assert ze_frame.loc["0051", "solde"] == pytest.approx(10.0)
    assert coverage["communes_sans_ze"] == 1
    assert coverage["poids_sans_ze"] == 3
    assert coverage["flux_inter_ze"] == 10


def test_migrations_by_ze_maps_plm_origin() -> None:
    """A PLM arrondissement origin maps to its parent commune's ZE."""
    commune_ze = pd.DataFrame({"code": ["01001", "75056"], "ze": ["0051", "1109"]})
    frame = migrations.parse_migcom(
        _raw([{"COMMUNE": "01001", "DCRAN": "75101", "IRAN": "5", "IPONDI": 4.0}])
    )
    ze_frame, coverage = migrations.migrations_by_ze(frame, commune_ze)
    assert ze_frame.loc["0051", "entrants"] == pytest.approx(4.0)
    assert coverage["poids_mobiles_sans_ze_origine"] == 0


def test_build_summary_medians_and_lists() -> None:
    """Tension medians and ranked lists read straight off the frame."""
    frame = migrations.parse_migcom(
        _raw(
            [
                {"COMMUNE": "01001", "IRAN": "1", "IPONDI": 90.0},
                {"COMMUNE": "01001", "IRAN": "2", "IPONDI": 10.0},
                {"COMMUNE": "02001", "IRAN": "1", "IPONDI": 60.0},
                {"COMMUNE": "02001", "IRAN": "2", "IPONDI": 40.0},
            ]
        )
    )
    ze_frame, coverage = migrations.migrations_by_ze(frame, _commune_ze())
    idx = ze_frame.index
    payload = migrations.build_summary(
        ze_frame,
        {"taux_mobilite_pct": 25.0},
        coverage,
        tendue=pd.Series([True, False], index=idx),
        indice_cout_pct=pd.Series([0.9, 0.4], index=idx),
        rotation=pd.DataFrame({"part_recents_pct": [12.0, 10.0]}, index=idx),
        ze_names=pd.Series(["Alpha", "Beta"], index=idx),
    )
    assert payload["n_ze"] == 2
    assert payload["mediane_par_tension"]["tendues"]["taux_mobilite_pct"] == 10.0
    assert payload["mediane_par_tension"]["autres"]["taux_mobilite_pct"] == 40.0
    assert payload["mobilite_la_plus_faible"][0]["ze"] == "0051"


@given(
    st.lists(
        st.tuples(
            st.sampled_from(["1", "2", "3", "8"]),
            st.floats(min_value=0.1, max_value=1000.0),
        ),
        min_size=1,
        max_size=12,
    )
)
def test_property_rates_bounded_and_flows_balanced(obs: list[tuple[str, float]]) -> None:
    """Mobility rates stay in [0, 100] and inter-ZE flows sum to zero."""
    rows = [
        {"COMMUNE": "01001" if i % 2 else "02001", "DCRAN": "02001" if i % 2 else "01001",
         "IRAN": iran, "IPONDI": w}
        for i, (iran, w) in enumerate(obs)
    ]
    frame = migrations.parse_migcom(_raw(rows))
    ze_frame, _coverage = migrations.migrations_by_ze(frame, _commune_ze())
    rates = ze_frame["taux_mobilite_pct"].dropna()
    assert ((rates >= 0) & (rates <= 100)).all()
    assert ze_frame["solde"].sum() == pytest.approx(0.0, abs=1e-9)
