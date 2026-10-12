from pathlib import Path
import sys,time,numpy as np,pandas as pd
from xgboost import XGBClassifier
from sklearn.metrics import balanced_accuracy_score,matthews_corrcoef,roc_auc_score,confusion_matrix
BASE=Path('/mnt/data/obs41_base/CrossDataset_Experiment_Package_v2/harmonized_data');OUT=Path('/mnt/data/obs41_work/results/balance');OUT.mkdir(parents=True,exist_ok=True)
DS=['UNSW_NB15','CICIDS2017','BoT_IoT','TON_IoT'];SEEDS=[42,52,62,72,82];source=sys.argv[1];D={}
for d in DS:
 z=np.load(BASE/f'{d}.npz');D[d]={k:z[k] for k in ['X_train','y_train','X_test','y_test']}
X0,y0=D[source]['X_train'],D[source]['y_train'];nmin=min((y0==0).sum(),(y0==1).sum());nbal=2*nmin;rows=[]
for seed in SEEDS:
 rng=np.random.default_rng(seed);ids0=np.flatnonzero(y0==0);ids1=np.flatnonzero(y0==1);bal=np.r_[rng.choice(ids0,nmin,replace=False),rng.choice(ids1,nmin,replace=False)];rng.shuffle(bal)
 match=rng.choice(np.arange(len(y0)),nbal,replace=False) if nbal<len(y0) else np.arange(len(y0))
 schemes=[('full_unweighted',np.arange(len(y0)),None),('full_class_weighted',np.arange(len(y0)),(y0==0).sum()/(y0==1).sum()),('random_undersample',bal,None),('prevalence_preserving_size_match',match,None)]
 for scheme,idx,spw in schemes:
  kw=dict(n_estimators=100,random_state=seed,eval_metric='logloss',n_jobs=5,tree_method='hist',verbosity=0)
  if spw is not None:kw['scale_pos_weight']=float(spw)
  m=XGBClassifier(**kw);t=time.perf_counter();m.fit(X0[idx],y0[idx]);fit=time.perf_counter()-t
  for target in DS:
   X,y=D[target]['X_test'],D[target]['y_test'];s=m.predict_proba(X)[:,1];p=(s>=.5).astype(np.uint8);tn,fp,fn,tp=confusion_matrix(y,p,labels=[0,1]).ravel()
   rows.append(dict(source=source,target=target,seed=seed,scheme=scheme,n_train=len(idx),train_attack_prev=float(y0[idx].mean()),ba=balanced_accuracy_score(y,p),mcc=matthews_corrcoef(y,p),auc=roc_auc_score(y,s),fpr=fp/(fp+tn),tpr=tp/(tp+fn),fit_seconds=fit))
pd.DataFrame(rows).to_csv(OUT/f'{source}_xgb_balance_controls.csv',index=False)
