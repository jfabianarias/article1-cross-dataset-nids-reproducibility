from pathlib import Path
import time,numpy as np,pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import SGDClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score,precision_score,recall_score,f1_score,roc_auc_score,balanced_accuracy_score,matthews_corrcoef,confusion_matrix
from xgboost import XGBClassifier
ROOT=Path(__file__).resolve().parents[1];DATA=ROOT/'processed_data';OUT=ROOT/'results'/'reproduced'/'five_seed';OUT.mkdir(parents=True,exist_ok=True)
DATASETS=['UNSW_NB15','CICIDS2017','BoT_IoT','TON_IoT'];SEEDS=[42,52,62,72,82];data={}
for ds in DATASETS:
 z=np.load(DATA/f'{ds}.npz',allow_pickle=True);data[ds]={k:z[k] for k in ['X_train','y_train','X_test','y_test']}
def make_models(seed):
 return {'Random Forest':RandomForestClassifier(n_estimators=100,random_state=seed,n_jobs=-1),
 'XGBoost':XGBClassifier(n_estimators=100,random_state=seed,eval_metric='logloss',n_jobs=-1,tree_method='hist'),
 'Linear SVM':Pipeline([('scale',StandardScaler()),('model',SGDClassifier(loss='hinge',alpha=1e-4,max_iter=2000,tol=1e-3,random_state=seed,average=True))]),
 'MLP':Pipeline([('scale',StandardScaler()),('model',MLPClassifier(hidden_layer_sizes=(100,),random_state=seed,early_stopping=True,validation_fraction=.1,n_iter_no_change=3,tol=1e-3,max_iter=100,batch_size=4096))])}
def metrics(y,pred,score):
 tn,fp,fn,tp=confusion_matrix(y,pred,labels=[0,1]).ravel()
 return {'accuracy':accuracy_score(y,pred),'precision':precision_score(y,pred,zero_division=0),'recall':recall_score(y,pred,zero_division=0),'f1':f1_score(y,pred,zero_division=0),'fpr':fp/(fp+tn) if fp+tn else np.nan,'roc_auc':roc_auc_score(y,score),'balanced_accuracy':balanced_accuracy_score(y,pred),'mcc':matthews_corrcoef(y,pred),'tn':int(tn),'fp':int(fp),'fn':int(fn),'tp':int(tp)}
rows=[]
for source in DATASETS:
 for seed in SEEDS:
  for model_name,model in make_models(seed).items():
   t0=time.perf_counter();model.fit(data[source]['X_train'],data[source]['y_train']);fit=time.perf_counter()-t0;mlp_n_iter=(model.named_steps['model'].n_iter_ if model_name=='MLP' else np.nan)
   for target in DATASETS:
    X=data[target]['X_test'];y=data[target]['y_test'];pred=model.predict(X)
    try:score=model.predict_proba(X)[:,1]
    except Exception:score=model.decision_function(X)
    r=metrics(y,pred,score);r.update(source=source,target=target,model=model_name,seed=seed,is_intra=(source==target),fit_seconds=fit,mlp_n_iter=mlp_n_iter);rows.append(r)
res=pd.DataFrame(rows);res.to_csv(OUT/'five_seed_results.csv',index=False)
