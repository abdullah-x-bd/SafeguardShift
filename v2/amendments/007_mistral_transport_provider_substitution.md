# Amendment 007: Mistral transport provider substitution for residual completion

Date: 2026-08-11

## Trigger

After amendment 006, the fixed primary baseline contained 2,972 of 3,240 planned cells. All 268 missing cells belonged to `mistralai/mistral-small-3.2-24b-instruct`. The preregistered Venice route repeatedly returned HTTP-success responses without a non-empty `choices` field for some residual cells. Identical-request transport retries did not resolve this failure mode for those cells.

## Amendment

Only the 268 cells absent from the fixed 2,972-cell baseline may be recovered through OpenRouter's official Mistral provider while keeping the exact same model slug `mistralai/mistral-small-3.2-24b-instruct`.

No already accepted cell may be replaced. The 2,972-cell baseline has strict source priority. The provider-substitution rows can fill only absent expected keys.

The following remain unchanged:

- task manifest and task text
- five experimental conditions
- model identifier
- temperature and generation limits
- system prompt and tool definitions
- environment transitions
- scoring
- hypotheses
- analysis definitions
- replicate identifiers

The only changed execution field is the serving provider for still-missing Mistral cells, from `venice` to `mistral`.

## Rationale and claim boundary

This is a transport-completion amendment made before final behavioral analysis and without reference to behavioral scores. The same model weights/model slug are served by multiple OpenRouter providers. The substitution is used because the originally pinned route could not reliably return parseable tool-agent responses for a subset of planned cells.

Provider route is therefore retained in row-level provenance and the paper must disclose that Mistral's primary matrix combines previously accepted Venice-served cells with residual cells served by the official Mistral provider. Provider-sensitive analyses should treat serving route as a potential operational limitation.

DeepSeek remains excluded from the pooled primary behavioral estimand under amendment 005 and is preserved only as a provider/interface reliability diagnostic.

## Completion rule

The primary analysis remains gated on exactly 3,240 unique expected cells for GPT-4.1 Mini, Gemini 2.5 Flash Lite, and Mistral Small 3.2, with zero missing cells. No analysis is permitted if this gate fails.
