# CrisisBench

**Agentic evaluation of capacity-conditioned safety under institutional safeguard ablation.**

CrisisBench tests whether AI agents change what they *do* when the external safeguards that normally verify, review, monitor, authorize, reverse, or safely execute a high-stakes action disappear.

The v1 benchmark replaces the original high-capacity/low-capacity prompt-pair design with controlled causal interventions. Each base task is held fixed while one institutional safeguard is removed, an irrelevant safeguard is removed as a negative control, a substitute safeguard is offered, or multiple safeguards are ablated.

## Research question

> Do AI agents selectively adapt their trajectories when task-relevant institutional safeguards are removed, while the underlying actor, objective, facts, urgency, and authority framing remain fixed?

## v1 design

- 36 synthetic base tasks across six institutional crisis domains.
- Five matched conditions per task, producing 180 scenario cells before model replication.
- Four backbone models evaluated on the complete 180-cell matrix.
- GPT-5.4 and Claude Sonnet 5 evaluated on a frozen six-task, 30-cell diagnostic subset each.
- 780 accepted canonical trajectories in total.
- Stateful, bounded agent trajectories with deterministic tools and hidden action contracts.
- Primary outcomes derived from executable environment state rather than an LLM judge.
- OpenRouter multi-model harness with exact provider provenance, no silent fallback, request provenance, and hard cost controls.

## Safeguard interventions

1. Full safeguards
2. Relevant safeguard ablation
3. Irrelevant safeguard ablation
4. Relevant ablation with a feasible substitute
5. Compound ablation

The six manipulable safeguards are verification, expert review, monitoring, reversibility, authority, and execution capacity.

## Primary metrics

Unsafe invariance, phantom-capacity reliance, feasible substitution, safe recovery, task completion, utility preservation, irreversible error intent, and selective adaptation.

## Canonical v1 result

The canonical dataset verifies at **780 / 780 expected trajectories**, with 780 unique model-task-condition cells, zero duplicates, and zero missing cells.

Selected frozen endpoints:

- unsafe invariance: **1.3%** (2/156 matched cells)
- phantom capacity: **2.9%**
- successful substitute use: **0.6%** (1/156)
- safe recovery after a blocked action: **33.3%** (3/9)
- task completion: **78.2%**
- ablated utility preservation: **0.209**
- irreversible error intent: **0.6%**
- selective adaptation score: **0.120**

The pooled result suggests some selective response to task-relevant safeguard removal, but model behavior is highly heterogeneous. The strongest negative result is substitute use: agents almost never successfully used an explicitly available replacement safeguard. See `results/v1/RESULTS.md` for model-level results and interpretation boundaries.

## Agent environment

Agents may inspect state, check capacity, attempt one of the task's named actions, request a substitute safeguard where available, and submit a structured final plan. The synthetic environment blocks actions whose frozen prerequisites are missing while preserving the attempted action for analysis.

## Reproducibility and provenance

The accepted provider routes were OpenAI for GPT-4.1 Mini and GPT-5.4, Google Vertex for Gemini 2.5 Flash Lite, DeepInfra for DeepSeek V3.2, Venice for Mistral Small 3.2, and Anthropic for Claude Sonnet 5. Operational provider failures and recovery rules are recorded in `results/v1/provenance.json`; only designated accepted cells enter the canonical dataset.

Machine-readable outputs are in `results/v1/summary.json`, `results/v1/canonical_verification.json`, `results/v1/claims.json`, and `results/v1/cost_summary.json`.

## OpenRouter

Set the API key only in the environment:

```bash
export OPENROUTER_API_KEY=...
```

The repository expects the variable name **`OPENROUTER_API_KEY`**. Never commit a key. Paid collection workflows are explicit-only.

## Quick validation

```bash
python -m pip install -e .
crisisbench verify
pytest
crisisbench freeze
```

## Status

**CrisisBench v1 canonical collection is complete.** The frozen analysis passes on all 780 accepted trajectories. The accepted canonical trajectories account for approximately **$2.5352** of model-generation cost; a live key-usage snapshot taken during final recovery reported $2.6146 including pilots, preflights, discarded partial runs, and canonical work accrued by that point.

See `docs/PROTOCOL.md`, `docs/CONSTRUCT.md`, `docs/SCORING.md`, `docs/LIMITATIONS.md`, and `results/v1/RESULTS.md`.
