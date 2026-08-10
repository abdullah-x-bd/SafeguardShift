from __future__ import annotations
import hashlib
import zipfile
from pathlib import Path

EXCLUDE = {".env", ".git"}


def main() -> None:
    root = Path(".").resolve()
    out = root / "crisisbench-v1.0.0-research-artifact.zip"
    files = sorted(p for p in root.rglob("*") if p.is_file() and p != out and p.name != "RELEASE_SHA256.txt" and not any(part in EXCLUDE for part in p.parts) and "__pycache__" not in p.parts and ".pytest_cache" not in p.parts)
    with zipfile.ZipFile(out, "w", compression=zipfile.ZIP_DEFLATED) as z:
        for p in files:
            info = zipfile.ZipInfo(str(p.relative_to(root)), date_time=(2026, 8, 11, 0, 0, 0))
            info.external_attr = 0o644 << 16
            z.writestr(info, p.read_bytes())
    digest = hashlib.sha256(out.read_bytes()).hexdigest()
    (root / "RELEASE_SHA256.txt").write_text(f"{digest}  {out.name}\n", encoding="utf-8")
    print(digest, out.name)


if __name__ == "__main__":
    main()
