# CrisisBench v1 canonical results

## Verification

- 780 / 780 expected trajectories accepted
- 780 unique model-task-condition cells
- 0 duplicates
- 0 missing cells
- Four backbone models: 180 trajectories each
- Two frontier diagnostic models: 30 trajectories each

## Frozen pooled endpoints

| Endpoint | Result |
|---|---:|
| Unsafe invariance | 1.3% (2/156) |
| Phantom capacity | 2.9% |
| Feasible substitution | 0.6% (1/156) |
| Safe recovery after a blocked action | 33.3% (3/9) |
| Task completion | 78.2% |
| Ablated utility preservation | 0.209 |
| Irreversible error intent | 0.6% |
| Selective adaptation score | 0.120 |

## Model-level descriptive results

| Model | Completion | Unsafe invariance | Phantom capacity | Substitute use | Ablated utility | Selective adaptation |
|---|---:|---:|---:|---:|---:|---:|
| openai/gpt-4.1-mini | 100.0% | 2.8% | 5.6% | 0.0% | 0.346 | 0.155 |
| google/gemini-2.5-flash-lite | 95.6% | 0.0% | 0.0% | 0.0% | 0.105 | -0.132 |
| deepseek/deepseek-v3.2 | 10.0% | 0.0% | 0.0% | 0.0% | 0.009 | 0.083 |
| mistralai/mistral-small-3.2-24b-instruct | 100.0% | 2.8% | 6.9% | 2.8% | 0.352 | 0.394 |
| openai/gpt-5.4 | 100.0% | 0.0% | 0.0% | 0.0% | 0.514 | -0.056 |
| anthropic/claude-sonnet-5 | 100.0% | 0.0% | 0.0% | 0.0% | 0.056 | 0.167 |

## Ranking stability

Utility ranking Spearman correlation versus the full-safeguard condition:

- relevant ablation: 0.829
- irrelevant ablation: 0.829
- substitute: 0.771
- compound ablation: 0.928

## Interpretation boundaries

The canonical study shows a pooled directional signal of selective adaptation, but it is highly heterogeneous across models. The strongest negative result is substitute use: only one of 156 substitute-condition trajectories actually activated and then used the offered replacement safeguard. Unsafe invariance and irreversible-error intent were uncommon overall.

Task completion should not be conflated with useful action. DeepSeek frequently failed the structured terminal-tool contract, while Claude often completed by submitting a plan with little executable action utility under this benchmark's action-based utility measure.

These are descriptive outputs from the frozen endpoints. No post-hoc significance threshold or replacement primary metric was introduced after canonical outcomes were observed.
