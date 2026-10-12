from pathlib import Path
import sys,time,numpy as np,pandas as pd
from xgboost import XGBClassifier
from sklearn.metrics import balanced_accuracy_score,roc_auc_score,matthews_corrcoef
BASE=Path('/mnt/data/obs41_base/CrossDataset_Experiment_Package_v2/harmonized_data');OUT=Path('/mnt/data/obs41_work/results/representation');OUT.mkdir(parents=True,exist_ok=True)
DS=['UNSW_NB15','CICIDS2017','BoT_IoT','TON_IoT'];SEEDS=[42,52,62,72,82];source=sys.argv[1];D={}
for d in DS:
 z=np.load(BASE/f'{d}.npz');D[d]={k:z[k] for k in ['X_train','y_train','X_test','y_test']}
def rep(X,kind):
 if kind=='full11':return X
 if kind=='base5':return X[:,:5]
 dur,sp,dp,sb,db=[np.expm1(np.clip(X[:,i],0,50)).astype(np.float64) for i in range(5)];tp=sp+dp;tb=sb+db;mean=np.divide(tb,tp,out=np.zeros_like(tb),where=tp>0);pps=np.divide(tp,dur,out=np.zeros_like(tp),where=dur>0);bps=np.divide(tb,dur,out=np.zeros_like(tb),where=dur>0);pbal=np.divide(np.abs(sp-dp),tp,out=np.zeros_like(tp),where=tp>0);bbal=np.divide(np.abs(sb-db),tb,out=np.zeros_like(tb),where=tb>0);R=np.column_stack([np.log1p(dur),np.log1p(tp),np.log1p(tb),np.log1p(mean),np.log1p(pps),np.log1p(bps),pbal,bbal]).astype(np.float32);R[~np.isfinite(R)]=0;return R
rows=[]
for kind in ['base5','full11','direction_invariant8']:
 Xtr=rep(D[source]['X_train'],kind);ytr=D[source]['y_train']
 for seed in SEEDS:
  m=XGBClassifier(n_estimators=100,random_state=seed,eval_metric='logloss',n_jobs=5,tree_method='hist',verbosity=0);t=time.perf_counter();m.fit(Xtr,ytr);fit=time.perf_counter()-t
  for target in DS:
   X=rep(D[target]['X_test'],kind);y=D[target]['y_test'];s=m.predict_proba(X)[:,1];p=(s>=.5).astype(np.uint8);rows.append(dict(source=source,target=target,representation=kind,seed=seed,ba=balanced_accuracy_score(y,p),auc=roc_auc_score(y,s),mcc=matthews_corrcoef(y,p),fit_seconds=fit))
pd.DataFrame(rows).to_csv(OUT/f'{source}_representation_xgb.csv',index=False)
