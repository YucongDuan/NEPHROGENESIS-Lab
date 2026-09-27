#!/usr/bin/env python3
"""Create a new release inventory after review; never use this to hide a mismatch.

The manifest is an integrity inventory, not an external signature. Recreating it
makes a new release claim and cannot authenticate historical artifacts.
"""
from pathlib import Path
import argparse
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]
EXCLUDED_DIRS = {".git", "__pycache__", ".pytest_cache", "build", "runs", ".venv"}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--confirm-new-inventory", action="store_true", required=True)
    parser.parse_args()
    files = {}
    for path in sorted(ROOT.rglob("*")):
        rel = path.relative_to(ROOT)
        if any(p in EXCLUDED_DIRS or p.endswith(".egg-info") for p in rel.parts):
            continue
        if path.is_symlink():
            raise SystemExit(f"Symlinks are not release files: {rel}")
        if not path.is_file() or rel.as_posix() == "RELEASE_MANIFEST.json" or path.suffix == ".pyc" or path.name == ".coverage":
            continue
        files[rel.as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
    payload = {"format": "nephrogenesis-source-release-v1", "version": "1.0.0", "algorithm": "SHA-256", "files": files,
               "scope": "Integrity relative to this inventory; no authorship signature or external attestation."}
    (ROOT / "RELEASE_MANIFEST.json").write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"inventory_files": len(files), "path": str(ROOT / "RELEASE_MANIFEST.json")}, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
