#!/usr/bin/env python3
"""Verify SHA-256 release inventory. Run this from an extracted source release."""
from pathlib import Path
import hashlib
import json
import sys
ROOT=Path(__file__).resolve().parents[1]
def main():
    manifest=ROOT/'RELEASE_MANIFEST.json'
    if not manifest.is_file():
        print('No release manifest: this may be a development checkout.');return 2
    data=json.loads(manifest.read_text())
    failures=[]
    for name,expected in data['files'].items():
        p=ROOT/name
        if p.is_symlink() or not p.resolve().is_relative_to(ROOT.resolve()):
            failures.append(name+' (unsafe path)');continue
        if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=expected:failures.append(name)
    print(json.dumps({'passed':not failures,'checked_files':len(data['files']),'failures':failures,
                      'note':'Inventory integrity is relative to the preserved manifest, not an authenticity signature.'},indent=2))
    return 1 if failures else 0
if __name__=='__main__':raise SystemExit(main())
