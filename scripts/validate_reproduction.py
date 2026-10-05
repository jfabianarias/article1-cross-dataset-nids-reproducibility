"""Compare fresh results/reproduced outputs with archived reference outputs.

Timing columns are ignored. Numerical comparisons tolerate small platform-level
floating point variation.
"""
from pathlib import Path
import pandas as pd
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
REP = ROOT / "results" / "reproduced"

def compare_csv(ref_rel, rep_rel, keys, numeric, atol=5e-4):
    ref = pd.read_csv(ROOT / ref_rel)
    rep = pd.read_csv(REP / rep_rel)
    a = ref[keys + numeric].sort_values(keys).reset_index(drop=True)
    b = rep[keys + numeric].sort_values(keys).reset_index(drop=True)
    if a[keys].astype(str).to_dict("records") != b[keys].astype(str).to_dict("records"):
        raise SystemExit(f"Key mismatch: {rep_rel}")
    for col in numeric:
        if not np.allclose(a[col].astype(float), b[col].astype(float), atol=atol, rtol=1e-5, equal_nan=True):
            mx = np.nanmax(np.abs(a[col].astype(float)-b[col].astype(float)))
            raise SystemExit(f"Numeric mismatch {rep_rel}:{col}, max abs diff={mx}")
    print(f"{rep_rel}: PASS")

compare_csv(
    "results/five_seed/five_seed_results.csv", "five_seed/five_seed_results.csv",
    ["source","target","model","seed","is_intra"],
    ["balanced_accuracy","mcc","f1","fpr","roc_auc","tn","fp","fn","tp"],
)
compare_csv(
    "results/lodo/lodo_summary.csv", "lodo/lodo_summary.csv",
    ["target","model"], ["ba_mean","ba_sd","mcc_mean","mcc_sd","fpr_mean","f1_mean"],
)
compare_csv(
    "results/balanced_training/balanced_five_seed_results.csv", "balanced_training/balanced_five_seed_results.csv",
    ["source","target","model","seed","is_intra"],
    ["balanced_accuracy","mcc","f1","fpr","roc_auc","tn","fp","fn","tp"],
)
print("REPRODUCTION VALIDATION PASSED")
