"""Discover experts and build the routing table the triage agent reads.

Each expert ships an ``expert.yaml`` describing itself. The registry scans
``experts/*/expert.yaml`` and returns one record per expert. The triage agent
calls :func:`load` (or reads :func:`as_table`) to know which experts exist and
what each one handles — it holds no hard-coded routing table of its own.
"""

from __future__ import annotations

from pathlib import Path

import yaml


def _repo_root() -> Path:
    # harness/registry.py -> repo root is the parent of the harness package.
    return Path(__file__).resolve().parent.parent


def load(experts_dir: str | Path = "experts") -> list[dict]:
    """Return one record per expert found under ``experts_dir``.

    Each record: ``name``, ``domain``, ``description``, ``status``, ``version``,
    and ``module`` (the importable dotted path, e.g. ``experts._template``).
    Directories without an ``expert.yaml`` are skipped.
    """
    base = Path(experts_dir)
    if not base.is_absolute():
        base = _repo_root() / base

    records: list[dict] = []
    if not base.is_dir():
        return records

    for manifest in sorted(base.glob("*/expert.yaml")):
        data = yaml.safe_load(manifest.read_text()) or {}
        dir_name = manifest.parent.name
        records.append(
            {
                "name": data.get("name", dir_name),
                "domain": data.get("domain", ""),
                "description": data.get("description", ""),
                "status": data.get("status", "experimental"),
                "version": data.get("version", ""),
                "module": f"{base.name}.{dir_name}",
            }
        )
    return records


def as_table(experts_dir: str | Path = "experts") -> str:
    """Human-readable routing table for the triage agent to read."""
    records = load(experts_dir)
    if not records:
        return "(no experts registered)"
    lines = ["name\tstatus\tdomain\tdescription"]
    for r in records:
        lines.append(
            f"{r['name']}\t{r['status']}\t{r['domain']}\t{r['description']}"
        )
    return "\n".join(lines)
