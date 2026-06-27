"""Load and naively match playbooks.

A playbook is a Markdown file with a YAML frontmatter block fenced by ``---``
lines. The frontmatter declares the symptoms and keywords used for matching; the
body is the human-readable diagnosis + fix.

    ---
    symptoms:
      - example symptom here
    keywords: [example, symptom]
    ---
    ## Diagnosis
    ...

Matching is intentionally dumb (lowercase substring/keyword scoring). It is good
enough to prove the contract end to end and to give a starting `confidence`. An
expert that graduates to a real model-backed `ask()` can use these same files as
context rather than relying on this matcher.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import yaml


@dataclass
class Playbook:
    name: str  # filename stem, e.g. "example-issue"
    symptoms: list[str] = field(default_factory=list)
    keywords: list[str] = field(default_factory=list)
    body: str = ""
    score: float = 0.0  # populated by match(); 0.0 when loaded


def _split_frontmatter(text: str) -> tuple[dict, str]:
    """Split a ``---``-fenced YAML frontmatter block from the Markdown body."""
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) == 3:
            front = yaml.safe_load(parts[1]) or {}
            return front, parts[2].lstrip("\n")
    return {}, text


def load_playbooks(directory: str | Path) -> list[Playbook]:
    """Load every ``*.md`` playbook in ``directory`` (sorted by name)."""
    directory = Path(directory)
    playbooks: list[Playbook] = []
    if not directory.is_dir():
        return playbooks
    for path in sorted(directory.glob("*.md")):
        front, body = _split_frontmatter(path.read_text())
        playbooks.append(
            Playbook(
                name=path.stem,
                symptoms=[str(s) for s in (front.get("symptoms") or [])],
                keywords=[str(k) for k in (front.get("keywords") or [])],
                body=body,
            )
        )
    return playbooks


def _score(playbook: Playbook, question: str) -> float:
    """Fraction of the playbook's signals (symptoms + keywords) present in the question."""
    q = question.lower()
    signals = [s.lower() for s in playbook.symptoms + playbook.keywords]
    if not signals:
        return 0.0
    hits = sum(1 for s in signals if s and s in q)
    return hits / len(signals)


def match(playbooks: list[Playbook], question: str) -> list[Playbook]:
    """Return the playbooks whose signals appear in ``question``, best first.

    Each returned playbook has its ``score`` set. Non-matching playbooks
    (score 0) are excluded.
    """
    scored: list[Playbook] = []
    for pb in playbooks:
        s = _score(pb, question)
        if s > 0:
            pb.score = s
            scored.append(pb)
    scored.sort(key=lambda p: p.score, reverse=True)
    return scored
