# Amendment 007: Cell-local transport completion

## Timing

Adopted after the primary three-model matrix reached 3,059 / 3,240 accepted cells and before primary behavioral analysis.

## Problem

The remaining 181 cells all belonged to `mistralai/mistral-small-3.2-24b-instruct` on the frozen Venice route. Recovery attempts showed intermittent transport-invalid OpenRouter responses, especially HTTP-success payloads without a non-empty `choices` array. The previous recovery helper retried an identical request several times but terminated the entire domain shard if one cell exhausted those retries. This caused valid progress later in the shard to remain unattempted.

## Amendment

Recovery is made cell-local and outcome-blind.

1. The accepted 3,059-cell matrix is fixed as the priority baseline.
2. Only keys absent from that matrix are eligible for recovery.
3. For an eligible cell, malformed JSON or an HTTP-success response without a non-empty `choices` array may be retried using the identical frozen request.
4. If a cell still has a transport-invalid response after the local retry limit, that cell is recorded as a transport failure and the shard continues to the next missing cell.
5. Subsequent passes are generated only from the exact missing-key manifest produced after the previous pass.
6. A previously accepted cell is never replaced by a later recovery output. First-valid-cell provenance remains fixed and outcome-blind.
7. No retry decision may depend on behavioral content, score, action choice, utility, or hypothesis direction.
8. Primary behavioral analysis remains blocked until the matrix contains exactly 3,240 unique expected cells and zero missing cells.

## Scientific scope

This amendment changes only operational handling of provider-invalid responses during exact-cell completion. It does not change tasks, prompts, conditions, safeguard manipulations, model identity, provider route, tools, temperature, token limits, scoring, hypotheses, or analysis definitions.
