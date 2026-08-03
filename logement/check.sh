#!/usr/bin/env bash
# The feedback half of the control loop: four deterministic gates, no LLM.
# Code isn't "done" until this is green. Run from anywhere; operates on logement/.
#   ./check.sh         ruff format --check · ruff check · ty check · skylos
#   ./check.sh --fix   auto-apply ruff format + safe lint fixes, then re-check
set -euo pipefail
cd "$(dirname "$0")"

if [[ "${1:-}" == "--fix" ]]; then
    echo "== ruff format (apply) =="   && uv run ruff format src/
    echo "== ruff check --fix =="       && uv run ruff check --fix src/
fi

fail=0
echo "== ruff format --check ==" && uv run ruff format --check src/    || fail=1
echo "== ruff check =="          && uv run ruff check src/             || fail=1
echo "== ty check =="            && uv run ty check src/               || fail=1
echo "== skylos =="              && uv run skylos --gate --strict src/ || fail=1

if [[ $fail -ne 0 ]]; then
    echo; echo "check.sh: RED — fix the code (or add a documented ignore)." >&2
    exit 1
fi
echo; echo "check.sh: green."
