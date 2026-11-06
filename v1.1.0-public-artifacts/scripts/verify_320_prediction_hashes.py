#!/usr/bin/env python3
"""Verify locally held private NPZ files against the corrected public manifest."""
import argparse,csv,hashlib,sys
from pathlib import Path
p=argparse.ArgumentParser()
p.add_argument('--private',type=Path,required=True,help='Unpacked private_predictions directory')
p.add_argument('--manifest',type=Path,default=Path(__file__).parent/'supplementary/P3_OBS2_private_prediction_artifact_manifest_320.csv')
a=p.parse_args()
rows=list(csv.DictReader(a.manifest.open(newline=''))); errors=[]
for row in rows:
    f=a.private/row['file_name']
    if not f.is_file(): errors.append(f'MISSING {f.name}');continue
    if f.stat().st_size!=int(row['size_bytes']):errors.append(f'SIZE {f.name}')
    if hashlib.sha256(f.read_bytes()).hexdigest()!=row['sha256']:errors.append(f'HASH {f.name}')
print(f'Checked {len(rows)} expected NPZ files: {len(rows)-len(set(e.split(" ",1)[1] for e in errors))} valid, {len(errors)} errors')
for e in errors: print(e)
sys.exit(bool(errors))
