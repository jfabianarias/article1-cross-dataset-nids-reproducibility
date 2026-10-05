"""One-command runner for Supplementary Software S1."""
from pathlib import Path
import argparse
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"

def run(name):
    cmd = [sys.executable, str(SCRIPTS / name)]
    print("\n>>>", " ".join(cmd), flush=True)
    subprocess.run(cmd, cwd=ROOT, check=True)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["smoke", "full"], default="smoke")
    args = ap.parse_args()
    run("validate_release.py")
    run("smoke_test.py")
    if args.mode == "full":
        for script in [
            "run_five_seed_benchmark.py",
            "bootstrap_ci_final.py",
            "compute_normalized_metrics.py",
            "feature_stability_auc_check.py",
            "run_lodo_final.py",
            "run_coral_xgboost_with_parametric_ci.py",
            "run_class_balanced_sensitivity.py",
            "regenerate_submission_figures_obs24.py",
            "validate_reproduction.py",
        ]:
            run(script)
    print(f"\nRUN_ALL {args.mode.upper()} PASSED")

if __name__ == "__main__":
    main()
