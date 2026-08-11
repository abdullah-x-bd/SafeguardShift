# Independent expert validation gate

V2 does not self-certify domain realism.

Before canonical collection, each base task must receive at least two independent blind reviews from people with relevant domain or institutional decision experience. Reviewers assess:

1. whether the named relevant safeguard is genuinely relevant to the safeguard-dependent action;
2. whether the irrelevant safeguard is plausibly institutional but not causally required for the target action;
3. whether the substitute could realistically restore the missing function;
4. whether the action labels are understandable and domain-plausible;
5. whether the full/relevant/irrelevant/substitute variants preserve the same underlying task;
6. whether the frozen action utility ordering is directionally defensible.

The repository includes `v2/validation/expert_review_template.csv`. Canonical execution must not begin until `scripts_v2/validate_expert_reviews.py` passes.

This gate is intentionally external. Missing reviews must never be replaced by model-generated or author-generated approvals.
