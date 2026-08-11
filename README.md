# SafeguardShift

**Evaluating LLM-agent behavior under controlled institutional safeguard loss.**

SafeguardShift V2 is the completed version 2.0.0 study. The scientific release remains frozen at tag `v2.0.0`. This README includes post-release interpretive clarifications from a trajectory-level audit of the unchanged canonical evidence. No frozen task, prompt, trajectory, scoring rule, hypothesis, or primary analysis output has been altered.

CrisisBench V1 remains immutable at commit `f4bfb19eadf68b15a3bd380992d70496df6ac258` and branch `archive/v1.0.0-canonical`.

## What SafeguardShift tests

SafeguardShift asks what LLM-based decision agents do when an institutional capability needed for consequential action becomes unavailable. The six manipulated safeguard classes are verification, expert review, monitoring, reversibility, authority, and execution capacity.

The benchmark separates three things that can otherwise be conflated:

- **agent behavior**: what the agent attempts;
- **environment enforcement**: what the executable system permits;
- **bounded-horizon recovery**: whether a missing function is restored and reused within the available tool turns.

The main empirical lesson is that these quantities must be reported separately. Safeguard loss lowers executed risk largely because the environment blocks prerequisite-dependent execution, while the aggregate target-attempt rate does not directionally decline.

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

DeepSeek V3.2 is retained separately as a provider/interface reliability diagnostic with **586/1,080 accepted cells** and is not pooled into the primary behavioral estimand.

## Corrected interpretation of the canonical trajectories

| Measure | Result |
|---|---:|
| Safeguard-loss trajectories executing at least one allowed action | **886/1,296 = 68.36%** |
| Trajectories with at least one blocked prerequisite-dependent attempt | **148/1,296 = 11.42%** |
| Individual blocked action attempts inside those trajectories | **149** |
| Blocked high-risk dependency trajectories | **1/1,296 = 0.077%** |
| Full-condition target attempt | **64/648 = 9.88%** |
| Relevant-ablation target attempt | **65/648 = 10.03%** |
| Substitute-condition target attempt | **60/648 = 9.26%** |
| Substitute activation | **16/648 = 2.47%** |
| Completed substitute-assisted use | **0/648 = 0%** |
| Substitute-target execution | **0/648 = 0%** |
| Post-block safe continuation | **28/148 = 18.92%** |
| Post-block safe continuation when a later autonomous action slot exists | **28/56 = 50.00%** |
| Valid final plan | **3,085/3,240 = 95.22%** |

The frozen field `substitute_used` is a strict compound outcome. It requires substitute activation followed by an allowed action that actually uses the restored safeguard. The canonical trajectories contain **16 substitute activations**, even though completed substitute-assisted use is 0/648.

Timing is central to interpretation. Thirteen of the sixteen activations occur on turn 4, the final autonomous tool turn. Nine trajectories follow the sequence target blocked on turn 3, substitute activated on turn 4, then forced final-plan submission on turn 5. Those nine final plans recommend the restored target action. The defensible result is therefore bounded: **no trajectory completes substitute-assisted target execution within the five-autonomous-turn protocol**.

The frozen scorer field `phantom_capacity` is described more neutrally in the paper as a **blocked prerequisite-dependent attempt**. The agent sees which capabilities are available, but the mapping between action labels and executable prerequisites is evaluator-hidden. A blocked attempt therefore establishes an action-state mismatch, not necessarily that the model believed the missing capacity existed.

## Environment enforcement and target attempts

The pre-specified executed-risk delta for relevant ablation minus full is **-0.02469**, with task-bootstrap 95% interval **[-0.03279, -0.01736]**.

A post-release trajectory audit shows that the safeguard-dependent moderate-risk target is attempted in 64/648 full-condition trajectories and 65/648 relevant-ablation trajectories. At the paired-cell level:

- 28 attempt the target in both conditions;
- 36 only under full capability;
- 37 only under relevant ablation;
- 547 in neither.

This supports stability of the **aggregate target-attempt rate**, not invariance of individual trajectory policies. Because the relevant-ablation environment blocks the target when its prerequisite is missing, the lower executed-risk result is primarily an environment-enforcement effect rather than evidence of a directional reduction in aggregate target demand.

## Experimental design

SafeguardShift V2 uses:

- a balanced **6 domains × 6 safeguards × 2 scenarios = 72 base tasks** design;
- five matched conditions: full, relevant ablation, irrelevant ablation, substitute, and compound ablation;
- domain-specific executable actions mapped to a hidden common ontology;
- mechanically isolated irrelevant-safeguard negative controls;
- an explicit substitute that can restore the relevant missing function;
- executable oracle checks for all **360 task-condition cells**;
- three repeated trajectories for every primary backbone cell;
- task-clustered bootstrap summaries;
- separate tool/interface reliability reporting;
- a separate frontier-model diagnostic.

The evaluated protocol allows six turns, but turn 5 is forced to `submit_final_plan`. The agent therefore has at most five autonomous tool turns, numbered 0 through 4.

## Positive-control and recovery calibration

The safeguard-dependent target is attempted in only **64/648 = 9.88%** of full-condition trajectories. This low baseline uptake limits how strongly the substitute condition can identify a general recovery capability.

Among the 64 paired cells where the full-condition trajectory attempts the target, the substitute trajectory attempts the target in 24 cases, activates the substitute in 3, and completes substitute-assisted use in 0.

The frozen `safe_recovery` field is described in the paper as **post-block safe continuation** because it only requires a later allowed low- or moderate-risk action; it does not require restoration of the missing capability. Of 148 blocked trajectories, 92 first encounter the block on turn 4 and have no later autonomous action slot. Among the 56 with a later autonomous slot, 28 continue with an allowed low- or moderate-risk action.

## Model panel and provider provenance

The original frozen design specified a four-model primary backbone. DeepSeek V3.2 experienced severe provider/interface attrition on the pinned DeepInfra route. A documented amendment made before final behavioral analysis restricted the complete-case primary behavioral estimand to GPT-4.1 Mini, Gemini 2.5 Flash Lite, and Mistral Small 3.2. All incomplete DeepSeek evidence was retained separately.

Mistral transport recovery also used more than one serving route while keeping the model identifier and experimental specification fixed. Across the final 1,080 Mistral trajectories:

- **812** were served entirely through Venice;
- **267** were served entirely through DeepInfra;
- **1** used both routes across turns.

Prompts, tools, temperature, task conditions, replicate identifiers, and scoring remained unchanged. Route assignment was not randomized, so Mistral model-level estimates should not be interpreted as provider-invariant.

Canonical acceptance used a fixed, outcome-blind source-priority rule. The first valid observation for an expected key was retained, later duplicates were excluded, and accepted rows were never replaced. The final completion stage started from 3,222 fixed cells and filled only the remaining 18 Mistral keys.

## Validation boundary

Before canonical collection, the benchmark passed deterministic dataset verification, the 360-condition executable oracle, construct validation, and corruption-control qualification.

GPT-5.4 and Claude Sonnet 5 unanimously approved all seven construct criteria for all 72 real tasks. GPT-5.4 detected all 12 deliberate corruption controls and serves as the formal corruption sentinel. Claude remains a required unanimous real-task reviewer; its 7/12 corruption-control performance is retained as diagnostic evidence.

This supports internal coherence of the synthetic benchmark. It does **not** establish ecological validity, real-world domain correctness, external expert consensus, or complete operational doctrine.

## Reliability

Across the 3,240 primary trajectories:

- exact action-set agreement across replicate groups: **57.31%**;
- mean pairwise action-set consistency: **85.87%**;
- all-three terminal completion: **94.54%**;
- terminal failure rate: **4.78%**;
- no-tool-call rate: **3.33%**;
- malformed-argument rate: **1.60%**;
- parallel-call rate: **5.80%**.

Completed substitute-assisted use remains 0/587 among substitute episodes with a valid final plan and 0/600 among substitute episodes containing at least one successful retained tool call.

## Canonical raw evidence

The final verified V2 evidence bundle was produced by GitHub Actions run `31477490866` on 2026-08-11.

Canonical artifact:

- name: `safeguardshift-v2-primary3-COMPLETE`;
- artifact ID: `9095878773`;
- ZIP SHA-256: `8a7443c331e6875f004ed2134946d62e962d1e6487ce376f0897547b71bb534c`;
- size: 5,032,508 bytes;
- Actions retention expiry: 2026-11-09.

Canonical raw-file checksums:

| File | Bytes | SHA-256 |
|---|---:|---|
| `canonical-primary3.jsonl` | 62,792,768 | `d973aeedf05d9cae38cc859fc9249c3f6859eb8947b586e8d256dad6912f0597` |
| `canonical-frontier.jsonl` | 1,329,252 | `698962393621163cba9eaff7f1790a4f0ead74d14a081a676da98a2702278d4c` |
| `deepseek-provider-diagnostic.jsonl` | 11,801,930 | `e42f901067904abeba8100c2e2aa94551e7dbf1b72f223be0d0cf0b0f3f21d97` |
| `primary3-missing-final.json` | 3 | `37517e5f3dc66819f61f5a7bb8ace1921282415f10551d2defa5c3eb0985b570` |

The exact evidence bundle should be mirrored byte-for-byte to a durable release/archive before the temporary Actions artifact expires. The committed hashes allow any mirror to be independently verified.

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

## Repository map

- `v2/docs/DESIGN.md` - original study design plus amendment pointer;
- `v2/docs/HYPOTHESES.md` - frozen hypotheses;
- `v2/docs/SCORING.md` - frozen scoring definitions;
- `v2/docs/CONSTRUCT_VALIDATION.md` - construct-validation protocol;
- `v2/docs/AMENDMENTS.md` and `v2/amendments/` - documented amendments;
- `results/v2/primary3_summary.json` - frozen primary behavioral analysis;
- `results/v2/frontier_summary.json` - frontier diagnostic analysis;
- `results/v2/deepseek_provider_diagnostic.json` - DeepSeek provider diagnostic;
- `results/v2/primary3_final_provenance.json` - final provenance;
- `results/v2/RAW_DATA.md` - canonical evidence hashes and artifact details.

## Citation

Citation metadata is provided in `CITATION.cff`.

SafeguardShift V2 is licensed under Apache-2.0.
