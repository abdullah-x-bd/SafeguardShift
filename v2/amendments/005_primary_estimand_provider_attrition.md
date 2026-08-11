# Amendment 005: Primary estimand after DeepSeek/DeepInfra provider attrition

Date: 2026-08-11
Status: post-collection operational amendment, before final behavioral analysis

## Decision

The SafeguardShift V2 primary behavioral estimand is changed from the originally planned four-model backbone to the three models with complete recoverable canonical coverage:

- `openai/gpt-4.1-mini` via OpenAI
- `google/gemini-2.5-flash-lite` via Google Vertex
- `mistralai/mistral-small-3.2-24b-instruct` via Venice

The primary matrix therefore requires exactly 3 models × 72 tasks × 5 matched conditions × 3 replicates = 3,240 unique trajectories with zero missing cells.

The already completed frontier diagnostic remains separate and unchanged:

- `openai/gpt-5.4`
- `anthropic/claude-sonnet-5`

DeepSeek V3.2 via DeepInfra is removed from the complete-case primary behavioral estimand and retained as an interface/provider-reliability diagnostic.

## Reason

This change is driven by provider-route execution attrition, not by inspection of favorable or unfavorable behavioral endpoint values. The original DeepSeek/DeepInfra collection produced only a minority of the planned 1,080 cells. Exact recovery therefore required hundreds of additional multi-turn trajectories. During those recoveries, the pinned DeepInfra route repeatedly returned malformed or truncated HTTP-success response bodies that failed JSON decoding, as well as earlier valid JSON responses without a usable `choices` array. These failures occurred before a valid model trajectory could be recorded.

Continuing to retry hundreds of cells until every DeepSeek trajectory happened to complete would create a large outcome-contingent recovery process and risk conditioning the DeepSeek sample on provider success. It would also make provider transport behavior dominate the completion of the behavioral study.

## Analysis rule

1. Primary behavioral analysis uses only the three complete backbone models listed above.
2. All primary metrics, task-clustered inference, hypotheses, scoring definitions, task set, conditions, prompts, tools, and replicate structure remain unchanged.
3. The primary matrix must be exactly 3,240/3,240 with zero duplicates and zero missing cells before analysis runs.
4. Every DeepSeek row already obtained is preserved outcome-blind by fixed provenance priority and summarized separately as provider/interface evidence.
5. DeepSeek diagnostic reporting must include planned cells, accepted cells, coverage rate, provider failures observed during collection/recovery, and a clear warning that its behavioral metrics are incomplete-case descriptive statistics only.
6. No DeepSeek incomplete-case behavioral estimate may be pooled into the primary three-model estimand.
7. The completed GPT-5.4/Claude frontier diagnostic remains a separate 60-cell diagnostic and is not pooled into the primary backbone.

## Interpretation boundary

The paper must state that the primary behavioral conclusions generalize across the three complete backbone models evaluated under the frozen SafeguardShift V2 protocol. DeepSeek provides evidence about deployment/interface reliability on the evaluated OpenRouter/DeepInfra route, not a complete behavioral replication. A future provider-robust DeepSeek replication may be reported separately.

## Lineage

This amendment does not modify V1, the V2 task corpus, condition construction, construct-validation record, oracle, hypotheses, scoring code, or the frozen agent protocol. It changes only the model set included in the complete-case primary behavioral estimand because of severe provider-route attrition observed before final behavioral analysis.
