"""Pure parsing and transforms of the LOVAC open data (stabilized from
notebooks/exploration/02_vacance_territoriale.py).

All functions take already-loaded DataFrames (the cp1252/';' reads happen in
the shell) and return validated data — no I/O, no clock. Counts are dwellings
of the private stock (S-05); 's' marks statistical secrecy (< 11 vacant).
"""

from __future__ import annotations

import re

import pandas as pd

# Methodological breaks documented by S-05: 2023 (taxe d'habitation -> GMBI),
# 2025 (source data taken before the fiscal processing chain). Levels are not
# comparable across them; only the structural series is reasonably robust.
BREAK_MILLESIMES = (2023, 2025)
# Reference millésime for rates: the last one with numerator AND denominator
# before the 2025 break (recorded as choice C-03 in evidence/claims.yaml).
# Millésimes are normalized to 4 digits everywhere (the files mix '2026' in
# the France file with '_26' column suffixes in the territory files).
REFERENCE_MILLESIME = 2024

# Paris / Lyon / Marseille arrive split by arrondissement; any commune-level
# ranking must aggregate them first (code prefix -> parent commune).
PLM_CITIES: dict[str, tuple[str, str, str]] = {
    "751": ("75056", "Paris", "75"),
    "6938": ("69123", "Lyon", "69"),
    "132": ("13055", "Marseille", "13"),
}

_VALUE_COLUMN = re.compile(r"^(ff_pp_total|pp_vacant|pp_vacant_plus_2ans)_(\d{2})$")


class LovacError(Exception):
    """A LOVAC payload does not have the expected shape."""


def parse_counts(series: pd.Series) -> pd.Series:
    """Parse LOVAC counts: nbsp/space thousands separators, 's' (secret) -> NA."""
    cleaned = series.astype("string").str.replace(r"[\s\xa0]", "", regex=True)
    return pd.to_numeric(cleaned.replace("s", pd.NA), errors="coerce")


def _clean_header(raw: pd.DataFrame) -> pd.DataFrame:
    out = raw.copy()
    out.columns = [str(c).strip() for c in out.columns]
    return out


def parse_france(raw: pd.DataFrame) -> pd.DataFrame:
    """Parse the France file into a millésime-indexed frame of national counts."""
    df = _clean_header(raw)
    expected = ("Millésime", "ff_pp_total", "pp_vacant", "pp_vacant_plus_2ans")
    missing = [c for c in expected if c not in df.columns]
    if missing:
        raise LovacError(f"missing France columns: {missing}")
    out = pd.DataFrame(
        {
            "millesime": pd.to_numeric(df["Millésime"], errors="coerce"),
            "ff_pp_total": parse_counts(df["ff_pp_total"]),
            "pp_vacant": parse_counts(df["pp_vacant"]),
            "pp_vacant_plus_2ans": parse_counts(df["pp_vacant_plus_2ans"]),
        }
    ).dropna(subset=["millesime"])
    out["millesime"] = out["millesime"].astype(int)
    return out.set_index("millesime").sort_index()


def parse_territories(raw: pd.DataFrame, *, code_col: str, name_col: str) -> pd.DataFrame:
    """Parse a département/commune file: id columns kept, count columns numeric.

    Count columns are the `<variable>_<millésime>` ones; everything else is
    carried through stripped.
    """
    df = _clean_header(raw)
    for col in (code_col, name_col):
        if col not in df.columns:
            raise LovacError(f"missing column {col}")
    value_cols = {c: m for c in df.columns if (m := _VALUE_COLUMN.match(c))}
    if not value_cols:
        raise LovacError("no LOVAC count columns found")
    out = pd.DataFrame({"code": df[code_col].str.strip(), "name": df[name_col].str.strip()})
    for col in df.columns:
        if col in (code_col, name_col):
            continue
        if col in value_cols:
            match = value_cols[col]
            out[f"{match.group(1)}_{2000 + int(match.group(2))}"] = parse_counts(df[col])
        else:
            out[col] = df[col].str.strip()
    return out


def aggregate_plm(territories: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    """Aggregate PLM arrondissements into their parent commune, summing `columns`.

    Secrecy propagates: a parent whose arrondissements include a masked value
    keeps NA (min_count) rather than a silently understated sum.
    """

    def parent(code: str) -> str:
        return next((city for p, (city, _, _) in PLM_CITIES.items() if code.startswith(p)), code)

    out = territories.copy()
    out["code"] = out["code"].map(parent)
    renames = {city: name for _, (city, name, _) in PLM_CITIES.items()}
    grouped = out.groupby("code", as_index=False).agg(
        name=("name", "first"), **{c: (c, "sum") for c in columns}
    )
    masked = out[columns].isna().groupby(out["code"]).any()
    for col in columns:
        grouped.loc[grouped["code"].map(masked[col]).fillna(False), col] = pd.NA
    grouped["name"] = grouped.apply(lambda r: renames.get(r["code"], r["name"]), axis=1)
    return grouped


def structural_rate(territories: pd.DataFrame, millesime: int = REFERENCE_MILLESIME) -> pd.Series:
    """Structural-vacancy rate (%) of the private stock for one millésime."""
    num, den = f"pp_vacant_plus_2ans_{millesime}", f"ff_pp_total_{millesime}"
    for col in (num, den):
        if col not in territories.columns:
            raise LovacError(f"millésime {millesime} not available ({col} missing)")
    return territories[num] / territories[den] * 100


def build_summary(
    france: pd.DataFrame, departements: pd.DataFrame, communes: pd.DataFrame
) -> dict[str, object]:
    """Assemble the R-02 payload: national series, departmental gradient, secrecy."""
    ref = REFERENCE_MILLESIME
    dep = departements.copy()
    dep["rate_pct"] = structural_rate(dep, ref).round(1)
    # Rounded rates tie (e.g. 7.3/7.3): a stable sort with an explicit code
    # tie-break keeps the ranking identical across platforms — the regression
    # test compares this list element by element.
    dep = dep.sort_values(["rate_pct", "code"], ascending=[False, True], kind="stable")
    national_rate = dep[f"pp_vacant_plus_2ans_{ref}"].sum() / dep[f"ff_pp_total_{ref}"].sum() * 100

    def dep_entry(row: pd.Series) -> dict[str, object]:
        return {
            "dep": row["code"],
            "name": row["name"],
            "rate_pct": float(row["rate_pct"]),
            "structural": int(row[f"pp_vacant_plus_2ans_{ref}"]),
        }

    latest = int(france.index.max())
    com_cols = [f"pp_vacant_plus_2ans_{ref}", f"ff_pp_total_{ref}"]
    cities = aggregate_plm(communes, com_cols)
    visible = cities.dropna(subset=com_cols)
    top_cities = visible.sort_values(
        [f"pp_vacant_plus_2ans_{ref}", "code"], ascending=[False, True], kind="stable"
    ).head(10)
    masked_latest = communes[f"pp_vacant_plus_2ans_{latest}"].isna().sum()

    return {
        "reference_millesime": ref,
        "break_millesimes": list(BREAK_MILLESIMES),
        "national": {
            "structural_by_millesime": {
                str(m): int(v) for m, v in france["pp_vacant_plus_2ans"].dropna().items()
            },
            "total_by_millesime": {str(m): int(v) for m, v in france["pp_vacant"].dropna().items()},
            "structural_rate_ref_pct": round(float(national_rate), 1),
        },
        "departements": {
            "top": [dep_entry(r) for _, r in dep.head(12).iterrows()],
            "bottom": [dep_entry(r) for _, r in dep.tail(5).iterrows()],
        },
        "communes": {
            "n_total": len(communes),
            "n_masked_latest": int(masked_latest),
            "visible_ref": {
                "n": len(visible),
                "structural_share_pct": round(
                    float(
                        visible[f"pp_vacant_plus_2ans_{ref}"].sum()
                        / dep[f"pp_vacant_plus_2ans_{ref}"].sum()
                        * 100
                    ),
                    1,
                ),
            },
            "top_by_volume_ref": [
                {
                    "code": r["code"],
                    "name": r["name"],
                    "structural": int(r[f"pp_vacant_plus_2ans_{ref}"]),
                    "rate_pct": round(
                        float(r[f"pp_vacant_plus_2ans_{ref}"] / r[f"ff_pp_total_{ref}"] * 100), 1
                    ),
                }
                for _, r in top_cities.iterrows()
            ],
        },
    }
