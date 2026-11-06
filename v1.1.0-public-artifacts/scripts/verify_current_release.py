#!/usr/bin/env python3
"""Verify the public v1.1.0 artifacts against SHA256SUMS.txt; no private data needed."""
from pathlib import Path
import argparse
import hashlib
import sys

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
args = parser.parse_args()
root = args.root.resolve()
manifest = root / 'SHA256SUMS.txt'
if not manifest.is_file():
    sys.exit(f'MISSING {manifest}')
errors = []
listed = set()
for line_number, line in enumerate(manifest.read_text(encoding='utf-8').splitlines(), 1):
    try:
        digest, relpath = line.split('  ', 1)
        assert len(digest) == 64 and all(c in '0123456789abcdef' for c in digest)
        f = (root / relpath).resolve()
        assert f.is_relative_to(root) and relpath not in listed
        listed.add(relpath)
        assert f.is_file()
        with f.open('rb') as stream:
            actual = hashlib.file_digest(stream, 'sha256').hexdigest()
        if actual != digest:
            errors.append(f'HASH MISMATCH {relpath}')
    except (AssertionError, ValueError, OSError):
        errors.append(f'MALFORMED OR MISSING entry at line {line_number}: {line!r}')
for f in root.rglob('*'):
    if not f.is_file():
        continue
    rel = f.relative_to(root).as_posix()
    if f.suffix.lower() in {'.npz', '.npy', '.parquet', '.pkl', '.joblib', '.pem', '.key'}:
        errors.append(f'PRIVATE/BINARY REVIEW {rel}')
    if rel not in listed and rel != 'SHA256SUMS.txt':
        errors.append(f'UNLISTED {rel}')
print(f'Public release validation: {len(listed)} files checked; errors={len(errors)}')
for error in errors[:50]:
    print(error)
sys.exit(bool(errors))
