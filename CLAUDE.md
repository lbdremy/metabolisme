# CLAUDE.md — Métabolisme

Guidance for Claude when working in this repository.

## What this repo is

**Métabolisme** is a research program: designing institutions and economic
systems from real material conditions, published as **executable evidence
chains**. The method is defined in `INTRO.md` — read it before any research
work; its §21 lists twenty binding rules for agents (record every source, never
silently change a hypothesis, distinguish facts / hypotheses / interpretations /
values / choices, …).

```
INTRO.md      # the method: executable evidence chain (authoritative)
logement/     # first study: efficiency of the French housing stock
              # (see logement/INTRO.md + logement/CLAUDE.md)
.github/workflows/logement-ci.yml   # CI: gates + tests + validate + reproduce
.gitignore    # single root gitignore (git lives at the repo root only)
```

Each study is a **self-contained uv Python project** (like `vttae/`/`casarent/`
in the sibling `learn` repo): `pyproject.toml`, `src/<study>/`, `tests/`,
`check.sh` + `test.sh`, its own `.venv/`. No shared engine yet — extract one
only after several studies show a real common need (INTRO §20).

## Language: follow the register, not the folder

- **English for the technical** — code, identifiers, docstrings, commits,
  architecture discussion. `vacant_dwellings`, never `logements_vacants`.
- **French for the substance** — housing, institutions, sources, definitions,
  articles, evidence documents, anything the reader of the research sees.
- When in doubt, mirror the language of the user's message.

## Architecture doctrine (imported from the `learn` repo)

Established in `/Volumes/Work/github/learn` (`scripts/CLAUDE.md` there is the
reference formulation); every study here follows it:

1. **Deterministic over probabilistic.** Anything a parser/regex/script can do
   must not use an LLM. This is the INTRO's exploratory→stabilized transition:
   stabilized work is code, versioned, testable.
2. **Write code, then run the code** — the work goes into committed scripts,
   not one-off shell commands.
3. **Functional core / imperative shell.** Pure `core/` (parse, validate,
   transform, compute — no I/O, no clock), effects in `shell/` (fetch, files,
   subprocess). The whole evidence chain's calculations are table-testable
   pure functions.
4. **Parse at the boundary (pydantic v2).** `StrictModel` (`extra="forbid"`)
   for data we own (registries, hypotheses, claims), `SubsetModel` for
   third-party payloads (INSEE/SDES files). Never flow a raw dict downstream.
   Brand domain scalars with `NewType` so a rent can't be passed as a rate.
5. **Typed CLI (clypi)** — one `uv run <study> <stage>` command per study;
   args declared in `cli.py`, logic in plain `shell.*` handlers.
6. **Quality gate**: `./check.sh` (ruff format · ruff check · ty · skylos) and
   `./test.sh` (pytest + hypothesis over the pure core). Code is not "done"
   until both are green. Property tests carry the INTRO's invariants (rates in
   [0,1], category sums match totals, filtered ≤ total population). CI
   (`.github/workflows/`) replays gates + tests + `validate` + `reproduce` in
   a fresh environment on every push touching a study (method INTRO §6.8).
7. **Committed code + committed artifacts.** Registries, small raw data,
   processed outputs and reports are committed together; a reader can
   `git clone` and re-run. `uv.lock` committed, `.venv/` ignored.
8. **Unknown keeps, definite rejects.** A record that fails to parse is kept
   and flagged in reports, never silently dropped (INTRO §21 rule 9).
9. **Library docs via the `ctx7` CLI** (`npx ctx7@latest library/docs …`), not
   memory.

## What the method adds on top (study-level artifacts)

Beyond the `learn` architecture, every study maintains the INTRO's evidence
artifacts: `sources/sources.yaml` (checksummed source registry),
`sources/definitions.yaml`, `sources/hypotheses.yaml` (named, ranged
parameters), `evidence/claims.yaml` (the dependency graph),
Jupytext-paired notebooks (`exploration/` free, `verification/` reproducible),
and a Quarto evidence document (`evidence/*.qmd`) distinct from the article.
