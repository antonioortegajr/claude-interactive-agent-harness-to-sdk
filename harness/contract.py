"""The CLI request/response contract — the spine of the harness.

Defined once here and reused by every expert through :mod:`harness.cli`. The
canonical, human-readable spec lives in ``docs/CONTRACT.md``; this module is the
executable source of truth.

Stdlib only — no third-party imports — so the contract can be parsed and emitted
in any environment without installing the SDK.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field, asdict
from typing import Any

# Allowed values for Response.status.
STATUS_OK = "ok"
STATUS_NEED_INFO = "need_info"
STATUS_ERROR = "error"
VALID_STATUSES = (STATUS_OK, STATUS_NEED_INFO, STATUS_ERROR)


@dataclass
class Request:
    """An incoming question for an expert.

    ``context`` is an arbitrary JSON-serializable mapping the caller (triage
    agent or human) may attach — e.g. logs, environment, prior findings.
    """

    question: str
    context: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_args(cls, question: str, context_json: str | None) -> "Request":
        """Build a Request from CLI arguments. ``context_json`` is raw JSON or None."""
        context: dict[str, Any] = {}
        if context_json:
            parsed = json.loads(context_json)
            if not isinstance(parsed, dict):
                raise ValueError("--context must be a JSON object")
            context = parsed
        return cls(question=question, context=context)


@dataclass
class Response:
    """An expert's structured answer.

    This is what gets serialized to stdout for the triage agent to parse.
    """

    expert: str
    status: str = STATUS_OK
    answer: str = ""
    evidence: list[str] = field(default_factory=list)
    playbooks_used: list[str] = field(default_factory=list)
    confidence: float = 0.0

    def __post_init__(self) -> None:
        if self.status not in VALID_STATUSES:
            raise ValueError(
                f"invalid status {self.status!r}; expected one of {VALID_STATUSES}"
            )

    @classmethod
    def error(cls, expert: str, message: str) -> "Response":
        """Convenience constructor for an error Response."""
        return cls(expert=expert, status=STATUS_ERROR, answer=message, confidence=0.0)

    def to_json(self) -> str:
        """Serialize to a single-line, deterministic JSON object."""
        return json.dumps(asdict(self), sort_keys=True)

    @classmethod
    def from_json(cls, raw: str) -> "Response":
        """Parse a Response from a JSON string (inverse of :meth:`to_json`)."""
        data = json.loads(raw)
        return cls(**data)

    @property
    def exit_code(self) -> int:
        """Process exit code: 0 for ok/need_info, 1 for error."""
        return 1 if self.status == STATUS_ERROR else 0
