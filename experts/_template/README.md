# `_template` expert

The generic example expert — a **working skeleton** you copy to start a new
domain. It is not a proven domain; its job is to demonstrate the structure and to
prove the CLI contract end to end.

## What it is

An expert is a unit of knowledge and the unit of promotion. It owns:

- `playbooks/` — known issues → fixes
- `skills/` — research/data-gathering orchestration
- `scripts/` — deterministic tools
- `expert.yaml` — the manifest the triage registry reads
- `expert.py` — `ask(question, context) -> Response`, wrapped as a CLI

## How to call it

```bash
# Matches the template playbook -> status "ok"
python -m experts._template ask "example symptom here"

# No match -> status "need_info"
python -m experts._template ask "totally unrelated text"

# Optional structured context
python -m experts._template ask "example symptom" --context '{"env":"staging"}'
```

Output is a single JSON object on stdout (contract in `../../docs/CONTRACT.md`).

## Start a new expert from this template

1. Copy the directory: `cp -r experts/_template experts/<your-domain>`
2. Edit `expert.yaml` (`name`, `domain`, `description`, `status`).
3. In `__main__.py` change the module string to `experts.<your-domain>`.
4. Write real playbooks/skills/scripts (see `DEV.md` and `../../docs/AUTHORING.md`).
5. The triage registry picks it up automatically from `expert.yaml`.
