"""The template expert's brain.

``ask()`` is the single function the callable CLI and (eventually) the
model-backed agent both go through. Here it is a **deterministic stub**: it loads
this expert's playbooks, keyword-matches the question, and returns a structured
Response. No model call — which is exactly what lets the contract be verified in a
clean checkout without ``claude-agent-sdk`` installed.

To promote this expert (see DEV.md), replace the body of ``ask()`` with a real
claude-agent-sdk agent that reads the same playbooks/skills/scripts as context.
The signature and the returned Response contract stay identical.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from harness.contract import Response, STATUS_OK, STATUS_NEED_INFO
from harness.playbook import load_playbooks, match

EXPERT_NAME = "_template"
PLAYBOOKS_DIR = Path(__file__).resolve().parent / "playbooks"


def ask(question: str, context: dict[str, Any] | None = None) -> Response:
    """Answer ``question`` using this expert's playbooks. Returns a Response."""
    context = context or {}
    playbooks = load_playbooks(PLAYBOOKS_DIR)
    matches = match(playbooks, question)

    if not matches:
        return Response(
            expert=EXPERT_NAME,
            status=STATUS_NEED_INFO,
            answer=(
                "No playbook matched this question. Provide more detail "
                "(symptoms, error text, environment) or add a new playbook to "
                f"experts/{EXPERT_NAME}/playbooks/."
            ),
            evidence=[f"checked {len(playbooks)} playbook(s)"],
            confidence=0.0,
        )

    best = matches[0]
    return Response(
        expert=EXPERT_NAME,
        status=STATUS_OK,
        answer=best.body.strip(),
        evidence=[f"matched playbook '{best.name}' (score {best.score:.2f})"],
        playbooks_used=[m.name for m in matches],
        confidence=round(best.score, 2),
    )
