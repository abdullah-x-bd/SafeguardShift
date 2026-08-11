# SafeguardShift V2 release freeze

Version: `2.0.0`

Release date: `2026-08-11`

Canonical release tag: `v2.0.0`

## Freeze rule

The commit referenced by the annotated Git tag `v2.0.0` is the canonical public code and analysis snapshot for SafeguardShift V2.

After that tag is created, the V2 release must not be silently rewritten. Any later scientific change to tasks, prompts, tools, model panel, conditions, scoring, hypotheses, estimands, analysis definitions, accepted evidence, or reported results requires a later version and an explicit changelog entry.

CrisisBench V1 remains separately frozen at commit `f4bfb19eadf68b15a3bd380992d70496df6ac258` and branch `archive/v1.0.0-canonical`.

## Completed V2 state

Primary behavioral estimand:

- 3 backbone models;
- 72 base tasks;
- 5 matched conditions;
- 3 replicates;
- 3,240 expected cells;
- 3,240 accepted cells;
- 0 missing cells;
- 0 duplicate accepted cells.

Primary models:

- `openai/gpt-4.1-mini`;
- `google/gemini-2.5-flash-lite`;
- `mistralai/mistral-small-3.2-24b-instruct`.

Frontier diagnostic:

- GPT-5.4 and Claude Sonnet 5;
- 60/60 trajectories complete.

DeepSeek provider/interface diagnostic:

- model: `deepseek/deepseek-v3.2`;
- provider: DeepInfra;
- 586/1,080 accepted cells;
- 494 missing cells;
- excluded from the pooled primary behavioral estimand under amendment 005.

## Frozen headline results

- explicit substitute use: `0/648 = 0%`;
- substitute-target execution: `0/648 = 0%`;
- phantom-capacity behavior: `148/1,296 = 11.42%`;
- safe recovery after phantom capacity: `28/148 = 18.92%`;
- pooled selective adaptation: `0.02497427983539095`;
- selective-adaptation task-bootstrap 95% interval: `[-0.017978395061728398, 0.06646090534979425]`;
- executed-risk delta, relevant ablation minus full: `-0.024691358024691357`;
- executed-risk task-bootstrap 95% interval: `[-0.0327932098765432, -0.01736111111111111]`;
- terminal compliance: `3,085/3,240 = 95.21604938271605%`;
- unsafe dependency violations: `1/1,296 = 0.07716049382716049%`.

The final primary analysis is `results/v2/primary3_summary.json`.

## Canonical evidence bundle

The final verified evidence bundle was produced by GitHub Actions run `31477490866`.

Artifact:

- name: `safeguardshift-v2-primary3-COMPLETE`;
- artifact ID: `9095878773`;
- ZIP SHA-256: `8a7443c331e6875f004ed2134946d62e962d1e6487ce376f0897547b71bb534c`;
- size: 5,032,508 bytes;
- Actions retention expiry: `2026-11-09`.

Canonical raw-file hashes:

| File | Bytes | SHA-256 |
|---|---:|---|
| `canonical-primary3.jsonl` | 62,792,768 | `d973aeedf05d9cae38cc859fc9249c3f6859eb8947b586e8d256dad6912f0597` |
| `canonical-frontier.jsonl` | 1,329,252 | `698962393621163cba9eaff7f1790a4f0ead74d14a081a676da98a2702278d4c` |
| `deepseek-provider-diagnostic.jsonl` | 11,801,930 | `e42f901067904abeba8100c2e2aa94551e7dbf1b72f223be0d0cf0b0f3f21d97` |
| `primary3-missing-final.json` | 3 | `37517e5f3dc66819f61f5a7bb8ace1921282415f10551d2defa5c3eb0985b570` |

The exact artifact should be attached to or permanently mirrored alongside the GitHub Release. The hashes above are the integrity authority for the raw bundle.

## Provenance

Canonical acceptance followed a fixed outcome-blind priority rule. Accepted rows were never replaced. The final completion stage began from 3,222 fixed cells and filled only the remaining 18 Mistral cells.

The final provenance file is `results/v2/primary3_final_provenance.json`.

The documented operational amendment sequence is retained in `v2/amendments/`, including amendments 005 through 010 relevant to the final estimand and transport recovery.

## Release verification

Before creating the `v2.0.0` tag, run:

```bash
python -m pip install -e '.[dev]'
pytest
safeguardshift verify
python scripts_v2/run_oracle.py
python scripts_v2/check_freeze.py
python scripts_v2/check_construct_validation.py results/v2/construct_validation.json
```

Then verify that `results/v2/primary3_canonical_verification.json` reports 3,240 accepted cells and 0 missing cells and that the working tree is clean.

The tag must be created only after these checks pass.
