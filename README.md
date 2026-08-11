# SafeguardShift

**Evaluating LLM agent sensitivity and resilience under controlled institutional safeguard ablation.**

SafeguardShift is the successor to CrisisBench V1. CrisisBench V1 remains immutable at commit `f4bfb19eadf68b15a3bd380992d70496df6ac258` and branch `archive/v1.0.0-canonical`.

SafeguardShift V2 is the completed version 2.0.0 study. Canonical collection, validation, recovery, frozen analysis, result publication, and provenance recording are complete.

## What SafeguardShift tests

SafeguardShift asks a specific agent-safety question: when an institutional safeguard disappears, does an LLM agent merely notice the changed environment, does it become more conservative, or can it safely reconstruct the missing operational capacity through an available substitute?

The benchmark separates three concepts that are often conflated:

- **sensitivity**: whether behavior changes when a relevant safeguard is removed;
- **conservatism**: whether the agent retreats from risk when support disappears;
- **resilience**: whether the agent can recover safe capability using an explicit substitute.

The central empirical result is that **sensitivity to missing safeguards is not the same as resilience to missing safeguards**.

## Final study status

The complete primary behavioral estimand contains:

- 72 base tasks;
- 6 operational domains;
- 6 safeguard classes;
- 5 matched conditions per task;
- 3 independent replicates;
- 3 complete backbone models: GPT-4.1 Mini, Gemini 2.5 Flash Lite, and Mistral Small 3.2;
- exactly **3,240/3,240 primary trajectories**;
- **0 missing primary cells**;
- **0 duplicate accepted primary cells**.

The separate frontier diagnostic contains **60/60 trajectories** across GPT-5.4 and Claude Sonnet 5.

DeepSeek V3.2 is retained separately as a provider/interface reliability diagnostic with **586/1,080 accepted cells**. It is not pooled into the primary behavioral estimand.

## Primary findings

| Measure | Final result |
|---|---:|
| Explicit substitute use | **0/648 = 0%** |
| Substitute-target execution | **0/648 = 0%** |
| Phantom-capacity behavior | **148/1,296 = 11.42%** |
| Safe recovery after phantom capacity | **28/148 = 18.92%** |
| Pooled selective adaptation | **0.02497** |
| Selective-adaptation task-bootstrap 95% interval | **[-0.01798, 0.06646]** |
| Executed-risk delta, relevant ablation minus full | **-0.02469** |
| Executed-risk task-bootstrap 95% interval | **[-0.03279, -0.01736]** |
| Terminal compliance | **3,085/3,240 = 95.22%** |
| Unsafe dependency violations | **1/1,296 = 0.077%** |

The strongest result is not widespread reckless behavior after safeguard removal. Agents often responded conservatively when institutional support disappeared, but none of the three primary models used the explicit substitute mechanism across 648 opportunities. SafeguardShift therefore identifies a gap between **behavioral sensitivity** and **functional resilience**.

The experiment also identifies **phantom-capacity behavior**. In 148 of 1,296 relevant or compound ablation trajectories, agents behaved as though unavailable institutional capacity still existed. Only 28 of those 148 cases ended in safe recovery.

The negative executed-risk delta indicates that relevant safeguard removal generally made agents more conservative rather than more risk-seeking. This distinguishes **safety through retreat** from **resilience through substitution**.

## Model-level results

| Model | Terminal compliance | Selective adaptation | Mean safe utility |
|---|---:|---:|---:|
| GPT-4.1 Mini | **100.00%** | 0.02323 | 0.33281 |
| Mistral Small 3.2 | **98.70%** | 0.00540 | 0.46401 |
| Gemini 2.5 Flash Lite | **86.94%** | 0.04630 | 0.08647 |

All three primary models recorded **0% explicit substitute use**.

Full primary estimates, bootstrap intervals, safeguard-level breakdowns, reliability statistics, and ranking-stability results are in `results/v2/primary3_summary.json`.

## Experimental design

SafeguardShift V2 uses:

- a balanced **6 domains x 6 safeguards x 2 scenarios = 72 base tasks** design;
- five matched conditions per task;
- domain-specific executable actions mapped to a hidden common ontology;
- mechanically isolated irrelevant-safeguard negative controls;
- an explicit substitute whose successful use restores the missing function;
- executable oracle checks for all **360 task-condition cells**;
- three repeated trajectories for every primary backbone cell;
- task-clustered bootstrap inference;
- safeguard-specific estimates;
- separate tool and terminal reliability reporting;
- separate frontier-model diagnostic replication.

V2 does not overwrite or retrospectively re-score CrisisBench V1.

## Safeguard classes

The six safeguard classes are:

- authority;
- execution capacity;
- expert review;
- monitoring;
- reversibility;
- verification.

The safeguard-level analysis is reported in `results/v2/primary3_summary.json`. Reversibility produced the most negative selective-adaptation estimate, while authority, expert review, monitoring, and verification were positive on that measure. These subgroup estimates should be interpreted with their task-bootstrap intervals rather than as standalone rankings.

## Validation boundary

Before canonical collection, the benchmark passed:

- deterministic dataset verification;
- the 360-condition executable oracle;
- the frozen construct-validation procedure;
- corruption-control qualification.

GPT-5.4 and Claude Sonnet 5 unanimously approved all seven construct criteria for all 72 real tasks. GPT-5.4 is the formal corruption sentinel after detecting all 12 deliberate corruption controls. Claude remains a required unanimous real-task reviewer, while its weaker repeat corruption-control performance is retained transparently as a diagnostic result.

Validators assess the benchmark specification only. They do not grade canonical agent outputs.

The complete validation and amendment history is recorded in:

- `v2/docs/AMENDMENTS.md`;
- `v2/amendments/`;
- `results/v2/construct_validation.json`;
- `results/v2/validator_qualification_provenance.json`.

## Provider and recovery provenance

Canonical acceptance used a fixed, outcome-blind source-priority rule. The first valid observation for an expected model/task/replicate/condition key was retained. Later duplicates were excluded. Already accepted behavioral rows were never replaced.

Mistral transport failures required documented operational amendments before final behavioral analysis. These amendments changed serving and retry mechanics only for still-missing keys. They did not change tasks, prompts, tools, model identifier, temperature, scoring, hypotheses, replicate identifiers, or analysis definitions.

The final completion stage started from a fixed **3,222-cell** matrix and filled only the remaining **18 Mistral keys**. The final provenance record is `results/v2/primary3_final_provenance.json`.

## DeepSeek provider diagnostic

DeepSeek V3.2 on the pinned DeepInfra route experienced substantial provider/interface attrition, including HTTP-success payloads without a usable choices array and malformed or truncated response bodies.

Under the pre-analysis operational amendment in `v2/amendments/005_primary_estimand_provider_attrition.md`:

- DeepSeek is not pooled into the primary behavioral estimand;
- **586/1,080** accepted cells are preserved;
- **494** cells remain missing;
- its evidence is treated as a provider/interface reliability diagnostic;
- incomplete-case behavioral summaries are descriptive only.

See `results/v2/deepseek_provider_diagnostic.json`.

## Reliability

Across the 3,240 primary trajectories:

- exact action-set agreement across replicate groups: **57.31%**;
- mean pairwise action-set consistency: **85.87%**;
- terminal failure rate: **4.78%**;
- no-tool-call rate: **3.33%**;
- malformed-argument rate: **1.60%**;
- parallel-call rate: **5.80%**.

These measures are reported separately from the behavioral safety estimands.

## Canonical raw evidence

The final verified V2 evidence bundle was produced by GitHub Actions run `31477490866` on 2026-08-11.

Canonical Actions artifact:

- name: `safeguardshift-v2-primary3-COMPLETE`;
- artifact ID: `9095878773`;
- artifact ZIP SHA-256: `8a7443c331e6875f004ed2134946d62e962d1e6487ce376f0897547b71bb534c`;
- artifact size: 5,032,508 bytes;
- GitHub Actions retention expiry: 2026-11-09.

Canonical raw-file checksums:

| File | Bytes | SHA-256 |
|---|---:|---|
| `canonical-primary3.jsonl` | 62,792,768 | `d973aeedf05d9cae38cc859fc9249c3f6859eb8947b586e8d256dad6912f0597` |
| `canonical-frontier.jsonl` | 1,329,252 | `698962393621163cba9eaff7f1790a4f0ead74d14a081a676da98a2702278d4c` |
| `deepseek-provider-diagnostic.jsonl` | 11,801,930 | `e42f901067904abeba8100c2e2aa94551e7dbf1b72f223be0d0cf0b0f3f21d97` |
| `primary3-missing-final.json` | 3 | `37517e5f3dc66819f61f5a7bb8ace1921282415f10551d2defa5c3eb0985b570` |

The release should preserve the exact evidence bundle byte-for-byte. The committed hashes allow any permanent mirror or GitHub Release asset to be independently verified.

See `results/v2/RAW_DATA.md` and `results/v2/primary3_final_provenance.json`.

## Release freeze

SafeguardShift V2 is frozen as **version 2.0.0**. The release tag `v2.0.0` should point to the final release-preparation commit on `main` after all checks below pass.

The scientific state covered by this release includes:

- task specifications;
- prompts and tool interfaces;
- hypotheses and scoring definitions;
- construct validation;
- all documented operational amendments;
- the complete 3,240-cell primary estimand;
- the 60-cell frontier diagnostic;
- the DeepSeek provider/interface diagnostic;
- frozen behavioral analysis;
- result summaries;
- canonical evidence checksums;
- citation metadata.

Any future scientific modification should occur after the `v2.0.0` release rather than silently changing the canonical V2 release.

## Reproduce validation and analysis

```bash
python -m pip install -e '.[dev]'
pytest
safeguardshift verify
python scripts_v2/run_oracle.py
python scripts_v2/check_freeze.py
python scripts_v2/check_construct_validation.py results/v2/construct_validation.json
```

Given the raw evidence bundle, the final primary matrix can be assembled with `scripts_v2/assemble_primary3.py` and analyzed with `scripts_v2/analyse_primary3.py`. DeepSeek provider coverage is assembled separately with `scripts_v2/assemble_deepseek_diagnostic.py`.

## Research boundary

SafeguardShift V2 is a controlled synthetic benchmark. It does not claim external domain-expert certification, ecological validity, or complete real-world crisis doctrine. Its claims concern agent behavior under the benchmark's controlled institutional-safeguard manipulations.

## Repository map

- `v2/docs/DESIGN.md` - study design;
- `v2/docs/HYPOTHESES.md` - frozen hypotheses;
- `v2/docs/SCORING.md` - scoring definitions;
- `v2/docs/CONSTRUCT_VALIDATION.md` - construct-validation protocol;
- `v2/amendments/` - documented operational amendments;
- `results/v2/primary3_summary.json` - primary behavioral analysis;
- `results/v2/frontier_summary.json` - frontier diagnostic analysis;
- `results/v2/deepseek_provider_diagnostic.json` - DeepSeek provider diagnostic;
- `results/v2/primary3_final_provenance.json` - final provenance;
- `results/v2/RAW_DATA.md` - canonical evidence hashes and artifact details.

## Citation

Citation metadata is provided in `CITATION.cff`.

SafeguardShift V2 is licensed under Apache-2.0.
