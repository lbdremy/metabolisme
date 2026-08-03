# CLAUDE.md — the `logement` study (logement/)

Local guidance for the housing-stock efficiency study. Same architecture,
toolchain and quality gate as the projects in the `learn` repo — read the
repo-root `../CLAUDE.md` for the shared doctrine and `INTRO.md` (here) for the
research framing; this file only adds what is specific to `logement`.

`logement/` is a self-contained Python project (`pyproject.toml` here, package
in `src/logement/`, env in `logement/.venv/` via `uv`; git lives at the repo
root only). Code is not "done" until `./check.sh` (ruff format · ruff check ·
ty · skylos) and `./test.sh` (pytest + hypothesis over the pure core) are both
green.

## The build loop is a control loop

Same mechanism as the `learn` engine — encode intent up front, then verify
deterministically:

- **Feed-forward — encode the intent so the machine builds the right thing.**
  The repo-root `../CLAUDE.md` + this file (working principles), `INTRO.md`
  (the research framing and its normative axiom), and the three registries in
  `sources/` (what counts as a source, a definition, a hypothesis) make the
  implicit explicit, so work is on-doctrine by construction.
- **Feedback — deterministic verification closes the loop.** No-LLM signals:
  `./check.sh` (static gates), `./test.sh` (behaviour tests over the pure
  core), `uv run logement validate` (registry integrity + checksums) and
  `uv run logement reproduce` (replay of every stabilized stage). CI
  (`../.github/workflows/logement-ci.yml`) runs all four in a fresh
  environment on every push touching `logement/`. A red signal: fix the work,
  or add a *documented* ignore — never ship past it.

The LLM is reserved for the judgement the loop can't encode (exploration,
interpretation, critique — method INTRO §13); everything stabilized is code.

## What it is

First Métabolisme study: *dans quelle mesure le parc immobilier français
permet-il de loger correctement la population ?* — an executable evidence
chain (sources → definitions → observations → transformations → results),
leading to an institutional proposal. `INTRO.md` is the framing document:
question, hypotheses H-01…H-05, dimensions, deliverables.

**Normative axiom (binding, INTRO §3):** an occupied primary residence is
never an inefficiency. Statistical under-occupation must never be counted as
mobilisable capacity, used as a waste metric, or feed any indicator of
inefficiency. The legitimate field of analysis is capacity NOT devoted to a
primary residence (durable vacancy, dereliction, legal blockage, degradation,
bad production).

## Layout

```
INTRO.md              # research framing (French)
EVIDENCE.md           # human index of the evidence chain (French)
sources/
  sources.yaml        # S-xx registry: every retained source, checksummed
  definitions.yaml    # D-xx registry: statistical/legal definitions, caveats
  hypotheses.yaml     # H-xx registry: named parameters with plausible ranges
data/raw/             # frozen source files (small ones committed as-is)
src/logement/
  models.py           # StrictModel/SubsetModel bases + typed registry records
  config.py           # project-root resolution
  cli.py              # typed CLI (clypi): validate · reproduce
  core/               # pure: registry parsing/cross-checks, later transforms
  shell/              # effects: file I/O, checksums, later acquisition
tests/                # pytest + hypothesis over the pure core
notebooks/
  exploration/        # free lab notebooks (never published from)
  verification/       # top-to-bottom reproducible, import from src/
evidence/             # claims.yaml graph + Quarto evidence documents (.qmd)
articles/             # the public article(s), pointing at the evidence doc
```

Subfolders of `src/logement/` stay flat until real code needs the INTRO's
fuller split (acquisition/ transformations/ indicators/ …) — minimal first
(method INTRO §20).

## Running

```bash
uv sync                        # install into .venv/ (uv.lock is committed)
uv run logement validate       # parse + cross-check the three registries,
                               #   verify local_file existence and sha256
uv run logement reproduce      # re-run every pipeline stage (none defined yet:
                               #   says so and exits 0 — never fakes work)
./check.sh                     # static gates   (--fix to auto-format first)
./test.sh                      # behaviour tests (--cov for coverage)
```

Correspondence with the method INTRO's canonical commands: `uv run validate` ≙
`uv run logement validate`, `uv run reproduce` ≙ `uv run logement reproduce`,
`uv run test` ≙ `./test.sh`.

## logement-specific principles

- **Registries are the trust boundary of the research.** Any figure used in a
  calculation must trace to an `S-xx` entry (with `retrieved_at`, scope,
  licence, checksum) — an LLM answer or a remembered number is never a source
  (method INTRO §13/§21). Definitions carry their own `D-xx` id and caveats;
  every model parameter is an `H-xx` with a central value AND a plausible
  range. `logement validate` gates all three files.
- **Epistemic statuses are ids, not prose**: S/D/O/T/M/H/R/I/V/C/P/L. New
  artifacts (claims, notebook outputs, evidence docs) reference these ids so
  the dependency graph in `evidence/claims.yaml` stays machine-readable.
- **French data quirks live at the boundary.** INSEE/SDES files come with
  exotic encodings, COG geo codes that change yearly, and definitions that
  drift between millésimes — normalize in `shell`/parsers, keep `core` pure
  and unit-consistent (dwelling counts as `int`, rates as branded ratios).
- **Notebooks**: `exploration/` is a lab (anything goes, never published);
  `verification/` must run top-to-bottom, import from `src/logement/`, and
  display the intermediate values a reader needs. **Jupytext py:percent `.py`
  files are the primary, committed representation** (`# %%` cells — diffable,
  ruff-lintable, runnable as scripts); `.ipynb` files stay local and
  git-ignored.
- **Evidence docs are Quarto** (`evidence/*.qmd`), rendered from the
  stabilized code — the article in `articles/` cites result ids and points to
  a tagged version, it never carries untraceable numbers.

## Settled decisions (2026-08-03)

- **Vacancy split (frictional vs durable):** adopt the administrative
  convention — vacance structurelle = vacant > 2 years (LOVAC / Zéro Logement
  Vacant) — as the central definition, to be sourced as D-10 when LOVAC is
  acquired, AND parameterize the threshold as a named hypothesis (plausible
  range 1–3 years) so every result shows its sensitivity to it.
- **Acquisition order:** national series first (S-01..S-03, first notebook on
  dwellings vs households), then LOVAC for the territorial dive.
- **Raw data policy: Git LFS for everything** under `logement/data/raw/`
  (root `.gitattributes`), whatever the size. The LFS object id is the
  file's sha256 — the same checksum recorded in `sources.yaml`.
- **Notebooks: Jupytext py:percent** as the committed representation.

## Roadmap files (keep them current)

- **`NEXT-STEPS.md`** — the ordered upcoming work, the 5-minute pickup
  procedure, and the known traps. Update it at the end of any significant
  session.
- **`PREV-STEPS.md`** — the session journal (most recent first): what was
  done, decisions taken, what the results say. Append a session entry when
  closing one; don't rewrite history.
