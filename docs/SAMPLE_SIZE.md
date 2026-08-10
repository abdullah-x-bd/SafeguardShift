# Sample-size rationale

CrisisBench v1 uses 36 base tasks, balanced as six tasks in each of six domains. The primary comparisons are paired within base task and model.

A simple design-level check treats each informative paired task as a directional Bernoulli comparison. With 36 independent base tasks, a two-sided alpha near 0.05 requires at least 25 of 36 informative pairs in the same direction under a 0.5 null. If the true directional probability is 0.75, exact-binomial power is approximately 0.833. This is not a substitute for endpoint-specific power under unknown discordance rates, but it establishes that the chosen base-task count is not arbitrary and has useful power for a strong, consistent paired effect.

The noncanonical pilot is used for tool reliability, cost, and floor/ceiling diagnostics. It is not used to change primary hypotheses after canonical outcomes are inspected.
