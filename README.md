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
- true task-clustered bootstrap inference and safeguard-specific estimates;
- corruption-qualified synthetic construct validation before paid canonical collection.

The four-model backbone contains 4,320 planned trajectories. V2 does **not** overwrite or retrospectively re-score V1.

## Validation boundary

V2 is deliberately a controlled synthetic benchmark. It does not claim external domain-expert certification or complete real-world crisis doctrine.

Before canonical collection, the benchmark must pass deterministic dataset checks, a 360-condition executable oracle, and the frozen construct panel. Validator candidates are qualified using only 12 deliberately corrupted specifications. GPT-5.4 and Claude Sonnet 5 are the only tested candidates that passed the control threshold; the final panel therefore requires unanimous approval from both qualified judges on all seven construct criteria for all 72 tasks, and both must reject all 12 corruptions. Validators assess the benchmark specification only and never grade canonical agent outputs.

All pre-final task judgments are discarded. The complete qualification and amendment history is recorded in `v2/docs/AMENDMENTS.md` and `results/v2/validator_qualification_provenance.json`.

## Zero-cost validation

```bash
python -m pip install -e '.[dev]'
pytest
safeguardshift verify
python scripts_v2/run_oracle.py
python scripts_v2/check_freeze.py
```

## Canonical execution

Canonical OpenRouter collection remains blocked until the final qualified construct-validation result passes and provider preflight succeeds. Actual validation/qualification spend accrued before the final panel is **$1.65313968**. The final validation is capped at **$0.75**, the 4,320-trajectory backbone at **$6.00**, and the 120-trajectory frontier diagnostic at **$3.30**. The maximum planned V2 program ceiling is therefore **$11.71**, within the user's $12 authorization. The API variable remains `OPENROUTER_API_KEY`.

See `v2/docs/DESIGN.md`, `v2/docs/HYPOTHESES.md`, `v2/docs/SCORING.md`, and `v2/docs/CONSTRUCT_VALIDATION.md`.
