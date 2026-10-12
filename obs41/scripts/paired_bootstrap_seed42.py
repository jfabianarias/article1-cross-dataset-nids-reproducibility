from pathlib import Path
import numpy as np,pandas as pd
from scipy.stats import norm
P=Path('/mnt/data/obs41_work/results/paired_seed42'); OUT=Path('/mnt/data/obs41_work/results/paired_uncertainty'); OUT.mkdir(parents=True,exist_ok=True)
DS=['UNSW_NB15','CICIDS2017','BoT_IoT','TON_IoT']; MODELS=['RF','XGB','SVM','MLP']; B=5000; rng=np.random.default_rng(20261012)
def metric_counts(tn,fp,fn,tp):
 tpr=np.divide(tp,tp+fn,out=np.zeros_like(tp,dtype=float),where=(tp+fn)>0); tnr=np.divide(tn,tn+fp,out=np.zeros_like(tn,dtype=float),where=(tn+fp)>0);ba=(tpr+tnr)/2
 tn=tn.astype(float);fp=fp.astype(float);fn=fn.astype(float);tp=tp.astype(float);den=np.sqrt((tp+fp)*(tp+fn)*(tn+fp)*(tn+fn));mcc=np.divide(tp*tn-fp*fn,den,out=np.zeros_like(den,dtype=float),where=den>0);return ba,mcc
def bh(p):
 p=np.asarray(p,float);n=len(p);order=np.argsort(p);q=np.empty(n);prev=1
 for rank,i in reversed(list(enumerate(order,start=1))):
  val=min(prev,p[i]*n/rank);q[i]=val;prev=val
 return q
rows=[];dirs=[]
for source in DS:
 for target in DS:
  ys=None; preds=[]
  for m in MODELS:
   z=np.load(P/f'{source}__{target}__{m}.npz')
   if ys is None: ys=z['y'].astype(np.uint8)
   preds.append(z['pred'].astype(np.uint8))
  A=np.column_stack(preds); n=len(ys); mask=A[:,0]+2*A[:,1]+4*A[:,2]+8*A[:,3]; cat=ys.astype(int)*16+mask
  counts=np.bincount(cat,minlength=32); probs=counts/counts.sum(); boots=rng.multinomial(n,probs,size=B); bas=[]
  for j,m in enumerate(MODELS):
   bit=1<<j; tn=np.zeros(B,dtype=np.int64);fp=tn.copy();fn=tn.copy();tp=tn.copy()
   for c in range(32):
    y=c//16;pred=1 if (c%16)&bit else 0;v=boots[:,c]
    if y==0 and pred==0:tn+=v
    elif y==0:fp+=v
    elif pred==0:fn+=v
    else:tp+=v
   ba,mc=metric_counts(tn,fp,fn,tp); bas.append(ba)
   yy=ys;pp=A[:,j];otn=((yy==0)&(pp==0)).sum();ofp=((yy==0)&(pp==1)).sum();ofn=((yy==1)&(pp==0)).sum();otp=((yy==1)&(pp==1)).sum();oba,_=metric_counts(np.array([otn]),np.array([ofp]),np.array([ofn]),np.array([otp]))
   rows.append(dict(source=source,target=target,model=m,ba=float(oba[0]),ba_lo=float(np.quantile(ba,.025)),ba_hi=float(np.quantile(ba,.975)),mcc_lo=float(np.quantile(mc,.025)),mcc_hi=float(np.quantile(mc,.975)),p_below_ref=float((ba>=.5).mean()),is_intra=source==target))
  meanba=np.vstack(bas).mean(axis=0);dirs.append(dict(source=source,target=target,ba_models_mean=float(np.mean([r['ba'] for r in rows[-4:]])),ba_lo=float(np.quantile(meanba,.025)),ba_hi=float(np.quantile(meanba,.975)),is_intra=source==target))
cell=pd.DataFrame(rows);ext=cell[~cell.is_intra].copy();ext['q_below_ref_bh']=bh(ext.p_below_ref.values);cell=cell.merge(ext[['source','target','model','q_below_ref_bh']],on=['source','target','model'],how='left');cell.to_csv(OUT/'paired_seed42_cell_intervals.csv',index=False);pd.DataFrame(dirs).to_csv(OUT/'paired_seed42_direction_intervals.csv',index=False)
print('external cells CI entirely below .5:',((~cell.is_intra)&(cell.ba_hi<.5)).sum())
print('BH q<.05 below-reference:',((~cell.is_intra)&(cell.q_below_ref_bh<.05)&(cell.ba<.5)).sum())
