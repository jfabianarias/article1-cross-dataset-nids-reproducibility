from pathlib import Path
import sys,time,json
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import SGDClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from xgboost import XGBClassifier
BASE=Path('/mnt/data/obs41_base/CrossDataset_Experiment_Package_v2/harmonized_data');OUT=Path('/mnt/data/obs41_work/results/paired_seed42');OUT.mkdir(parents=True,exist_ok=True)
DS=['UNSW_NB15','CICIDS2017','BoT_IoT','TON_IoT']; source=sys.argv[1];name=sys.argv[2];seed=42
D={}
for d in DS:
 z=np.load(BASE/f'{d}.npz');D[d]={k:z[k] for k in ['X_train','y_train','X_test','y_test']}
if name=='RF':m=RandomForestClassifier(n_estimators=100,random_state=seed,n_jobs=5)
elif name=='XGB':m=XGBClassifier(n_estimators=100,random_state=seed,eval_metric='logloss',n_jobs=5,tree_method='hist',verbosity=0)
elif name=='SVM':m=Pipeline([('scale',StandardScaler()),('model',SGDClassifier(loss='hinge',alpha=1e-4,max_iter=2000,tol=1e-3,random_state=seed,average=True,n_jobs=5))])
elif name=='MLP':m=Pipeline([('scale',StandardScaler()),('model',MLPClassifier(hidden_layer_sizes=(100,),random_state=seed,early_stopping=True,validation_fraction=.1,n_iter_no_change=3,tol=1e-3,max_iter=100,batch_size=4096))])
t=time.perf_counter();m.fit(D[source]['X_train'],D[source]['y_train']);fit=time.perf_counter()-t
for target in DS:
 X=D[target]['X_test'];y=D[target]['y_test'].astype(np.uint8)
 try:s=m.predict_proba(X)[:,1].astype(np.float32);thr=.5;orient='predict_proba(class=1)'
 except Exception:s=m.decision_function(X).astype(np.float32);thr=0.;orient='decision_function(class=1 positive)'
 p=(s>=thr).astype(np.uint8);np.savez_compressed(OUT/f'{source}__{target}__{name}.npz',y=y,pred=p,score=s)
meta={'source':source,'model':name,'seed':seed,'fit_seconds':fit,'threshold':thr,'score_orientation':orient}
if name=='MLP':
 mm=m.named_steps['model'];meta['n_iter']=int(mm.n_iter_);meta['loss_curve']=[float(x) for x in mm.loss_curve_];meta['validation_scores']=[float(x) for x in (mm.validation_scores_ or [])]
(OUT/f'{source}__{name}_meta.json').write_text(json.dumps(meta,indent=2))
print(meta)
