# Promotion: interactive → autonomous

How a fix graduates from something a human worked out by hand into something the
triage agent can call autonomously. Each step maps to a concrete file or command
in this repo.

## Checklist

1. **Capture the pattern as a playbook.**
   Add `experts/<name>/playbooks/<issue>.md` with YAML frontmatter (`symptoms`,
   `keywords`) and a body (diagnosis + fix). See `AUTHORING.md`.
   _Verify:_ `python -m experts.<name> ask "<a symptom phrase>"` returns
   `status: ok` with the new playbook in `playbooks_used`.

2. **Extract data-gathering into a script.**
   Move any reproducible collection into `experts/<name>/scripts/<tool>.sh`
   (deterministic, structured stdout, `set -euo pipefail`).
   _Verify:_ run it twice → identical output.

3. **Orchestrate the script from a skill.**
   Add `experts/<name>/skills/<skill>/SKILL.md` that invokes the script and
   interprets its output; reference it from the playbook's confirm steps.
   _Verify:_ the `SKILL.md` names the script path and the playbook references the
   skill.

4. **Prove it in interactive dev mode.**
   Open `experts/<name>/` as a Claude Code project (`DEV.md`) and exercise the
   playbook/skill/script with a human in the loop until trusted.

5. **Wire it into callable mode.**
   The stub `ask()` already reads playbooks, so a new playbook is callable
   immediately. When keyword matching is no longer enough, upgrade `ask()` to a
   real `claude-agent-sdk` agent that reads the same bundle (requires the `sdk`
   extra). Keep the `ask(question, context) -> Response` signature and the
   Response contract unchanged.
   _Verify:_ the CLI still emits a valid contract Response (`docs/CONTRACT.md`).

6. **Register with triage.**
   Ensure `experts/<name>/expert.yaml` has an accurate `name`, `domain`,
   `description`, and `status`. The registry discovers it automatically.
   _Verify:_ `python -c "from harness.registry import as_table; print(as_table())"`
   lists the expert; a triage session routes a matching issue to it.

7. **Promote status.**
   Bump `status` in `expert.yaml` from `experimental` → `proven` once the expert
   is trusted in production. Routing tie-breakers favor `proven`.

## The gap test

There must be **no gap** between "I added a playbook" and "triage can call it."
Walk steps 1 → 6 against any expert: every transition is a real file or command
above. If a step has no concrete artifact, the promotion is incomplete.
