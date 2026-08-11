# Study 2 design

SafeguardShift V2 is a balanced 6 × 6 factorial diagnostic.

Six domains:
public health, critical infrastructure, cyber incident response, disaster response, public governance, crisis communication.

Six relevant safeguards:
verification, expert review, monitoring, reversibility, authority, execution capacity.

Two independent scenarios are instantiated for each domain × safeguard cell, giving 72 base tasks. Every task has five matched conditions: full, relevant ablation, irrelevant ablation, substitute, and compound ablation.

Each task contains domain-specific public action labels while actions are mapped to a hidden common ontology for cross-domain analysis. The substitute condition explicitly restores the relevant safeguard and unlocks a pre-specified higher-utility safe target action. An executable oracle verifies that this mechanism works for every task before model collection.

The original frozen design specified a four-model backbone with three independent trajectories per model-task-condition cell: 72 × 5 × 4 × 3 = 4,320 planned trajectories.

The original text also specified two frontier diagnostic models on a balanced 12-task subset for 120 diagnostic trajectories. **Before any V2 canonical agent trajectory was collected**, the documented "Final cue-neutrality and fixed-budget amendment" in `v2/docs/AMENDMENTS.md` prospectively reduced only this non-powered frontier diagnostic from 12 tasks / 120 trajectories to a balanced 6-task / 60-trajectory diagnostic. The primary backbone design was unchanged at that stage.

A later documented post-collection operational amendment, made before final behavioral analysis because of severe DeepSeek provider/interface attrition, restricted the complete-case primary behavioral estimand to the three backbone models with fully recoverable coverage. The final primary matrix therefore contains 3 × 72 × 5 × 3 = 3,240 complete trajectories. DeepSeek evidence is retained separately as a provider/interface reliability diagnostic. This note reconciles the original design with the prospective and operational amendments without rewriting the historical record.

Study 1 is immutable and remains at archive/v1.0.0-canonical.
