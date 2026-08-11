# Amendment 008: Tool-aware provider-flexible Mistral residual routing

Date: 2026-08-11

## Trigger

The fixed primary baseline remains 2,972 of 3,240 expected cells, with all 268 absent keys belonging to `mistralai/mistral-small-3.2-24b-instruct`. Venice repeatedly returned HTTP-success responses without usable `choices`, including after identical-request retries. The attempted pinned official-Mistral route in amendment 007 returned no eligible endpoint for the tool-calling request and produced no accepted rows.

## Amendment

Only the 268 keys absent from the fixed 2,972-cell baseline may be recovered using OpenRouter provider-flexible routing for the exact same model slug `mistralai/mistral-small-3.2-24b-instruct`.

The residual requests:

- keep the exact model slug, messages, system prompt, tool definitions, tool choice, temperature, generation limit, environment, replicate identifier, and scoring logic;
- set `provider.require_parameters=true` so routing is limited to endpoints that support the supplied request parameters;
- exclude the two routes already demonstrated unusable for these residual requests, `venice` and `mistral`;
- permit OpenRouter fallback routing among the remaining eligible providers;
- opt in to OpenRouter routing metadata and preserve it in trajectory provenance;
- retry only transport-level failures, malformed JSON, or successful envelopes without non-empty `choices`;
- never retry, replace, or select a row based on its behavioral content or score.

## Acceptance policy

The 2,972-cell baseline has strict priority. Residual rows may fill only keys that are absent from that baseline. If multiple residual attempts produce the same expected key, first valid source-priority acceptance applies and later duplicates are excluded outcome-blind.

No previously accepted trajectory may be replaced.

## Unchanged scientific definitions

No change is made to:

- the 72-task manifest;
- the five experimental conditions;
- the Mistral model identifier;
- prompts or agent instructions;
- tool schemas or environment transitions;
- temperature or response-token limit;
- hypotheses;
- scoring;
- primary metrics or inference definitions;
- replicate identifiers;
- frontier diagnostic.

## Claim boundary

Serving provider is an operational factor and is retained in row-level routing metadata. The paper must disclose that the Mistral primary matrix combines the previously accepted pinned-Venice trajectories with residual trajectories served through tool-aware OpenRouter routing. Provider sensitivity is therefore an explicit limitation, not hidden as if all Mistral trajectories used a single endpoint.

DeepSeek remains outside the pooled primary behavioral estimand under amendment 005 and remains a provider/interface reliability diagnostic.

## Completion rule

Behavioral analysis is permitted only if the final primary matrix contains exactly 3,240 unique expected cells and zero missing cells. Otherwise the run remains incomplete.
