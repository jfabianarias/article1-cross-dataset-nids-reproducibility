#!/usr/bin/env python3
"""Resumable source-only prediction reconstruction with count equality gate.
Never use target labels in training or model selection.  No publication of NPZs.
"""
import os
for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):os.environ[k]='1'
import argparse,sys,time,hashlib,resource,platform,json
from pathlib import Path
import pandas as pd,numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import SGDClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import confusion_matrix
from xgboost import XGBClassifier
DS=['UNSW_NB15','CICIDS2017','BoT_IoT','TON_IoT'];SEEDS=[42,52,62,72,82]

def make_model(m,s):
 if m=='Random Forest':return RandomForestClassifier(n_estimators=100,random_state=s,n_jobs=4)
 if m=='XGBoost':return XGBClassifier(n_estimators=100,random_state=s,eval_metric='logloss',n_jobs=1,tree_method='hist')
 if m=='Linear SVM':return Pipeline([('scale',StandardScaler()),('model',SGDClassifier(loss='hinge',alpha=1e-4,max_iter=2000,tol=1e-3,random_state=s,average=True))])
 if m=='MLP':return Pipeline([('scale',StandardScaler()),('model',MLPClassifier(hidden_layer_sizes=(100,),random_state=s,early_stopping=True,validation_fraction=.1,n_iter_no_change=3,tol=1e-3,max_iter=100,batch_size=4096))])
 raise ValueError(m)

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--data',type=Path,required=True);ap.add_argument('--archive',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--models',nargs='+',default=['Linear SVM','XGBoost','Random Forest','MLP']);ap.add_argument('--seeds',nargs='+',type=int,default=[52,62,72,82]);ap.add_argument('--sources',nargs='+',default=DS);a=ap.parse_args()
 a.out.mkdir(parents=True,exist_ok=True);pdir=a.out/'private_predictions';pdir.mkdir(exist_ok=True)
 ref=pd.read_csv(a.archive).set_index(['source','target','model','seed'])
 datasets={}
 for n in DS:
  with np.load(a.data/(n+'.npz'),allow_pickle=False) as z:datasets[n]={k:z[k] for k in ['X_train','X_test','y_train','y_test']}
 report=a.out/'rebuild_validation.csv'
 if report.exists():old=pd.read_csv(report);done=set(zip(old.source,old.model,old.seed))
 else:done=set()
 for m in a.models:
  for src in a.sources:
   for seed in a.seeds:
    if (src,m,seed) in done:continue
    start=time.time();clf=make_model(m,seed)
    clf.fit(datasets[src]['X_train'],datasets[src]['y_train'])
    fit=time.time()-start;arr=[]
    for target in DS:
     d=datasets[target];y=d['y_test'];x=d['X_test'];pred=clf.predict(x).astype(np.int8)
     score=clf.predict_proba(x)[:,1] if hasattr(clf,'predict_proba') else clf.decision_function(x)
     tn,fp,fn,tp=map(int,confusion_matrix(y,pred,labels=[0,1]).ravel())
     r=ref.loc[(src,target,m,seed)]
     exact=all(int(r[k])==v for k,v in zip(['tn','fp','fn','tp'],[tn,fp,fn,tp]))
     fname=f'{src}__{m.replace(" ","_")}__s{seed}__{target}.npz';f=pdir/fname
     np.savez_compressed(f,target_test_index=np.arange(len(y),dtype=np.int32),y_true=y.astype(np.int8),y_pred=pred,score=np.asarray(score,dtype=np.float32))
     arr.append(dict(source=src,target=target,model=m,seed=seed,tn=tn,fp=fp,fn=fn,tp=tp,exact_counts=exact,fit_seconds=fit,filename=fname,sha256=hashlib.sha256(f.read_bytes()).hexdigest(),n_test=len(y)))
    pd.DataFrame(arr).to_csv(report,mode='a',header=not report.exists(),index=False)
    print(f'{m} {src} seed{seed}: {sum(x["exact_counts"] for x in arr)}/4 EXACT, {fit:.2f}s',flush=True)
 summary=dict(checked=len(pd.read_csv(report)),count_exact=int(pd.read_csv(report).exact_counts.sum()),platform=platform.platform(),python=sys.version.split()[0],models=a.models,seeds=a.seeds,sources=a.sources)
 (a.out/'status.json').write_text(json.dumps(summary,indent=2))
if __name__=='__main__':main()
