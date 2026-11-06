import numpy as np,pandas as pd
from pathlib import Path
R=Path('/mnt/data/NIDS_Obs2_Final_Integrity_20261105');pdir=R/'rebuild/private_predictions'
S=['UNSW_NB15','CICIDS2017','BoT_IoT','TON_IoT'];M=['Linear SVM','XGBoost','Random Forest','MLP'];SEEDS=[42,52,62,72,82];B=20000;rng=np.random.default_rng(20261105)
rows=[]
for src in S:
 for trg in S:
  if src==trg:continue
  for model in M:
   yy=None;pp=[]
   for seed in SEEDS:
    z=np.load(pdir/f'{src}__{model.replace(" ","_")}__s{seed}__{trg}.npz',allow_pickle=False)
    if yy is None:yy=z['y_true'];ii=z['target_test_index']
    assert np.array_equal(yy,z['y_true']) and np.array_equal(ii,z['target_test_index'])
    pp.append(z['y_pred'])
   k=np.stack(pp).sum(axis=0);h0=np.bincount(k[yy==0],minlength=6);h1=np.bincount(k[yy==1],minlength=6);n0=h0.sum();n1=h1.sum();v=np.arange(6)/5
   point=.5*(1-(h0@v)/n0+(h1@v)/n1)
   reps=.5*(1-(rng.multinomial(n0,h0/n0,size=B)@v)/n0+(rng.multinomial(n1,h1/n1,size=B)@v)/n1)
   q=np.quantile(reps,[.05/(2*48),.025,.975,1-.05/(2*48)])
   rows.append(dict(source=src,target=trg,model=model,BA=point,ci95_low=q[1],ci95_high=q[2],ci_bonf_low=q[0],ci_bonf_high=q[3],ci95_below_chance=q[2]<.5,bonf_below_chance=q[3]<.5,replicates=B))
D=pd.DataFrame(rows);D.to_csv(R/'bootstrap'/'48_external_model_five_seed_paired_bootstrap_20000.csv',index=False)
print('rows',len(D),'mean<50',sum(D.BA<.5),'95% entirely below',sum(D.ci95_below_chance),'Bonf entirely below',sum(D.bonf_below_chance));print(D.sort_values('BA').head(5).to_string(index=False))
