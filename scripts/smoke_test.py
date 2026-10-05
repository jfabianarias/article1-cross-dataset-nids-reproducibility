"""Fast clean-start execution check for Supplementary Software S1.

This is deliberately small: it validates the packaged processed arrays and executes
all four model families on a deterministic stratified subset. It is not a substitute
for the full five-seed benchmark.
"""
from pathlib import Path
import json
import sys
import numpy as np
import pandas as pd
import sklearn
import xgboost
import scipy
import matplotlib
from PIL import Image
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import SGDClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import balanced_accuracy_score, matthews_corrcoef, confusion_matrix
from xgboost import XGBClassifier

ROOT = Path(__file__).resolve().parents[1]
CFG = json.loads((ROOT / "config" / "seeds.json").read_text())
SEED = int(CFG["model_seeds"][0])
DATASETS = ["UNSW_NB15", "CICIDS2017", "BoT_IoT", "TON_IoT"]

expected_versions = {
    "numpy": "2.3.5",
    "pandas": "2.2.3",
    "scikit-learn": "1.8.0",
    "xgboost": "3.1.3",
    "scipy": "1.17.0",
    "matplotlib": "3.10.8",
    "Pillow": "12.3.0",
}
actual_versions = {
    "numpy": np.__version__,
    "pandas": pd.__version__,
    "scikit-learn": sklearn.__version__,
    "xgboost": xgboost.__version__,
    "scipy": scipy.__version__,
    "matplotlib": matplotlib.__version__,
    "Pillow": Image.__version__,
}
for k, exp in expected_versions.items():
    got = actual_versions[k]
    if got != exp:
        raise SystemExit(f"Dependency mismatch: {k}={got}, expected {exp}")
print("Dependency versions: PASS")

for ds in DATASETS:
    z = np.load(ROOT / "processed_data" / f"{ds}.npz", allow_pickle=True)
    required = {"X_train", "y_train", "X_test", "y_test", "feature_names"}
    if not required.issubset(z.files):
        raise SystemExit(f"{ds}: missing arrays {sorted(required - set(z.files))}")
    if z["X_train"].shape[1] != 11 or z["X_test"].shape[1] != 11 or len(z["feature_names"]) != 11:
        raise SystemExit(f"{ds}: expected 11 harmonized features")
    if set(np.unique(z["y_train"])) != {0, 1} or set(np.unique(z["y_test"])) != {0, 1}:
        raise SystemExit(f"{ds}: labels are not binary 0/1")
print("Processed partitions: PASS")

z = np.load(ROOT / "processed_data" / "UNSW_NB15.npz", allow_pickle=True)
X, y = z["X_train"], z["y_train"]
Xt, yt = z["X_test"], z["y_test"]
rng = np.random.default_rng(SEED)

def stratified_indices(labels, n_per_class):
    idx = []
    for cls in (0, 1):
        ids = np.flatnonzero(labels == cls)
        idx.extend(rng.choice(ids, size=min(n_per_class, len(ids)), replace=False))
    idx = np.asarray(idx, dtype=int)
    rng.shuffle(idx)
    return idx

tr = stratified_indices(y, 1000)
te = stratified_indices(yt, 500)
models = {
    "Random Forest": RandomForestClassifier(n_estimators=10, random_state=SEED, n_jobs=1),
    "XGBoost": XGBClassifier(n_estimators=10, random_state=SEED, eval_metric="logloss", n_jobs=1, tree_method="hist"),
    "Linear SVM": Pipeline([("scale", StandardScaler()), ("model", SGDClassifier(loss="hinge", max_iter=100, tol=1e-3, random_state=SEED))]),
    "MLP": Pipeline([("scale", StandardScaler()), ("model", MLPClassifier(hidden_layer_sizes=(16,), max_iter=20, random_state=SEED, early_stopping=True, n_iter_no_change=3))]),
}
for name, model in models.items():
    model.fit(X[tr], y[tr])
    pred = model.predict(Xt[te])
    tn, fp, fn, tp = confusion_matrix(yt[te], pred, labels=[0, 1]).ravel()
    ba = balanced_accuracy_score(yt[te], pred)
    mcc = matthews_corrcoef(yt[te], pred)
    if not (np.isfinite(ba) and np.isfinite(mcc) and tn + fp + fn + tp == len(te)):
        raise SystemExit(f"{name}: invalid smoke-test metrics")
    print(f"{name}: PASS (BA={ba:.4f}, MCC={mcc:.4f})")

if CFG["model_seeds"] != [42, 52, 62, 72, 82]:
    raise SystemExit("Unexpected model seed policy")
if CFG["bootstrap_replicates"] != 10000:
    raise SystemExit("Unexpected bootstrap replicate count")
print("Seed/config policy: PASS")
print("SMOKE TEST PASSED")
