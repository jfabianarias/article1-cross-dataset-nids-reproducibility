from pathlib import Path
import numpy as np,pandas as pd
from sklearn.metrics import roc_auc_score
BASE=Path('/mnt/data/obs41_base/CrossDataset_Experiment_Package_v2/harmonized_data');OUT=Path('/mnt/data/obs41_work/results/feature_stability');OUT.mkdir(parents=True,exist_ok=True)
DS=['UNSW_NB15','CICIDS2017','BoT_IoT','TON_IoT'];rows=[]
for ds in DS:
 z=np.load(BASE/f'{ds}.npz');X=np.vstack([z['X_train'],z['X_test']]);y=np.r_[z['y_train'],z['y_test']];n1=int(y.sum());n0=len(y)-n1
 for j,f in enumerate(z['feature_names']):
  a=float(roc_auc_score(y,X[:,j]));q1=a/(2-a);q2=2*a*a/(1+a);se=np.sqrt((a*(1-a)+(n1-1)*(q1-a*a)+(n0-1)*(q2-a*a))/(n0*n1));rows.append(dict(dataset=ds,feature=str(f),auc=a,ci_lo=max(0,a-1.96*se),ci_hi=min(1,a+1.96*se),n_benign=n0,n_attack=n1))
df=pd.DataFrame(rows);df.to_csv(OUT/'feature_by_dataset_auc_with_ci.csv',index=False);sens=[]
for t in [.05,.10,.15]:
 for feat,g in df.groupby('feature'):
  h=g[np.abs(g.auc-.5)>=t];sign=np.sign(h.auc-.5);sens.append(dict(threshold=t,feature=feat,n_meaningful=len(h),reversal=(len(h)>=2 and len(set(sign))>1),consistent_all_four=(len(h)==4 and len(set(sign))==1)))
pd.DataFrame(sens).to_csv(OUT/'auc_reversal_threshold_sensitivity.csv',index=False)
