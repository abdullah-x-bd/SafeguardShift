# Amendment 010: DeepInfra to Venice transport fallback for any final unresolved Mistral cells

Date: 2026-08-11

## Status

Prepared prospectively while amendment 009 is still running. This amendment is activated only if the amendment 009 finalizer reports a nonzero set of missing primary cells. If amendment 009 reaches 3,240/3,240, this amendment is not activated and no calls under it are made.

## Trigger condition

Amendment 009 uses tool-aware OpenRouter routing with the demonstrated-unusable `mistral` and `venice` routes excluded. Successful routed calls have been served by DeepInfra, but failure sidecars show upstream DeepInfra HTTP 429 `engine_overloaded` / shared-pool rate limits for some cells. Those are transport/provider failures rather than valid behavioral trajectories.

## Conditional amendment

Only cells still absent after the fixed amendment 009 assembly may be attempted. For those keys only, OpenRouter provider routing may use the ordered provider list `deepinfra`, then `venice`, with fallbacks enabled, `require_parameters=true`, and the ineligible pinned official-Mistral route excluded.

This re-admits Venice only as a fallback serving route. Venice was the original planned Mistral provider. The fixed accepted matrix from all prior stages retains strict priority and no accepted row can be replaced.

The exact model remains `mistralai/mistral-small-3.2-24b-instruct`. Prompts, system instructions, tools, tool choice, temperature, response limit, task, condition, environment, replicate identifiers, scoring, hypotheses, and analysis definitions remain unchanged.

## Retry and acceptance policy

- Retries are allowed only for HTTP/transport failure, malformed JSON, or successful envelopes without a non-empty `choices` list.
- A cell that exhausts retries is logged to a failure sidecar and the runner continues.
- No retry or acceptance decision can depend on behavioral content, score, safety outcome, or task completion.
- A residual success can fill only an expected key absent from the fixed prior matrix.
- Row-level routing metadata and the actual selected provider are retained.

## Completion rule

Primary behavioral analysis remains prohibited unless the assembled primary matrix contains exactly 3,240 unique expected cells and zero missing cells.
