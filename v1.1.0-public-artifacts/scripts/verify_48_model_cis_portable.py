#!/usr/bin/env python3
"""Reproduce external 48-cell, five-seed, class-stratified paired-flow CIs.
Inputs stay private; no NPZ files are redistributed.
"""
import argparse
from pathlib import Path
import numpy as np
import pandas as pd
S=['UNSW_NB15','CICIDS2017','BoT_IoT','TON_IoT']
M=['Linear SVM','XGBoost','Random Forest','MLP']
SEEDS=[42,52,62,72,82]
def main():
    p=argparse.ArgumentParser()
    p.add_argument('--private',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--replicates',type=int,default=20000)
    p.add_argument('--rng-seed',type=int,default=20261105)
    a=p.parse_args()
    rng=np.random.default_rng(a.rng_seed)
    rows=[]
    for src in S:
        for trg in S:
            if src==trg: continue
            for model in M:
                y=None; idx=None; preds=[]
                for seed in SEEDS:
                    f=a.private/f'{src}__{model.replace(" ","_")}__s{seed}__{trg}.npz'
                    with np.load(f,allow_pickle=False) as z:
                        yy=z['y_true'];ii=z['target_test_index'];p=z['y_pred']
                    if y is None:y=yy;idx=ii
                    else:
                        assert np.array_equal(y,yy) and np.array_equal(idx,ii),f
                    preds.append(p)
                k=np.stack(preds).sum(axis=0)
                h0=np.bincount(k[y==0],minlength=6)
                h1=np.bincount(k[y==1],minlength=6)
                n0=h0.sum();n1=h1.sum();v=np.arange(6)/5
                point=.5*(1-(h0@v)/n0+(h1@v)/n1)
                reps=.5*(1-(rng.multinomial(n0,h0/n0,size=a.replicates)@v)/n0+(rng.multinomial(n1,h1/n1,size=a.replicates)@v)/n1)
                q=np.quantile(reps,[.05/(2*48),.025,.975,1-.05/(2*48)])
                rows.append(dict(source=src,target=trg,model=model,BA=point,ci95_low=q[1],ci95_high=q[2],ci_bonf_low=q[0],ci_bonf_high=q[3],ci95_below_chance=q[2]<.5,bonf_below_chance=q[3]<.5,replicates=a.replicates))
    a.output.parent.mkdir(parents=True,exist_ok=True)
    pd.DataFrame(rows).to_csv(a.output,index=False)
    print('48 cells; nominal-below',sum(r['ci95_below_chance'] for r in rows),'Bonferroni-below',sum(r['bonf_below_chance'] for r in rows))
if __name__=='__main__':main()
