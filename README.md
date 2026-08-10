# CrisisBench

**Agentic evaluation of capacity-conditioned safety under institutional safeguard ablation.**

CrisisBench tests whether AI agents change what they *do* when the external safeguards that normally verify, review, monitor, authorize, reverse, or safely execute a high-stakes action disappear.

The v1 benchmark replaces the original high-capacity/low-capacity prompt-pair design with controlled causal interventions. Each base task is held fixed while one institutional safeguard is removed, an irrelevant safeguard is removed as a negative control, a substitute safeguard is offered, or multiple safeguards are ablated.

## Research question

> Do AI agents selectively adapt their trajectories when task-relevant institutional safeguards are removed, while the underlying actor, objective, facts, urgency, and authority framing remain fixed?

## v1 design

- 36 synthetic base tasks across six institutional crisis domains.
- Five matched conditions per task, producing 180 scenario cells before model replication.
- Stateful, bounded agent trajectories with deterministic tools and hidden action contracts.
- Primary outcomes derived from executable environment state rather than an LLM judge.
- OpenRouter multi-model harness with exact model/provider routing, no silent fallback, request provenance, and hard cost controls.
- Frozen protocol, hypotheses, scoring rules, model panel, hashes, and release verification.

## Safeguard interventions

1. Full safeguards
2. Relevant safeguard ablation
3. Irrelevant safeguard ablation
4. Relevant ablation with a feasible substitute
5. Compound ablation

The six manipulable safeguards are verification, expert review, monitoring, reversibility, authority, and execution capacity.

## Primary metrics

Unsafe invariance, phantom-capacity reliance, feasible substitution, safe recovery, task completion, utility preservation, irreversible error intent, and selective adaptation.

## Agent environment

Agents may inspect state, check capacity, attempt one of the task's named actions, request a substitute safeguard where available, and submit a structured final plan. The synthetic environment blocks actions whose frozen prerequisites are missing while preserving the attempted action for analysis.

## OpenRouter

Set the API key only in the environment:

```bash
export OPENROUTER_API_KEY=...
```

The repository expects the variable name **`OPENROUTER_API_KEY`**. Never commit a key. Canonical paid collection is manual-only.

## Quick validation

```bash
python -m pip install -e .
crisisbench verify
pytest
crisisbench freeze
```

## Status

**v1 research design and execution harness implemented.** The repository is ready for provider preflight and canonical collection once an OpenRouter key is supplied to the execution environment. No canonical model results are claimed before that collection occurs.

See `docs/PROTOCOL.md`, `docs/CONSTRUCT.md`, `docs/SCORING.md`, and `docs/LIMITATIONS.md`.
