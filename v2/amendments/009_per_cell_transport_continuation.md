# Amendment 009: Per-cell continuation for final Mistral transport completion

Date: 2026-08-11

## Trigger

Tool-aware routing under amendment 008 recovered 187 of the 268 missing Mistral cells, raising the fixed primary baseline from 2,972 to 3,159 of 3,240 cells. The remaining 81 cells are all `mistralai/mistral-small-3.2-24b-instruct` and are concentrated in four domains because the residual shard runner aborted an entire domain after one cell exhausted transport retries.

## Amendment

The 3,159 accepted cells are fixed and have strict source priority. Only the 81 keys absent from that baseline may be attempted.

For these 81 cells, transport handling changes from shard-abort to per-cell continuation. If one cell exhausts transport retries, the runner records that exact key, error class, and routing events in a failure sidecar and continues to the next missing key. A failed cell produces no behavioral row and cannot enter analysis.

The request-level policy from amendment 008 is unchanged:

- exact model slug `mistralai/mistral-small-3.2-24b-instruct`;
- `provider.require_parameters=true`;
- fallbacks enabled;
- `venice` and `mistral` excluded because they were already demonstrated unusable for these residual tool-calling requests;
- OpenRouter routing metadata retained;
- retries restricted to transport errors, malformed JSON, or successful envelopes without non-empty `choices`;
- no retry or acceptance decision based on behavioral content or score.

## Scientific invariants

No task, condition, prompt, tool schema, environment transition, model identifier, temperature, generation limit, score, hypothesis, replicate identifier, or analysis definition changes.

No previously accepted row can be replaced. Residual successes may fill only absent expected keys.

## Completion rule

Behavioral analysis remains prohibited until the primary matrix contains exactly 3,240 unique expected cells with zero missing cells. Any cells still unresolved after this pass remain explicit transport failures rather than being silently dropped or imputed.
