# Construct validation without external expert review

SafeguardShift V2 is explicitly a **controlled synthetic benchmark**. It does not claim that its action contracts constitute complete real-world crisis doctrine, and it does not claim external domain-expert certification.

Because independent human expert review is not available for this study, the pre-canonical validation gate uses a frozen **Triangulated Synthetic Construct Validation** regime instead of fabricated or author-supplied expert approvals.

The gate has four layers.

1. **Deterministic structural validation.** The dataset verifier checks the exact 6 × 6 × 2 balance, causal separation of relevant and irrelevant safeguards, condition construction, and action-contract invariants.
2. **Executable oracle validation.** A deterministic oracle executes all 360 task-condition cells and verifies that relevant ablation blocks the safeguard-dependent action, irrelevant ablation does not, and the named substitute restores the missing function and unlocks the intended safe utility.
3. **Three-model blinded construct panel.** GPT-5.4, Claude Sonnet 5, and Gemini 2.5 Flash Lite independently assess all 72 task specifications before canonical model outcomes exist. For each task they evaluate relevant-safeguard relevance, negative-control validity, substitute-function coherence, domain action plausibility, matched-condition equivalence, directional utility ordering, and obvious answer-cue leakage. Every criterion must receive at least two of three positive votes.
4. **Corruption controls.** The same validators receive 12 balanced, deliberately corrupted task specifications without being told which criterion was corrupted. Majority rejection is required for every corrupted item, and every judge must detect at least eight of twelve controls.

The validation panel is frozen in `v2/configs/validation_panel_v2.json`. Raw validator outputs are retained separately from the canonical experiment. `scripts_v2/check_construct_validation.py` prevents canonical collection if the validation result is missing, fails, or is stale relative to the current V2 freeze manifest.

## Claim boundary

Passing this gate supports **internal construct coherence** for a synthetic causal benchmark. It does not establish ecological validity, domain completeness, legal correctness, clinical correctness, operational doctrine, or expert consensus. Those remain explicit limitations and possible future validation work.

The validators never score canonical model trajectories and therefore cannot directly determine the study's primary outcomes.
