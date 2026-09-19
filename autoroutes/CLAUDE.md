# CLAUDE.md — the `autoroutes` study (autoroutes/)

Local guidance for the first sector study of the natural-monopoly and
positional-rent programme. Read the repo-root `../CLAUDE.md` for the shared
doctrine, `../monopoles/INTRO.md` (the framing: definitions D-01..D-21, the
grid, the measurable rent D-15, the sector template §9) and `INTRO.md`
(here) for the sector framing; this file only adds what is specific to
`autoroutes`.

## What it is

Sector study n° 1 of `monopoles/`: *sur les autoroutes concédées, le péage
rémunère-t-il une position, à qui va ce surprofit, de combien est-il, et
sous quelles formes pourrait-il revenir à l'usager à l'échéance des
contrats (2031-2036) ?* It follows the framing's template question by
question and produces the **first measure** of the programme: D-15 applied
to the 2023 accounts of the historical concessions, next to the
regulator's own measure (a TRI), with the gap between the two interpreted
(I-02). Same architecture as `logement/` (uv project, functional core /
imperative shell, pydantic at the boundary, `check.sh` + `test.sh`, CI).

Session 1 (2026-09-18) was run in autonomy; every methodological decision
is in `evidence/decisions-2026-09-18.md` (DEC-01..07). Nothing has been
reviewed by Rémy yet.

## The framing is a SOURCE, not a shared graph (DEC-01)

Cross-study ids do not resolve in the site's graph (`monopoles:D-15` is
prose). The framing's registries are frozen at tag `monopoles-cadrage-v1.0`
as S-01 (`data/raw/monopoles-cadrage-v1.0-*.yaml`); the notions this study
reuses are LOCAL definitions/hypotheses that cite S-01 and carry the origin
id in their term (D-01 = monopoles:D-15, D-02 = monopoles:D-21, H-01 =
monopoles:H-06, H-10 = monopoles:H-17, V-01 = monopoles:V-01/V-05). Do not
re-import the framing's text elsewhere; if the framing changes, bump the
tag, re-freeze S-01 and revisit D-01/D-02/H-01.

## Data: hand-transcribed accounts, checked before use (T-01, DEC-03)

The sources are PDFs (group accounts, ART syntheses, ASFA). Their figures
live in `data/transcribed/comptes-2023.csv`, one row per (entity, year,
item) with `source` (S-xx) and `page` of the PDF. Rules:

- every new figure gets a row with its page; never type a number into
  code or into a claim without a row (or an O-xx quoting the page);
- `TranscribedRow` (pydantic, strict) parses the CSV; `group_accounts`
  refuses a partial transcription; `balance_sheet_closes` must hold for
  every group (gross − amortisation − net subsidies + WIP ≈ published net,
  1 M€) — the build stage fails otherwise;
- the four D-15 inputs are assembled in `core/accounts.py` under named
  choices (`base="net"|"gross"`, `dep="accounting"|"technical"`, H-06,
  H-08); the measure itself is `core/rent.py`. Both are pure and
  property-tested; `shell/build.py` writes `data/processed/rente-d15.json`
  and `tests/test_reproduce.py` pins it.

## Binding conventions

- **Rates are named, never bare.** Every measure is published at the two
  bounds of H-01 (4,0 / 8,8), the centre (5,0), the ART's rate (H-02, 7,0),
  the State's negotiated rate (H-03, 5,9) and the market rate (H-04, 2,28);
  the JSON keys carry the names (`surplus_reference_high`, …).
- **Two bases, two depreciations, none chosen alone** (C-04): net
  accounting base is the central variant, gross historical cost the widest
  D-15 admits; the ART's replacement-cost base is NOT a D-15 base — it is
  rendered by M-03 and the gap is I-02.
- **Sector-specific levies are a destination** (C-03): TAT, redevance
  domaniale, AFITF contribution, TEITLD are the State's share of the
  surplus, not a cost; CET stays a cost; IS is a destination (D-15).
- **Sanef-SAPN is extrapolated** (H-07, H-09, L-04): its 2023 accounts
  could not be frozen (groupe.sanef.com returns 403 to curl, WebFetch,
  browser-driven fetch and Playwright download; three methods tried). Fix
  by a manual download, then add rows and drop H-09.
- **The control is VINCI Energies / VINCI Construction** (C-05), same
  group, same year, same form; VINCI Autoroutes at acquisition-price
  capital is the counter-example of base, not a measure.
- **Statuses are not decoration**: P-01 is conditional on V-01 and says
  so; R-04 compares four configurations and retains none; the Senate
  rapporteur's contrary conclusion (régie « inadaptée ») is reported in
  R-04/O-24, not dropped.
- **Language**: English for identifiers, code and commits; French for
  everything the reader of the research sees.
- Update `PREV-STEPS.md` (append per session) and `NEXT-STEPS.md` at
  session close; conventional commits, one per completed deliverable.

## Running

```bash
uv sync
uv run autoroutes validate     # registries + sha256 of data/raw/
uv run autoroutes reproduce    # rebuild data/processed/rente-d15.json
./check.sh                     # ruff format · ruff check · ty · skylos
./test.sh                      # pytest + hypothesis + regression
cd ../site && pnpm content     # derive the post (graph, files, checksums)
```
