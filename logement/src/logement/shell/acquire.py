"""`logement acquire-dpe` — freeze the ADEME DPE commune × label counts (S-16).

One-off acquisition, NOT part of `reproduce`: queries the data-fair
aggregation API of the ADEME dataset « DPE Logements existants (depuis
juillet 2021) », one request per département × étiquette (A..G), and
writes the long-format commune counts to data/raw/. Aggregating
server-side is LOSSLESS for our use (the two-column row extract carries
exactly the same information as the commune × étiquette counts, up to row
order) and ~400× lighter than paginating the 15.3M rows — which the API
throttles to a trickle for anonymous clients (HTTP 429). Each département
has < 1 000 communes, so the per-request agg_size cap of 1 000 is never
binding. The frozen file is registered and sha256-checksummed in
sources/sources.yaml; the API is live (new DPE arrive daily), so a re-run
yields a different file — reproducibility rests on the frozen copy.
"""

from __future__ import annotations

import csv
import json
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

DATASET_ID = "meg-83tjwtg8dyz4vv7h1dqe"
API_BASE = f"https://data.ademe.fr/data-fair/api/v1/datasets/{DATASET_ID}/values_agg"
DPE_LABELS = ("A", "B", "C", "D", "E", "F", "G")
DPE_OUTPUT = Path("data") / "raw" / "ademe-dpe-existants-communes-etiquettes.csv"


def _get_json(url: str, retries: int = 8) -> dict[str, object]:
    """Fetch one API response, honouring 429 Retry-After with backoff."""
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(url, timeout=90) as resp:
                return json.load(resp)
        except urllib.error.HTTPError as exc:
            if exc.code != 429 or attempt == retries - 1:
                raise
            retry_after = exc.headers.get("Retry-After")
            time.sleep(float(retry_after) if retry_after else 2**attempt)
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError):
            if attempt == retries - 1:
                raise
            time.sleep(2**attempt)
    raise RuntimeError("unreachable")


def _values_agg(field: str, qs: str | None = None) -> dict[str, object]:
    params = {"field": field, "agg_size": "1000", "size": "0"}
    if qs:
        params["qs"] = qs
    return _get_json(f"{API_BASE}?{urllib.parse.urlencode(params)}")


def _agg_pairs(payload: dict[str, object]) -> list[tuple[str, int]]:
    aggs = payload.get("aggs")
    pairs: list[tuple[str, int]] = []
    if not isinstance(aggs, list):
        return pairs
    for agg in aggs:
        if not isinstance(agg, dict):
            continue
        value = agg.get("value")
        if value is None:
            continue
        pairs.append((str(value), int(float(str(agg.get("total") or 0)))))
    return pairs


def run(root: Path) -> int:
    """Write the frozen commune × étiquette counts, one API call per dept × label."""
    out = root / DPE_OUTPUT
    out.parent.mkdir(parents=True, exist_ok=True)
    departements = _agg_pairs(_values_agg("code_departement_ban"))
    dataset_total = int(str(_values_agg("etiquette_dpe").get("total") or 0))
    print(f"acquire-dpe: {len(departements)} departements, {dataset_total} DPE in dataset")

    written_dpe = 0
    with out.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh, delimiter=";")
        writer.writerow(["code_insee_ban", "etiquette_dpe", "n_dpe"])
        for index, (dept, dept_total) in enumerate(departements, start=1):
            for label in DPE_LABELS:
                pairs = _agg_pairs(
                    _values_agg(
                        "code_insee_ban",
                        qs=f'etiquette_dpe:"{label}" AND code_departement_ban:"{dept}"',
                    )
                )
                for commune, count in pairs:
                    writer.writerow([commune, label, count])
                    written_dpe += count
            if index % 10 == 0:
                print(
                    f"acquire-dpe: {index}/{len(departements)} depts "
                    f"({written_dpe} DPE written, dept {dept}: {dept_total})",
                    flush=True,
                )
    uncovered = dataset_total - written_dpe
    print(
        f"acquire-dpe: wrote {DPE_OUTPUT} — {written_dpe} DPE over "
        f"{len(departements)} departements; {uncovered} DPE not covered "
        "(missing BAN department/commune code or unknown label) — record this "
        "figure in the S-16 notes."
    )
    return 0
