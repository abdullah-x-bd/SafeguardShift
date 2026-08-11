# SafeguardShift

**Evaluating LLM agent sensitivity and resilience under controlled institutional safeguard ablation.**

SafeguardShift is the successor to CrisisBench V1. V1 is immutable at commit `f4bfb19eadf68b15a3bd380992d70496df6ac258` and branch `archive/v1.0.0-canonical`.

## Study 2 status

SafeguardShift V2 canonical collection and frozen analysis are complete.

The final primary behavioral estimand contains:

- 72 base tasks across 6 domains and 6 safeguard classes;
- 5 matched conditions per task;
- 3 independent replicates;
- 3 complete backbone models: GPT-4.1 Mini, Gemini 2.5 Flash Lite, and Mistral Small 3.2;
- exactly **3,240/3,240 primary trajectories**, with zero missing and zero duplicate accepted cells.

The separate frontier diagnostic contains **60/60 trajectories** across GPT-5.4 and Claude Sonnet 5.

DeepSeek V3.2 on the pinned DeepInfra route suffered severe provider/interface attrition during collection. Under the pre-analysis operational amendment recorded in `v2/amendments/005_primary_estimand_provider_attrition.md`, it is not pooled into the primary behavioral estimand. Its **586/1,080** accepted cells are retained as a provider/interface reliability diagnostic.

## Headline result

The central result is that **sensitivity to missing safeguards is not the same as resilience to missing safeguards**.

Across the complete three-model primary matrix:

- substitute use: **0/648** substitute-condition opportunities;
- substitute-target execution: **0/648**;
- phantom-capacity behavior: **148/1,296 = 11.42%** of relevant/compound ablation trajectories;
- safe recovery after phantom-capacity behavior: **28/148 = 18.92%**;
- pooled selective-adaptation estimate: **0.025**, task-bootstrap 95% interval **[-0.018, 0.066]**;
- terminal compliance: **3,085/3,240 = 95.22%**;
- unsafe dependency violations: **1/1,296 = 0.077%**.

Agents often changed behavior when safeguards disappeared, but they did not reconstruct the explicit substitute capacity offered by the benchmark. The substitute intervention therefore distinguishes behavioral sensitivity from functional resilience.

Full estimates, model breakdowns, safeguard breakdowns, reliability statistics, and bootstrap intervals are in `results/v2/primary3_summary.json`.

## Experimental design

V2 was built to address the limitations exposed by V1:

- balanced 6 domains × 6 safeguards × 2 scenarios = 72 base tasks;
- five matched conditions per task;
- domain-specific executable actions mapped to a hidden common ontology;
- mechanically isolated irrelevant-safeguard negative controls;
- an explicit substitute whose successful use unlocks the missing function;
- executable oracle checks for all 360 task-condition cells;
- three repeated trajectories for every primary backbone cell;
- frontier models kept separate as diagnostic replication;
- tool/terminal reliability reported separately from safety behavior;
- task-clustered bootstrap inference and safeguard-specific estimates;
- synthetic construct validation before canonical collection.

V2 does **not** overwrite or retrospectively re-score V1.

## Validation boundary

V2 is deliberately a controlled synthetic benchmark. It does not claim external domain-expert certification, ecological validity, or complete real-world crisis doctrine.

Before canonical collection, the benchmark passed deterministic dataset verification, a 360-condition executable oracle, and a frozen model-based construct panel. GPT-5.4 and Claude Sonnet 5 unanimously approved all seven construct criteria for all 72 real tasks. GPT-5.4 is the formal corruption sentinel after detecting all 12 deliberate corruption controls; Claude remains a required unanimous real-task reviewer, while its weaker repeat corruption-control performance is reported diagnostically rather than hidden.

Validators assess the benchmark specification only and never grade canonical agent outputs.

The complete validation and amendment history is recorded in `v2/docs/AMENDMENTS.md`, `v2/amendments/`, `results/v2/construct_validation.json`, and `results/v2/validator_qualification_provenance.json`.

## Provider and recovery provenance

Canonical acceptance used a fixed, outcome-blind source-priority rule: the first valid observation for an expected model/task/replicate/condition key was retained, later duplicates were excluded, and already accepted behavioral rows were never replaced.

Mistral transport failures required a sequence of documented operational amendments before final behavioral analysis. These changed serving/retry mechanics only for still-missing keys. They did not change tasks, prompts, tools, model identifier, temperature, scoring, hypotheses, replicate identifiers, or analysis definitions. See `v2/amendments/006_residual_transport_retry.md` through `v2/amendments/010_deepinfra_venice_transport_fallback.md`.

The final completion pass started from a fixed 3,222-cell matrix and filled only the remaining 18 Mistral keys. OpenRouter routing metadata is retained in the recovered rows. The final provenance record is `results/v2/primary3_final_provenance.json`.

## Raw evidence

The canonical raw bundle is checksum-pinned in `results/v2/RAW_DATA.md` and `results/v2/primary3_final_provenance.json`.

Key raw hashes:

- primary 3-model JSONL: `d973aeedf05d9cae38cc859fc9249c3f6859eb8947b586e8d256dad6912f0597`
- frontier JSONL: `698962393621163cba9eaff7f1790a4f0ead74d14a081a676da98a2702278d4c`
- DeepSeek provider diagnostic JSONL: `e42f901067904abeba8100c2e2aa94551e7dbf1b72f223be0d0cf0b0f3f21d97`

The final GitHub Actions evidence artifact is temporary and must be mirrored to a durable research archive before its retention deadline. The committed hashes allow any mirror to be verified byte-for-byte.

## Reproduce validation and analysis

```bash
python -m pip install -e '.[dev]'
pytest
safeguardshift verify
python scripts_v2/run_oracle.py
python scripts_v2/check_freeze.py
```

Given the raw evidence bundle, the final primary matrix can be assembled with `scripts_v2/assemble_primary3.py` and analyzed with `scripts_v2/analyse_primary3.py`. DeepSeek provider coverage is assembled separately with `scripts_v2/assemble_deepseek_diagnostic.py`.

See `v2/docs/DESIGN.md`, `v2/docs/HYPOTHESES.md`, `v2/docs/SCORING.md`, `v2/docs/CONSTRUCT_VALIDATION.md`, and `results/v2/`.
