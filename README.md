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
- mandatory independent expert-validation gate before paid canonical collection.

The four-model backbone contains 4,320 planned trajectories. V2 does **not** overwrite or retrospectively re-score V1.

## Zero-cost validation

```bash
python -m pip install -e '.[dev]'
pytest
safeguardshift verify
python scripts_v2/run_oracle.py
```

## Canonical execution

Canonical OpenRouter execution is intentionally disabled until independent expert validation and a new explicit budget approval are both present. The API variable remains `OPENROUTER_API_KEY`.

See `v2/docs/DESIGN.md`, `v2/docs/HYPOTHESES.md`, `v2/docs/SCORING.md`, and `v2/docs/EXPERT_VALIDATION.md`.
