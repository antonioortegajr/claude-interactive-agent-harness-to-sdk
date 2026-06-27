# Routing rules

How to classify an incoming issue and map it to an expert. The triage agent
reads this together with the live registry table.

## Procedure

1. Get the candidate experts from the registry (`harness.registry.as_table`).
   Each has a `domain` and a one-line `description`.

2. Extract the salient signals from the issue: the core symptom, any error text,
   the component/area involved, the environment.

3. Match signals to the expert whose `domain` + `description` best covers them.
   Prefer the most specific match.

4. Tie-breakers, in order:
   - An expert whose `description` names the exact symptom beats a general one.
   - A `status: proven` expert beats an `experimental` one for the same domain.
   - If still tied, pick one and note that another may also apply.

5. **No match?** Do not force one. Tell the user no registered expert covers the
   issue and ask for more detail. A persistent gap means a new playbook or a new
   expert should be authored (see `../docs/AUTHORING.md`).

## Notes

- Routing is classification only. Never let routing leak into diagnosis — the
  chosen expert does the diagnosing.
- The registry is the source of truth. If an expert was just added, it appears
  here automatically via its `expert.yaml`; there is nothing to update in this
  file.
