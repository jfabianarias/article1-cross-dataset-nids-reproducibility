from pathlib import Path
import csv
import hashlib
import json
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
checks = []

def ok(name, cond, detail=""):
    checks.append((name, bool(cond), detail))
    print(f"{name}: {'PASS' if cond else 'FAIL'}{(' - ' + detail) if detail else ''}")

required = [
    "README.md", "requirements.txt", "python_version.txt", "CITATION.cff",
    "config/seeds.json", "MANIFEST_SHA256.csv",
    "scripts/run_all.py", "scripts/smoke_test.py", "scripts/validate_reproduction.py",
    "processed_data/UNSW_NB15.npz", "processed_data/CICIDS2017.npz",
    "processed_data/BoT_IoT.npz", "processed_data/TON_IoT.npz",
    "results/five_seed/five_seed_results.csv", "results/bootstrap/bootstrap_summary.json",
    "results/coral/coral_summary.json", "results/balanced_training/balanced_summary.json",
]
ok("required_files", all((ROOT/p).exists() for p in required))

cfg = json.loads((ROOT/"config/seeds.json").read_text())
ok("model_seeds", cfg.get("model_seeds") == [42,52,62,72,82])
ok("bootstrap_seed", cfg.get("direct_transfer_bootstrap_seed") == 20261004)
ok("coral_bootstrap_seed", cfg.get("coral_bootstrap_seed") == 20261005)
ok("bootstrap_replicates", cfg.get("bootstrap_replicates") == 10000)
ok("lodo_cap", cfg.get("lodo_per_source_cap") == 25000)
ok("coral_epsilon", abs(float(cfg.get("coral_regularization_epsilon", -1)) - 1e-3) < 1e-15)

def close(a,b,tol=5e-4): return abs(float(a)-float(b)) <= tol
over = pd.read_csv(ROOT/'results/five_seed/overall_five_seed_summary.csv').set_index('metric')
ok('intra_ba', close(over.loc['intra_ba','mean'],0.853967))
ok('cross_ba', close(over.loc['cross_ba','mean'],0.476333))
ok('cross_mcc', close(over.loc['cross_mcc','mean'],-0.056217))
bs = json.loads((ROOT/'results/bootstrap/bootstrap_summary.json').read_text())
ok('below_chance', bs['mean_ba_lt_0_5']==28)
ok('ci_below', bs['ci_entirely_below_0_5']==25)
cs = json.loads((ROOT/'results/coral/coral_summary.json').read_text())
ok('coral_ba', close(cs['coral_ba_mean'],0.541766))
ok('coral_improved', cs['directions_improved']==8)
norm = json.loads((ROOT/'results/normalized/collapse_sensitivity.json').read_text())
ok('intra_excl_bot_mlp', close(norm['overall_intra_excl_bot_mlp_mean'],0.877565))
bal = json.loads((ROOT/'results/balanced_training/balanced_summary.json').read_text())
ok('balanced_cross_ba', close(bal['balanced_cross_ba_mean'],0.479458))
ok('balanced_cross_mcc', close(bal['balanced_cross_mcc_mean'],-0.074507))
ok('balanced_cells', bal['directions_total']==48)
audit = pd.read_csv(ROOT/'audits/five_seed_compliance_audit.csv')
ok('five_seed_all', bool(audit['passes_five_seed_requirement'].all()))

manifest = ROOT / 'MANIFEST_SHA256.csv'
manifest_ok = True
manifest_detail = []
if manifest.exists():
    with manifest.open(newline='', encoding='utf-8') as f:
        for row in csv.DictReader(f):
            p = ROOT / row['path']
            if not p.exists():
                manifest_ok=False; manifest_detail.append(f"missing:{row['path']}"); continue
            size = p.stat().st_size
            h = hashlib.sha256(p.read_bytes()).hexdigest()
            if size != int(row['size_bytes']) or h != row['sha256']:
                manifest_ok=False; manifest_detail.append(f"mismatch:{row['path']}")
ok('sha256_manifest', manifest_ok, ', '.join(manifest_detail[:3]))

if not all(x[1] for x in checks):
    raise SystemExit('VALIDATION FAILED')
print('VALIDATION PASSED')
