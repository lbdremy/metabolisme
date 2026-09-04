# CLAUDE.md — the `monopoles` study (monopoles/)

Local guidance for the natural-monopoly rents study. Read the repo-root
`../CLAUDE.md` for the shared doctrine and `INTRO.md` (here) for the
research framing; this file only adds what is specific to `monopoles`.

## What it is

Second Métabolisme study: *dans quels secteurs le prix rémunère-t-il une
position plutôt qu'une production, à qui va cette rente, de combien est-elle,
et sous quelles formes pourrait-elle revenir à la collectivité ?* It is a
**framing study**: it fixes the definitions (D-01..D-14), the identification
grid (four questions, three levels), the normative position (V-01..V-04),
the sector inventory as hypotheses, and the template every sector study must
follow (`INTRO.md` §9). Sector studies (`autoroutes/`, `eau/`, …) are
separate top-level projects that reference this study's definitions.

Origin: a working note of September 2026, archived verbatim in
`exploration/` with the discrepancies found against already-frozen sources.
Nothing in `exploration/` is citable (method INTRO §2.1).

## No Python here (decision 2026-09-04)

The framing article computes nothing, so there is no `pyproject.toml`, no
`src/`, no `check.sh`/`test.sh`. The four registries follow the exact
schemas of `logement/src/logement/models.py` (SourceRecord,
DefinitionRecord, HypothesisRecord, ClaimRecord) so that a shared validator
can be extracted later without rewriting anything (method INTRO §20). Until
then the deterministic check is the site build: `site/tools/evidence`
derives the registries into the evidence graph and fails on unresolved
references (`cd ../site && pnpm content`).

Add a `uv` project the day a sector study — or this one — computes
something; do not add one before.

## Layout

```
INTRO.md              # research framing (French)
EVIDENCE.md           # human index of the evidence chain (French)
NEXT-STEPS.md         # ordered upcoming work + pickup procedure
PREV-STEPS.md         # session journal (most recent first)
sources/
  sources.yaml        # S-xx registry: every retained source, checksummed
  definitions.yaml    # D-xx registry: verbatim, dated, with caveats
  hypotheses.yaml     # H-xx registry: numeric parameters only (H-06+;
                      #   H-01..H-05 reserved for the framing hypotheses)
data/raw/             # frozen source files (Git LFS, sha256 in sources.yaml)
evidence/             # claims.yaml graph + evidence document (markdown)
articles/             # the public article(s)
exploration/          # exploratory material, never cited as established
```

## Binding conventions

- **Statuses are not decoration.** The grid's criteria are definitions (D);
  "the rent must go to the user" is a value (V); each sector row of the
  inventory is a hypothesis (H) until a sector study confirms it; the
  three-level split is a choice (C). Never let a V read as an O.
- **Rent must be measurable before it is named.** The operational
  definition (price paid minus efficient cost, normal return on capital
  included) and its parameter H-06 are fixed here and reused unchanged by
  every sector study.
- **Compare configurations; defend none in advance.** Every sector study
  instructs status quo / collectivised (variants) / fully private.
- **Housing decision (2026-09-04):** price-maker public stock with private
  ownership kept, three configurations compared (`INTRO.md` §8.1). The
  `logement/` study is referenced, never duplicated.
- **Qualitative hypotheses (decision 2026-09-04).** `sources/hypotheses.yaml`
  holds both numeric parameters (H-06+) and the framing hypotheses
  H-01..H-05 as `statement` records without numeric fields. The site
  contract (`site/packages/evidence`, `study-to-graph`) accepts both; the
  `logement` pydantic `HypothesisRecord` does NOT (it still requires the
  numeric triple) — when validating this study with logement's schemas,
  skip the `statement` records; the shared validator, when extracted, must
  carry both forms.
- **Language:** English for identifiers and commits, French for everything
  the reader of the research sees.
- Update `PREV-STEPS.md` (append per session) and `NEXT-STEPS.md` at
  session close; conventional commits, one per completed deliverable.
