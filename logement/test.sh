#!/usr/bin/env bash
# Behaviour tests over the pure core (logement.core).
# Kept separate from ./check.sh: a red test and a red linter mean different things.
#   ./test.sh          run the suite
#   ./test.sh --cov    run with a coverage report for the `logement` package
set -euo pipefail
cd "$(dirname "$0")"

if [[ "${1:-}" == "--cov" ]]; then
    exec uv run pytest --cov=logement --cov-report=term-missing
fi
exec uv run pytest
