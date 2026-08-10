# Reproducibility

Zero-cost verification:

```bash
python -m pip install -e .
crisisbench verify
pytest
crisisbench freeze
```

Canonical collection additionally requires:

```bash
export OPENROUTER_API_KEY=...
python scripts/preflight.py
python scripts/run_canonical.py --max-cost 7.0
```

Paid calls are never triggered by push or pull request CI. The canonical workflow is `workflow_dispatch` only. Raw accepted trajectories should be archived unchanged as a release asset before publication claims are frozen.
