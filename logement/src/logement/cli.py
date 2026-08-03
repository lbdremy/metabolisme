"""Typed CLI (clypi) — the imperative shell's entry point.

`logement <stage>` mirrors the method's canonical commands (INTRO §20):
`validate` gates the evidence registries, `reproduce` replays the stabilized
chain. Each command declares its args here and delegates to a plain `shell.*`
handler; validation lives in the command, logic in the handler.
"""

from __future__ import annotations

from clypi import Command
from typing_extensions import override

from logement.config import project_root


class Validate(Command):
    """Parse + cross-check sources/definitions/hypotheses; verify frozen files."""

    @override
    async def run(self) -> None:
        from logement.shell import validate

        raise SystemExit(validate.run(project_root()))


class Reproduce(Command):
    """Rebuild every published result from the raw data (the executable chain)."""

    @override
    async def run(self) -> None:
        from logement.shell import reproduce

        raise SystemExit(reproduce.run(project_root()))


class Logement(Command):
    """Executable evidence chain: efficacité du parc immobilier français."""

    subcommand: Validate | Reproduce


def main() -> None:
    """Parse argv and dispatch to the selected subcommand."""
    Logement.parse().start()
