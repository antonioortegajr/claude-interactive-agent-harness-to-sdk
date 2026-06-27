"""Run an expert's scripts deterministically.

Scripts are the determinism boundary of an expert: anything that must produce a
stable, reproducible result lives in a script rather than in model judgment. This
module just shells out and captures the result — no shell interpolation, text
mode, explicit args.
"""

from __future__ import annotations

import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence


@dataclass
class ScriptResult:
    stdout: str
    stderr: str
    exit_code: int

    @property
    def ok(self) -> bool:
        return self.exit_code == 0


def run_script(
    path: str | Path,
    args: Sequence[str] = (),
    timeout: float | None = 60.0,
) -> ScriptResult:
    """Execute ``path`` with ``args`` and capture stdout/stderr/exit code.

    ``shell=False`` (no shell interpolation). The script must be executable or a
    recognized interpreter target.
    """
    completed = subprocess.run(
        [str(path), *args],
        capture_output=True,
        text=True,
        timeout=timeout,
        check=False,
    )
    return ScriptResult(
        stdout=completed.stdout,
        stderr=completed.stderr,
        exit_code=completed.returncode,
    )
