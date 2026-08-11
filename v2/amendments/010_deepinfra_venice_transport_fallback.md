# Amendment 010: DeepInfra to Venice transport fallback for final unresolved Mistral cells

Date: 2026-08-11

## Status

Activated after amendment 009 completed its outcome-blind assembly at 3,222 of 3,240 expected primary cells. Exactly 18 cells remain missing, all from `mistralai/mistral-small-3.2-24b-instruct`. No behavioral analysis has run.

This amendment was prepared prospectively while amendment 009 was still running and was activated only after that finalizer reported a nonzero residual.

## Trigger condition

Amendment 009 used tool-aware OpenRouter routing with the demonstrated-unusable `mistral` and `venice` routes excluded. It recovered 63 of the 81 cells presented to it. Failure sidecars show upstream DeepInfra HTTP 429 `engine_overloaded` / shared-pool rate limits for unresolved cells. These are transport/provider failures rather than valid behavioral trajectories.

The accepted 3,222-cell matrix is now fixed with strict source priority.

## Amendment

Only the 18 cells absent from the fixed 3,222-cell matrix may be attempted. For those keys only, OpenRouter provider routing may use the ordered provider list `deepinfra`, then `venice`, with fallbacks enabled, `require_parameters=true`, and the ineligible pinned official-Mistral route excluded.

This re-admits Venice only as a fallback serving route. Venice was the original planned Mistral provider. No previously accepted cell may be replaced.

The exact model remains `mistralai/mistral-small-3.2-24b-instruct`. Prompts, system instructions, tools, tool choice, temperature, response limit, task, condition, environment, replicate identifiers, scoring, hypotheses, and analysis definitions remain unchanged.

## Retry and acceptance policy

- Retries are allowed only for HTTP/transport failure, malformed JSON, or successful envelopes without a non-empty `choices` list.
- A cell that exhausts retries is logged to a failure sidecar and the runner continues.
- No retry or acceptance decision can depend on behavioral content, score, safety outcome, or task completion.
- A residual success can fill only an expected key absent from the fixed 3,222-cell matrix.
- Row-level routing metadata and the actual selected provider are retained.

## Completion rule

Primary behavioral analysis remains prohibited unless the assembled primary matrix contains exactly 3,240 unique expected cells and zero missing cells.
