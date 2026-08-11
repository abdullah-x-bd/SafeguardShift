# Amendment 007: Attempted official-Mistral transport substitution

Date: 2026-08-11

## Trigger

After amendment 006, the fixed primary baseline contained 2,972 of 3,240 planned cells. All 268 missing cells belonged to `mistralai/mistral-small-3.2-24b-instruct`. The preregistered Venice route repeatedly returned HTTP-success responses without a non-empty `choices` field. Identical-request transport retries did not resolve this failure mode for those cells.

## Attempt

A residual-only recovery was prospectively prepared to send only the 268 absent keys to OpenRouter's provider slug `mistral` while keeping the same model slug, prompts, tools, temperature, tasks, conditions, scoring, hypotheses, and replicate identifiers. The fixed 2,972-cell baseline retained strict source priority.

## Outcome

The attempt produced no accepted provider-substitution rows. OpenRouter returned HTTP 404 `No endpoints found for mistralai/mistral-small-3.2-24b-instruct` for the pinned official-Mistral tool-calling requests. Therefore no cell from this attempt enters the primary matrix and no already accepted cell was changed.

This failed transport attempt occurred before final behavioral analysis and without reference to behavioral scores.

## Consequence

Amendment 008 supersedes this attempted route and permits tool-aware provider-flexible recovery for only the still-missing keys. The primary completion rule remains exactly 3,240 unique expected cells with zero missing cells before behavioral analysis.
