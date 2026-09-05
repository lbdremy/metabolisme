# CLAUDE.md — the `monopoles` study (monopoles/)

Local guidance for the natural-monopoly and positional-rent study. Read
the repo-root `../CLAUDE.md` for the shared doctrine and `INTRO.md` (here)
for the research framing; this file only adds what is specific to
`monopoles`.

## What it is

Second Métabolisme study: *dans quels secteurs le prix rémunère-t-il une
position plutôt qu'une production, à qui va cette rente, de combien est-elle,
et sous quelles formes pourrait-elle revenir à la collectivité ?* It is a
**framing study**: it fixes the definitions (D-01..D-21, eight of them
constructed), the identification grid (Q1 with three answers: substitutable
/ non-duplicable / fixed; four questions; three levels; the classified
object always named), the measurable definition of rent (D-15: surplus
profit on an asset base at historical cost net of subsidies, reference
rate H-06, before tax, with a substitutable control), the normative
position (V-01..V-06, including the destination of the rent V-05), the
inventory as classification hypotheses (H-09..H-20, two controls), and the
template every sector study must follow (`INTRO.md` §9, four
configurations C-05). Sector studies (`autoroutes/`, `eau/`, …) are separate
top-level projects that reference this study's definitions.

Origin: a working note of September 2026, archived verbatim in
`exploration/` with the discrepancies found against already-frozen sources.
Nothing in `exploration/` is citable (method INTRO §2.1). The framing was
reviewed adversarially on 2026-09-04/05 (58 objections, all integrated on
Rémy's decision): `evidence/revue-contradictoire-2026-09-04.md`.

## No Python here (decision 2026-09-04)

The framing article computes nothing, so there is no `pyproject.toml`, no
`src/`, no `check.sh`/`test.sh`. The deterministic check is the site build:
`site/tools/evidence` derives the registries into the evidence graph, fails
on unresolved references, and **recomputes every declared sha256**
(`cd ../site && pnpm content`). Add a `uv` project the day a sector study
computes something; do not add one before.

## Registry fields beyond logement's schemas

The registries follow the schemas of `logement/src/logement/models.py`
with four additions the site contract understands and logement's pydantic
models do not (skip them when validating with logement's models):

- hypotheses: `statement` (qualitative hypothesis, no numeric triple) and
  `limitations`;
- definitions: `constructed_by: C-02` on notions the study builds (the
  graph then shows the choice, not only the anchoring source);
- sources: `redistributable: false` (frozen copy kept for verification,
  not served by the site — the OECD PDF, L-10).

## Binding conventions

- **Statuses are not decoration.** Grid criteria are definitions (D);
  "the rent goes to the users" is a value (V); each inventory row is a
  hypothesis (H) until a sector study confirms it; the identification is a
  classification hypothesis, never a "constat"; the configurations to
  instruct first are a choice (C-05) depending on values, not a grid
  output.
- **`justification` holds only S, O or I**; limits go to `limitations`;
  `confidence: medium` only if a frozen observation carries the statement;
  every qualitative hypothesis says what would refute it; every C and I
  node says what would overturn it.
- **Rent is measured before it is named.** D-15 measures a surplus profit;
  attributing it to a position is the interpretation I-03, which requires a
  substitutable control measured the same way. Every measure is shown at
  both bounds of H-06 and at the sector regulator's own rate.
- **Compare four configurations; defend none in advance** (status quo /
  regulated private / collectivised with risk bearer / fully private), and
  state the destination of the rent (V-05: price at cost or earmarked
  revenue).
- **Housing (decisions 2026-09-04/05):** positional rent, not a natural
  monopoly; open price-maker stock with private ownership kept, founded on
  H-04 and V-01/V-02, four configurations including rent control; the
  `logement/` study is referenced (`logement:R-14`), never duplicated.
- **Frozen files:** Légifrance and OpenStax pages are browser DOM captures
  (L-08); the ARCEP decision is frozen from its JORF publication because
  arcep.fr sits behind a WAF; the OECD PDF is not served.
- **Language:** English for identifiers and commits, French for everything
  the reader of the research sees.
- Update `PREV-STEPS.md` (append per session) and `NEXT-STEPS.md` at
  session close; conventional commits, one per completed deliverable.
