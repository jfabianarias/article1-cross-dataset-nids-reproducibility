from pathlib import Path
import sys,numpy as np,pandas as pd
from xgboost import XGBClassifier
from sklearn.metrics import balanced_accuracy_score,roc_auc_score,matthews_corrcoef,confusion_matrix
BASE=Path('/mnt/data/obs41_base/CrossDataset_Experiment_Package_v2/harmonized_data');OUT=Path('/mnt/data/obs41_work/results/coral_inductive');OUT.mkdir(parents=True,exist_ok=True)
DS=['UNSW_NB15','CICIDS2017','BoT_IoT','TON_IoT'];SEEDS=[42,52,62,72,82];src=sys.argv[1];only_tgt=(sys.argv[2] if len(sys.argv)>2 else None);D={}
for d in DS:
 z=np.load(BASE/f'{d}.npz');D[d]={k:z[k].astype(np.float64 if k.startswith('X') else np.uint8) for k in ['X_train','y_train','X_test','y_test']}
def sqrtm(C,p):
 w,V=np.linalg.eigh(C);w=np.clip(w,1e-10,None);return (V*(w**p))@V.T
def transform(Xs,Xa,reg,scaling):
 Xs=Xs.copy();Xa=Xa.copy();params=None
 if scaling=='source_std':
  mu=Xs.mean(0);sd=Xs.std(0);sd[sd<1e-9]=1;Xs=(Xs-mu)/sd;Xa=(Xa-mu)/sd;params=(mu,sd)
 ms=Xs.mean(0);mt=Xa.mean(0);Cs=np.cov(Xs,rowvar=False,ddof=1)+reg*np.eye(Xs.shape[1]);Ct=np.cov(Xa,rowvar=False,ddof=1)+reg*np.eye(Xa.shape[1]);A=sqrtm(Cs,-.5)@sqrtm(Ct,.5);return ((Xs-ms)@A+mt).astype(np.float32),params
def eval_one(tgt,reg,scaling,seed,mode):
 Xs,ys=D[src]['X_train'],D[src]['y_train'];Xt,yt=D[tgt]['X_test'],D[tgt]['y_test'];idx=np.random.default_rng(314159).permutation(len(yt));na=max(1,int(.30*len(idx)));ia,ie=idx[:na],idx[na:];Xa=Xt[ia];Xe=Xt[ie];Xc,params=transform(Xs,Xa,reg,scaling)
 if params is not None:mu,sd=params;Xe=(Xe-mu)/sd
 m=XGBClassifier(n_estimators=100,random_state=seed,eval_metric='logloss',n_jobs=5,tree_method='hist',verbosity=0);m.fit(Xc,ys);s=m.predict_proba(Xe.astype(np.float32))[:,1];p=s>=.5;tn,fp,fn,tp=confusion_matrix(yt[ie],p,labels=[0,1]).ravel()
 return dict(source=src,target=tgt,mode=mode,adapt_fraction=.30,reg=reg,scaling=scaling,seed=seed,n_adapt=len(ia),n_eval=len(ie),ba=balanced_accuracy_score(yt[ie],p),auc=roc_auc_score(yt[ie],s),mcc=matthews_corrcoef(yt[ie],p),fpr=fp/(fp+tn),tpr=tp/(tp+fn))
rows=[]
for tgt in DS:
 if tgt==src or (only_tgt and tgt!=only_tgt):continue
 for seed in SEEDS:rows.append(eval_one(tgt,1e-3,'none',seed,'inductive_main'))
 for reg in [1e-5,1e-3,1e-1]:
  for scaling in ['none','source_std']:rows.append(eval_one(tgt,reg,scaling,42,'sensitivity'))
pd.DataFrame(rows).to_csv(OUT/f'{src}__{only_tgt or "ALL"}_coral_inductive.csv',index=False)
