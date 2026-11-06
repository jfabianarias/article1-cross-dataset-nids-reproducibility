#!/usr/bin/env python3
"""Validate the *current* public release candidate without requiring private NPZ files."""
from pathlib import Path
import argparse,csv,hashlib,sys
root=Path(__file__).resolve().parent
p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--root',type=Path,default=root)
p.add_argument('--manifest',default='SHA256_CURRENT_RELEASE.csv')
a=p.parse_args();base=a.root.resolve();manifest=base/a.manifest
if not manifest.is_file():sys.exit('MISSING current manifest: '+str(manifest))
rows=list(csv.DictReader(manifest.open(newline='',encoding='utf-8')))
errors=[];observed=set()
for row in rows:
    name=row['path'];f=(base/name).resolve()
    if name in observed:errors.append('DUPLICATE '+name);continue
    observed.add(name)
    if not f.is_relative_to(base) or not f.is_file():errors.append('MISSING/UNSAFE '+name);continue
    if f.stat().st_size!=int(row['size_bytes']):errors.append('SIZE '+name);continue
    if hashlib.file_digest(f.open('rb'),'sha256').hexdigest()!=row['sha256']:errors.append('SHA256 '+name)
# No private prediction archive/data allowed in public release.
for f in base.rglob('*'):
    if f.is_file() and f.suffix.lower() in {'.npz','.npy','.parquet','.pkl','.joblib','.pem','.key'}:
        errors.append('PRIVATE_OR_BINARY_REVIEW '+str(f.relative_to(base)))
    if f.is_file() and f.name not in {a.manifest} and str(f.relative_to(base)) not in observed:
        errors.append('UNLISTED '+str(f.relative_to(base)))
print(f'Current release candidate: {len(rows)} files checked; errors={len(errors)}')
for e in errors[:60]:print(e)
sys.exit(bool(errors))
