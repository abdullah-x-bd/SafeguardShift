# CrisisBench v1 protocol

The confirmatory dataset contains 36 base tasks across six domains. Each task is rendered in five conditions: full safeguards, relevant ablation, irrelevant ablation, substitute, and compound ablation. The base task is invariant across conditions; only machine-readable safeguard state is changed.

The canonical agent receives the same system policy and tool schemas in every cell. It may take at most eight sequential tool turns. Parallel tool calls are disabled. The environment, not an LLM judge, determines whether actions are executable under the frozen action contracts.

Primary analysis is paired within base task and model. Repeated trajectories, if later added, remain repeated measures and do not inflate the base-task sample size.

Canonical collection is manual-only and requires `OPENROUTER_API_KEY`. Provider fallback is disabled. Any model/provider incompatibility discovered at preflight is an amendment trigger and must be documented before results are inspected.
