# Agent environment

CrisisBench v1 is a bounded synthetic tool environment. Models cannot access real systems, live networks, or external tools. Five standardized tools expose inspection, capacity checks, action attempts, substitute activation, and terminal-plan submission.

Action attempts are checked against hidden evaluator-side contracts. Missing safeguards block execution but remain visible in the trajectory as attempted behavior. This lets CrisisBench measure unsafe intent, phantom-capacity reliance, and recovery without allowing real-world harmful action.
