# Authoring playbooks, skills, scripts, and experts

How to add knowledge to the system. Start by copying `experts/_template/`.

## Add a playbook

A playbook is a known issue and its fix:
`experts/<name>/playbooks/<issue>.md`.

```markdown
---
symptoms:
  - short phrase a caller would use
keywords:
  - distinctive
  - token
---
## Diagnosis
What this issue is and how to recognize it.

## Steps to confirm
1. ...

## Fix
The remediation.
```

- `symptoms` and `keywords` feed the matcher in `harness/playbook.py`. Matching
  is lowercase substring scoring; the `confidence` in the Response is the
  fraction of these signals present in the question. Choose phrases a caller
  would actually type.
- The body becomes the `answer` when this playbook is the best match.

## Add a script

A script is a deterministic tool: `experts/<name>/scripts/<tool>.sh` (or any
executable). Keep it reproducible.

```bash
#!/usr/bin/env bash
set -euo pipefail
echo "key=value"   # stable, structured output
```

- Make it executable (`chmod +x`).
- Run it via `harness.scripts.run_script(path, args)` to capture
  stdout/stderr/exit code.
- Determinism lives here, not in model judgment — same input, same output.

## Add a skill

A skill orchestrates scripts and interprets their output:
`experts/<name>/skills/<skill>/SKILL.md`. State when to use it, which scripts it
runs, and how to read the results. Reference it from the playbook that needs it.

## Add a new expert

1. `cp -r experts/_template experts/<your-domain>`
2. Edit `expert.yaml`: `name`, `domain`, `description`, `status`.
3. In `__main__.py`, change the module string to `experts.<your-domain>`.
4. Replace the template playbook/skill/script with real ones (above).
5. Done — the registry discovers it from `expert.yaml`; triage can route to it.

_Verify:_

```bash
python -m experts.<your-domain> ask "<a symptom phrase>"
python -c "from harness.registry import as_table; print(as_table())"
```

See `PROMOTION.md` for taking an expert from `experimental` to `proven` and for
upgrading `ask()` into a model-backed agent.
