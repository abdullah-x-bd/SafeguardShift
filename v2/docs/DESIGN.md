# Study 2 design

SafeguardShift V2 is a balanced 6 × 6 factorial diagnostic.

Six domains:
public health, critical infrastructure, cyber incident response, disaster response, public governance, crisis communication.

Six relevant safeguards:
verification, expert review, monitoring, reversibility, authority, execution capacity.

Two independent scenarios are instantiated for each domain × safeguard cell, giving 72 base tasks. Every task has five matched conditions: full, relevant ablation, irrelevant ablation, substitute, and compound ablation.

Each task contains domain-specific public action labels while actions are mapped to a hidden common ontology for cross-domain analysis. The substitute condition explicitly restores the relevant safeguard and unlocks a pre-specified higher-utility safe target action. An executable oracle verifies that this mechanism works for every task before model collection.

The four-model backbone runs three independent trajectories per model-task-condition cell: 72 × 5 × 4 × 3 = 4,320 trajectories. Two frontier diagnostic models are evaluated once on a balanced 12-task subset, one task per domain × selected safeguard allocation, for 120 diagnostic trajectories.

Study 1 is immutable and remains at archive/v1.0.0-canonical.
