from pathlib import Path
import sys,time,warnings,json
import numpy as np,pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import SGDClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import balanced_accuracy_score,roc_auc_score
from sklearn.exceptions import ConvergenceWarning
from xgboost import XGBClassifier
BASE=Path('/mnt/data/obs41_base/CrossDataset_Experiment_Package_v2/harmonized_data');OUT=Path('/mnt/data/obs41_work/results/model_selection');OUT.mkdir(parents=True,exist_ok=True)
source=sys.argv[1];seed=42;z=np.load(BASE/f'{source}.npz');X=z['X_train'];y=z['y_train']
if len(y)>75000:
 rng=np.random.default_rng(seed);idx=[]
 for c in [0,1]:
  ids=np.flatnonzero(y==c);k=max(1,round(75000*len(ids)/len(y)));idx.extend(rng.choice(ids,min(k,len(ids)),replace=False))
 idx=np.array(idx)
 if len(idx)>75000:idx=rng.choice(idx,75000,replace=False)
 elif len(idx)<75000:
  rest=np.setdiff1d(np.arange(len(y)),idx);idx=np.r_[idx,rng.choice(rest,75000-len(idx),replace=False)]
 X,y=X[idx],y[idx]
Xtr,Xv,ytr,yv=train_test_split(X,y,test_size=.2,random_state=seed,stratify=y)
C={'Random Forest':[{'n_estimators':100,'max_depth':None,'min_samples_leaf':1},{'n_estimators':100,'max_depth':12,'min_samples_leaf':1},{'n_estimators':100,'max_depth':None,'min_samples_leaf':5},{'n_estimators':100,'max_depth':12,'min_samples_leaf':5}],
'XGBoost':[{'n_estimators':100,'max_depth':3,'learning_rate':.1},{'n_estimators':100,'max_depth':6,'learning_rate':.1},{'n_estimators':150,'max_depth':3,'learning_rate':.05},{'n_estimators':150,'max_depth':6,'learning_rate':.05}],
'Linear SVM':[{'alpha':1e-3,'average':True},{'alpha':1e-4,'average':True},{'alpha':1e-5,'average':True},{'alpha':1e-4,'average':False}],
'MLP':[{'hidden_layer_sizes':(100,),'early_stopping':True,'n_iter_no_change':3,'max_iter':100},{'hidden_layer_sizes':(100,),'early_stopping':True,'n_iter_no_change':10,'max_iter':150},{'hidden_layer_sizes':(100,),'early_stopping':False,'n_iter_no_change':10,'max_iter':150},{'hidden_layer_sizes':(50,),'early_stopping':False,'n_iter_no_change':10,'max_iter':150}]}
rows=[]
for fam,cands in C.items():
 for ci,p in enumerate(cands,1):
  if fam=='Random Forest':m=RandomForestClassifier(random_state=seed,n_jobs=5,**p)
  elif fam=='XGBoost':m=XGBClassifier(random_state=seed,n_jobs=5,tree_method='hist',eval_metric='logloss',verbosity=0,**p)
  elif fam=='Linear SVM':m=Pipeline([('scale',StandardScaler()),('model',SGDClassifier(loss='hinge',max_iter=2000,tol=1e-3,random_state=seed,n_jobs=5,**p))])
  else:m=Pipeline([('scale',StandardScaler()),('model',MLPClassifier(random_state=seed,validation_fraction=.1,tol=1e-3,batch_size=4096,**p))])
  t=time.perf_counter()
  with warnings.catch_warnings(record=True) as ws:warnings.simplefilter('always');m.fit(Xtr,ytr)
  fit=time.perf_counter()-t;pred=m.predict(Xv)
  try:s=m.predict_proba(Xv)[:,1]
  except Exception:s=m.decision_function(Xv)
  nit=np.nan;loss='';internal=''
  if fam=='MLP':
   mm=m.named_steps['model'];nit=int(mm.n_iter_);loss=json.dumps([float(q) for q in mm.loss_curve_]);internal=json.dumps([float(q) for q in (getattr(mm,'validation_scores_',None) or [])])
  rows.append(dict(source=source,family=fam,candidate=ci,params=json.dumps(p),n_search_total=len(y),n_train=len(ytr),n_val=len(yv),val_balanced_accuracy=balanced_accuracy_score(yv,pred),val_auc=roc_auc_score(yv,s),fit_seconds=fit,n_iter=nit,convergence_warning=any(issubclass(w.category,ConvergenceWarning) for w in ws),loss_curve=loss,internal_validation_scores=internal))
df=pd.DataFrame(rows);df['selected']=False
for fam,g in df.groupby('family'):df.loc[g.val_balanced_accuracy.idxmax(),'selected']=True
df.to_csv(OUT/f'{source}_source_validation_search.csv',index=False)
