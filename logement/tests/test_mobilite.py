"""Behaviour tests for the pure residential-rotation core (S-27 L_STAY)."""

from __future__ import annotations

import pandas as pd
import pytest
from hypothesis import given
from hypothesis import strategies as st

from logement.core import mobilite

CLASSES = list(mobilite.LSTAY_CLASSES)


def _long(
    counts: dict[tuple[str, str, int], list[float]], *, total_drift: float = 0.0
) -> pd.DataFrame:
    """Explode {(level, geo, year): [6 class counts]} into the Melodi long shape."""
    rows: list[dict[str, object]] = []
    for (level, geo, year), values in counts.items():
        for cls, value in zip(CLASSES, values, strict=True):
            rows.append(
                {
                    "GEO_OBJECT": level,
                    "GEO": geo,
                    "TIME_PERIOD": f"{year}-01-01",
                    "L_STAY": cls,
                    "OBS_VALUE": value,
                }
            )
        rows.append(
            {
                "GEO_OBJECT": level,
                "GEO": geo,
                "TIME_PERIOD": f"{year}-01-01",
                "L_STAY": mobilite.LSTAY_TOTAL,
                "OBS_VALUE": sum(values) + total_drift,
            }
        )
    return pd.DataFrame(rows)


def _national(values_by_year: dict[int, list[float]]) -> dict[tuple[str, str, int], list[float]]:
    return {("FRANCE", "F", year): values for year, values in values_by_year.items()}


BASE_2012 = [130.0, 200.0, 170.0, 200.0, 120.0, 180.0]  # total 1000
BASE_2017 = [125.0, 200.0, 170.0, 205.0, 120.0, 180.0]
BASE_2023 = [110.0, 210.0, 180.0, 200.0, 120.0, 180.0]


def test_parse_lstay_requires_columns() -> None:
    """A missing column is a definite reject, not a silent skip."""
    with pytest.raises(mobilite.MobiliteError, match="missing L_STAY column"):
        mobilite.parse_lstay(pd.DataFrame({"GEO": ["F"]}))


def test_parse_lstay_requires_every_class() -> None:
    """A cut without one of the six classes cannot be published."""
    raw = _long(_national({2012: BASE_2012}))
    with pytest.raises(mobilite.MobiliteError, match="missing L_STAY class Y2T4"):
        mobilite.parse_lstay(raw[raw["L_STAY"] != "Y2T4"])


def test_parse_lstay_rejects_class_sum_drift() -> None:
    """Classes that stop re-summing to the diffused total are a parse error."""
    raw = _long(_national({2012: BASE_2012}), total_drift=5.0)
    with pytest.raises(mobilite.MobiliteError, match="drift"):
        mobilite.parse_lstay(raw)


def test_rotation_parts_shares() -> None:
    """Per-class shares and the recent-mover aggregates are plain ratios."""
    wide = mobilite.parse_lstay(_long(_national({2012: BASE_2012})))
    parts = mobilite.rotation_parts(wide)
    row = parts.loc[("FRANCE", "F", 2012)]
    assert row["moins_2_ans_pct"] == pytest.approx(13.0)
    assert row["moins_5_ans_pct"] == pytest.approx(33.0)
    assert row["rp_total"] == pytest.approx(1000.0)


def test_national_rotation_deltas() -> None:
    """The national block carries the three vintages and the 2012→2023 drop."""
    parts = mobilite.rotation_parts(
        mobilite.parse_lstay(_long(_national({2012: BASE_2012, 2017: BASE_2017, 2023: BASE_2023})))
    )
    national = mobilite.national_rotation(parts)
    assert national["parts_par_millesime"]["2012"]["moins_2_ans_pct"] == 13.0
    assert national["parts_par_millesime"]["2023"]["moins_2_ans_pct"] == 11.0
    assert national["delta_moins_2_ans_pts"] == -2.0
    # 2 lost points of a 1000-dwelling stock -> 20 missing recent move-ins.
    assert national["emmenagements_recents_manquants"] == 20


def test_national_rotation_requires_every_vintage() -> None:
    """A missing vintage is a definite reject (the drop would be meaningless)."""
    parts = mobilite.rotation_parts(
        mobilite.parse_lstay(_long(_national({2012: BASE_2012, 2023: BASE_2023})))
    )
    with pytest.raises(mobilite.MobiliteError, match="vintage 2017 missing"):
        mobilite.national_rotation(parts)


def _ze_counts() -> dict[tuple[str, str, int], list[float]]:
    return {
        ("ZE2020", "0051", 2012): BASE_2012,
        ("ZE2020", "0051", 2023): BASE_2023,
        ("ZE2020", "0052", 2012): [100.0, 200.0, 170.0, 200.0, 120.0, 180.0],
        ("ZE2020", "0052", 2023): [120.0, 210.0, 180.0, 200.0, 120.0, 180.0],
    }


def test_rotation_by_ze_levels_and_deltas() -> None:
    """Per-ZE frame carries the last-vintage level and the 2012→2023 delta."""
    parts = mobilite.rotation_parts(mobilite.parse_lstay(_long(_ze_counts())))
    frame = mobilite.rotation_by_ze(parts)
    assert frame.loc["0051", "part_recents_pct"] == pytest.approx(11.0)
    assert frame.loc["0051", "delta_pts"] == pytest.approx(-2.0)
    assert frame.loc["0052", "delta_pts"] > 0


def test_rotation_by_ze_requires_ze_rows() -> None:
    """A cut without the ZE2020 level cannot feed the territorial frame."""
    parts = mobilite.rotation_parts(mobilite.parse_lstay(_long(_national({2012: BASE_2012}))))
    with pytest.raises(mobilite.MobiliteError, match="ZE2020 rows missing"):
        mobilite.rotation_by_ze(parts)


def _summary() -> dict[str, object]:
    parts = mobilite.rotation_parts(mobilite.parse_lstay(_long(_ze_counts())))
    frame = mobilite.rotation_by_ze(parts)
    idx = frame.index
    return mobilite.build_summary(
        frame,
        {"delta_moins_2_ans_pts": -2.0},
        tendue=pd.Series([True, False], index=idx),
        structural_rate_pct=pd.Series([2.0, 6.0], index=idx),
        indice_cout_pct=pd.Series([0.9, 0.4], index=idx),
        ze_names=pd.Series(["Alpha", "Beta"], index=idx),
    )


def test_build_summary_counts_and_medians() -> None:
    """Falling-ZE count and tension medians read straight off the frame."""
    payload = _summary()
    assert payload["n_ze"] == 2
    assert payload["n_ze_en_baisse"] == 1
    assert payload["mediane_delta_par_tension"]["tendues_pts"] == -2.0
    assert payload["mediane_delta_par_tension"]["n_tendues"] == 1


def test_build_summary_hausse_list_only_positive() -> None:
    """The rising-ZE list carries only positive deltas, ranked descending."""
    payload = _summary()
    hausses = payload["ze_en_hausse"]
    assert [h["ze"] for h in hausses] == ["0052"]
    assert all(h["delta_pts"] > 0 for h in hausses)


@given(
    st.lists(st.floats(min_value=1.0, max_value=1e6), min_size=6, max_size=6),
    st.lists(st.floats(min_value=1.0, max_value=1e6), min_size=6, max_size=6),
)
def test_property_shares_bounded_and_consistent(v12: list[float], v23: list[float]) -> None:
    """Shares stay in [0, 100], and 'moins de 5 ans' dominates 'moins de 2 ans'."""
    counts = {("ZE2020", "0051", 2012): v12, ("ZE2020", "0051", 2023): v23}
    parts = mobilite.rotation_parts(mobilite.parse_lstay(_long(counts)))
    class_parts = parts[CLASSES]
    assert ((class_parts >= 0) & (class_parts <= 100)).all().all()
    assert class_parts.sum(axis=1).round(6).eq(100.0).all()
    assert (parts["moins_5_ans_pct"] >= parts["moins_2_ans_pct"]).all()
    frame = mobilite.rotation_by_ze(parts)
    assert (
        frame["delta_pts"] == frame["part_recents_pct"] - frame["part_recents_debut_pct"]
    ).all()
