import json
from pathlib import Path
from safeguardshift.freeze import build
committed=json.loads(Path("v2/FREEZE_MANIFEST.json").read_text())
current=build()
for key in ("protocol","frozen_on","v1_parent_commit"):
    assert committed[key]==current[key],(key,committed[key],current[key])
assert committed["files"]==current["files"],{"committed":committed["files"],"current":current["files"]}
print({"status":"PASS","files":len(current["files"])})
