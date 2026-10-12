from pathlib import Path
import sys,time,numpy as np,pandas as pd
from xgboost import XGBClassifier
from sklearn.metrics import balanced_accuracy_score,roc_auc_score,matthews_corrcoef
BASE=Path('/mnt/data/obs41_base/CrossDataset_Experiment_Package_v2/harmonized_data');OUT=Path('/mnt/data/obs41_work/results/lodo_budget');OUT.mkdir(parents=True,exist_ok=True)
DS=['UNSW_NB15','CICIDS2017','BoT_IoT','TON_IoT'];SEEDS=[42,52,62,72,82];target=sys.argv[1];B=75000;PER=25000;D={}
for d in DS:
 z=np.load(BASE/f'{d}.npz');D[d]={k:z[k] for k in ['X_train','y_train','X_test','y_test']}
def sample(X,y,n,seed):
 if len(y)<=n:return X,y,False
 rng=np.random.default_rng(seed);idx=rng.choice(len(y),n,replace=False);return X[idx],y[idx],True
def eval_cfg(name,Xtr,ytr,seed,meta):
 m=XGBClassifier(n_estimators=100,random_state=seed,eval_metric='logloss',n_jobs=5,tree_method='hist',verbosity=0);t=time.perf_counter();m.fit(Xtr,ytr);fit=time.perf_counter()-t;X,y=D[target]['X_test'],D[target]['y_test'];s=m.predict_proba(X)[:,1];p=(s>=.5).astype(np.uint8)
 return dict(target=target,config=name,seed=seed,n_train=len(ytr),train_attack_prev=float(ytr.mean()),ba=balanced_accuracy_score(y,p),auc=roc_auc_score(y,s),mcc=matthews_corrcoef(y,p),fit_seconds=fit,**meta)
rows=[];srcs=[d for d in DS if d!=target]
for seed in SEEDS:
 for j,s in enumerate(srcs):
  X,y,_=sample(D[s]['X_train'],D[s]['y_train'],B,seed+100*j);rows.append(eval_cfg('single_budget75k',X,y,seed,{'train_sources':s,'budget_exact':len(y)==B}))
 xs=[];ys=[]
 for j,s in enumerate(srcs):
  X,y,_=sample(D[s]['X_train'],D[s]['y_train'],PER,seed+200*j);xs.append(X);ys.append(y)
 X=np.vstack(xs);y=np.concatenate(ys);q=np.random.default_rng(seed).permutation(len(y));rows.append(eval_cfg('lodo_equal_domain25k',X[q],y[q],seed,{'train_sources':'+'.join(srcs),'budget_exact':len(y)==75000}))
 X=np.vstack([D[s]['X_train'] for s in srcs]);y=np.concatenate([D[s]['y_train'] for s in srcs]);q=np.random.default_rng(seed).permutation(len(y));rows.append(eval_cfg('full_pooled',X[q],y[q],seed,{'train_sources':'+'.join(srcs),'budget_exact':False}))
pd.DataFrame(rows).to_csv(OUT/f'{target}_xgb_lodo_budget.csv',index=False)
