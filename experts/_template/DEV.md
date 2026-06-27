# Developing this expert (interactive mode → callable mode)

An expert has two faces from one codebase. This file is about the **interactive
dev mode** you use to *grow* the expert, and how that work graduates into the
**callable mode** the triage agent invokes.

## Interactive dev mode

Open this directory (`experts/_template/`) as a Claude Code project, with a human
in the loop, to author and test the three kinds of knowledge:

- **playbooks/** — a known issue and its fix. Frontmatter declares `symptoms`
  and `keywords` (used by the matcher); the body is the diagnosis + remediation.
- **skills/** — research/data-gathering orchestration (`SKILL.md`) that sequences
  scripts and interprets their output.
- **scripts/** — deterministic tools. Anything that must be reproducible lives
  here, not in model judgment.

`python -m experts._template dev` prints this guidance.

Callable mode reads the **same** bundle, so anything you prove here is exactly
what runs in production — no divergence.

## Callable mode (the contract)

```bash
python -m experts._template ask "example symptom here"
```

Emits one JSON object on stdout (see `../../docs/CONTRACT.md`). Today `ask()` in
`expert.py` is a deterministic stub: load playbooks → keyword-match → structured
Response. This proves the contract without any model call.

## Promoting `ask()` to a real agent

When the stub's keyword matching is no longer enough, upgrade `ask()` into a real
model-backed agent (requires the `sdk` extra: `pip install -e ".[sdk]"`):

1. Keep the signature `ask(question, context) -> Response` and the returned
   contract identical — callers must not notice the change.
2. Inside `ask()`, build a `claude-agent-sdk` agent whose context is **this
   expert's own bundle**: the loaded `playbooks/`, the `skills/*/SKILL.md`, and
   the ability to run `scripts/` via `harness.scripts.run_script`.
3. Map the agent's conclusion back onto a `Response` (`answer`, `evidence`,
   `playbooks_used`, `confidence`, `status`).
4. Re-run the verification in the repo `README.md` / `docs/PROMOTION.md`.

The full interactive→autonomous checklist lives in `../../docs/PROMOTION.md`.
