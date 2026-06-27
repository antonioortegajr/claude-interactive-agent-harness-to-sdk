# claude-interactive-agent-harness-to-sdk

A **triage harness**: grow expertise during interactive development, then promote
that knowledge into autonomous, callable agents.

- A **triage agent** is a *pure router* — it classifies an issue, picks an
  expert, calls it, and relays the answer. It holds no domain fixes itself.
- An **expert** is the unit of knowledge and the unit of promotion. It owns its
  **playbooks** (issue → fix), **skills** (research orchestration), and
  **scripts** (deterministic tools). One codebase, two faces: an *interactive dev
  mode* to grow it and a *callable mode* (subprocess, question in → JSON out).

Full design: [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md).

## Layout

```
harness/    shared core (stdlib + PyYAML): contract, playbook, scripts, registry, cli
experts/    one directory per expert; copy _template to start a domain
triage/     the pure-router agent (AGENT.md + routing.md)
docs/        ARCHITECTURE, CONTRACT, PROMOTION, AUTHORING
```

## Quickstart

Install the core (PyYAML only — the SDK is an optional extra):

```bash
pip install -e .
```

### Call an expert

```bash
# Matches the template playbook -> status "ok"
python -m experts._template ask "example symptom here"

# No match -> status "need_info"
python -m experts._template ask "totally unrelated text"
```

Output is one JSON object on stdout (the contract: [`docs/CONTRACT.md`](docs/CONTRACT.md)).

### Inspect the registry (what triage routes over)

```bash
python -c "from harness.registry import as_table; print(as_table())"
```

### Run triage

In a Claude Code session, point the agent at [`triage/AGENT.md`](triage/AGENT.md)
and give it an issue. It will list experts from the registry, classify the issue
([`triage/routing.md`](triage/routing.md)), shell out to the chosen expert, and
relay the JSON answer.

### Start a new domain

```bash
cp -r experts/_template experts/<your-domain>
# edit expert.yaml, point __main__.py at experts.<your-domain>, write real
# playbooks/skills/scripts — see docs/AUTHORING.md
```

## Promotion path

Ad-hoc triage → playbook → skill + script → proven in dev mode → wired into the
callable CLI → registered with triage. See [`docs/PROMOTION.md`](docs/PROMOTION.md).

## Not yet (documented futures)

- A code-release expert (named future consumer).
- MCP / HTTP transports (CLI only; the contract leaves room for a wrapper).
- A real model-backed `ask()` (ships as a deterministic stub; the `sdk` extra and
  each expert's `DEV.md` document the upgrade).
