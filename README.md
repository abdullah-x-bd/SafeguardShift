# SafeguardShift

**Evaluating LLM agent sensitivity and resilience under controlled institutional safeguard ablation.**

SafeguardShift is the successor to CrisisBench V1. V1 is immutable at commit `f4bfb19eadf68b15a3bd380992d70496df6ac258` and branch `archive/v1.0.0-canonical`.

## Study 2

V2 addresses the exact limitations exposed by V1:

- balanced 6 domains × 6 safeguards × 2 scenarios = 72 base tasks;
- five matched conditions per task;
- domain-specific executable actions mapped to a hidden common ontology;
- an explicit substitute whose successful use unlocks a higher-utility safe action;
- executable oracle checks for all 72 substitute conditions;
- three repeated trajectories for every four-model backbone cell;
- frontier models kept separate as diagnostic replication;
- tool/terminal reliability reported separately from safety behavior;
- task-clustered bootstrap inference and safeguard-specific estimates;
- frozen Triangulated Synthetic Construct Validation before paid canonical collection.

The four-model backbone contains 4,320 planned trajectories. V2 does **not** overwrite or retrospectively re-score V1.

## Validation boundary

V2 is deliberately a controlled synthetic benchmark. It does not claim external domain-expert certification or complete real-world crisis doctrine.

Before canonical collection, the benchmark must pass deterministic dataset checks, a 360-condition executable oracle, a three-model blinded construct panel over all 72 tasks, and 12 balanced corruption controls. The validators assess the benchmark specification only and never grade canonical agent outputs.

The first construct-validation execution is retained only as a technical pilot because long validation-tool output was truncated for two judge families. The frozen criteria/panel are rerun from scratch with compact Boolean serialization before any canonical outcome is collected. See `v2/docs/AMENDMENTS.md`.

## Zero-cost validation

```bash
python -m pip install -e '.[dev]'
pytest
safeguardshift verify
python scripts_v2/run_oracle.py
python scripts_v2/check_freeze.py
```

## Canonical execution

Canonical OpenRouter collection remains blocked until the frozen construct-validation result passes and provider preflight succeeds. The V2 program has a single approved ceiling of **$11.70** within the user's $12 authorization: up to $1.70 cumulatively for construct validation including the technical pilot, $6.50 for the 4,320-trajectory backbone, and $3.50 for the 120-trajectory frontier diagnostic. The compact validation rerun itself is capped at $0.80. The API variable remains `OPENROUTER_API_KEY`.

See `v2/docs/DESIGN.md`, `v2/docs/HYPOTHESES.md`, `v2/docs/SCORING.md`, and `v2/docs/CONSTRUCT_VALIDATION.md`.
