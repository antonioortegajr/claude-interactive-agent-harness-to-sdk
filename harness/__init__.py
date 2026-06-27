"""Shared core for the triage harness.

Reused by every expert. Depends only on the standard library plus PyYAML; the
``claude-agent-sdk`` package is an optional extra needed only when an expert's
``ask()`` is upgraded from the deterministic stub into a real model-backed agent.
"""
