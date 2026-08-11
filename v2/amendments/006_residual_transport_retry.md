# Amendment 006: residual transport retry

Date: 2026-08-11

## Scope

This is an operational recovery amendment only. It does not change the frozen benchmark, tasks, model panel, prompts, tool definitions, scoring, hypotheses, or analysis.

After the outcome-blind three-model assembly accepted 2,972 of 3,240 expected primary cells, exactly 268 cells remained missing. Every missing cell belonged to `mistralai/mistral-small-3.2-24b-instruct` on the pinned Venice route.

The missing cells arose from provider/interface failures in which an HTTP-success response either could not be parsed as JSON or did not contain a non-empty `choices` array. Such a response cannot constitute an agent turn and therefore cannot be scored as a behavioral observation.

## Recovery rule

For only the 268 cells listed in `primary3-missing-after-final.json`, the recovery helper may retry the identical frozen request when either:

1. the response body is malformed JSON, or
2. the parsed response has no non-empty `choices` array.

No retry is triggered by the semantic content, action choice, score, or terminal outcome of a valid model response. Successful previously accepted cells are never rerun. The same model ID, provider route, prompts, tools, token limit, temperature, environment, and scoring remain fixed.

Each retry is cost-gated. Each successful recovered trajectory records the number of transport retries used for that trajectory.

## Final acceptance

The primary behavioral analysis remains blocked unless the fixed source-priority assembler verifies exactly 3,240 unique expected cells and zero missing cells. The 2,972 already accepted cells have priority over residual recovery rows, so the recovery cannot replace or cherry-pick earlier valid outcomes.
