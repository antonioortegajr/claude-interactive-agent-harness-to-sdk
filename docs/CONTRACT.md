# Expert CLI Contract

The contract every expert honors. It is defined once, executably, in
`harness/contract.py` and enforced for all experts by `harness/cli.py`. This
document is the human-readable mirror.

## Invoke

```bash
python -m experts.<name> ask "<question>" [--context '<json>']
```

- `<question>` — the issue/question to triage (positional, quoted).
- `--context` — optional JSON **object** of extra context (logs, environment,
  prior findings). Invalid JSON or a non-object is an error.

There is also `python -m experts.<name> dev`, which prints guidance for the
expert's interactive dev mode (see the expert's `DEV.md`).

## Output

Exactly **one JSON object on stdout** — nothing else. Diagnostics go to stderr,
so the triage agent can parse stdout verbatim.

```json
{
  "expert": "string",
  "status": "ok | need_info | error",
  "answer": "string",
  "evidence": ["..."],
  "playbooks_used": ["example-issue"],
  "confidence": 0.0
}
```

| field            | meaning                                                        |
| ---------------- | -------------------------------------------------------------- |
| `expert`         | the expert that produced this answer                           |
| `status`         | `ok`, `need_info`, or `error`                                  |
| `answer`         | the response text (a fix for `ok`; what's needed for `need_info`; the failure for `error`) |
| `evidence`       | supporting facts / what was checked                            |
| `playbooks_used` | playbooks that matched, best first                             |
| `confidence`     | 0.0–1.0 match confidence                                       |

## Status semantics

- **`ok`** — the expert has an answer. `answer` carries it; `playbooks_used` and
  `confidence` justify it.
- **`need_info`** — the expert cannot answer yet and needs more input. The caller
  should gather it and re-call with `--context`.
- **`error`** — the expert failed (bad input, exception). `answer` describes the
  failure.

## Exit codes

- `0` for `ok` and `need_info`.
- non-zero for `error`.

The triage agent treats a non-zero exit, or any stdout that is not valid JSON, as
a failure.

## Why CLI only

Transport is deliberately CLI-only: an expert is a stateless subprocess, question
in → JSON out. MCP/HTTP are deferred — they only pay off for warm, stateful,
multi-turn sessions, which the triage model does not need. The contract is shaped
so a thin MCP/HTTP wrapper can be added later without changing `ask()`.
