# Skill: gather-example

Research / data-gathering orchestration for the `_template` expert. A skill
describes *how to collect the evidence* a playbook needs — it sequences
deterministic scripts and interprets their output. Determinism lives in the
scripts; the skill orchestrates them.

## When to use

Invoke this skill while diagnosing an `example-issue` (see
`../../playbooks/example-issue.md`) to collect the supporting data the playbook's
"Steps to confirm" require.

## Procedure

1. Run the deterministic collector:

   ```bash
   experts/_template/scripts/collect_example.sh
   ```

2. Parse its `key=value` output. The script always prints the same keys in the
   same order, so the result is stable and comparable across runs.

3. Hand the collected values back to the playbook's confirmation steps.

## Notes

- Keep any non-deterministic judgment here in the skill; keep reproducible data
  collection in the script it calls. That split is what makes an expert
  promotable: the script can be trusted verbatim, the skill is where reasoning
  lives.
