"""Shared CLI scaffold that every expert reuses.

An expert's ``__main__.py`` is just::

    from harness.cli import main
    raise SystemExit(main("experts._template"))

This gives the expert the standard ``ask`` and ``dev`` subcommands and guarantees
the contract is enforced identically across all experts: stdout carries exactly
one JSON object, diagnostics go to stderr, and the exit code follows the status.
"""

from __future__ import annotations

import argparse
import importlib
import sys

from harness.contract import Request, Response


def _run_ask(module_name: str, expert_name: str, args: argparse.Namespace) -> int:
    try:
        request = Request.from_args(args.question, args.context)
        module = importlib.import_module(f"{module_name}.expert")
        response: Response = module.ask(request.question, request.context)
    except Exception as exc:  # noqa: BLE001 — any failure becomes a contract error
        response = Response.error(expert_name, f"{type(exc).__name__}: {exc}")
        print(f"[{expert_name}] error: {exc}", file=sys.stderr)
        print(response.to_json())
        return response.exit_code

    # stdout stays pure JSON for the triage agent to parse.
    print(response.to_json())
    return response.exit_code


def _run_dev(module_name: str, expert_name: str) -> int:
    print(
        f"Interactive dev mode for '{expert_name}'.\n"
        f"Open this expert's directory ({module_name.replace('.', '/')}/) as a "
        f"Claude Code project and follow its DEV.md to grow playbooks, skills, "
        f"and scripts with a human in the loop. The callable CLI ('ask') reads "
        f"the same bundle, so there is no divergence between the two modes.",
        file=sys.stderr,
    )
    return 0


def main(module_name: str) -> int:
    """Entry point for an expert package. ``module_name`` e.g. ``experts._template``."""
    expert_name = module_name.rsplit(".", 1)[-1]

    parser = argparse.ArgumentParser(prog=f"python -m {module_name}")
    sub = parser.add_subparsers(dest="command", required=True)

    ask = sub.add_parser("ask", help="answer a question (emits JSON on stdout)")
    ask.add_argument("question", help="the issue/question to triage")
    ask.add_argument(
        "--context",
        default=None,
        help="optional JSON object of extra context",
    )

    sub.add_parser("dev", help="how to run interactive dev mode for this expert")

    args = parser.parse_args()

    if args.command == "ask":
        return _run_ask(module_name, expert_name, args)
    if args.command == "dev":
        return _run_dev(module_name, expert_name)
    parser.error(f"unknown command {args.command!r}")
    return 2
