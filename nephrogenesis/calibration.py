"""Bounded calibration of a one-compartment surrogate to explicitly supplied data.

Research observations are declarations made by the operator, not independently
verified data. No fitted parameter is translated into clinical action.
"""
from __future__ import annotations
import csv
import math
from pathlib import Path
from .common import ValidationError,number,integer,object_keys


def synthetic_observations():
    return [{'time_min':float(t),'concentration_mmol_L':10+10*math.exp(-.02*t),
             'split':'train' if i%3!=2 or i==0 else 'test'}
            for i,t in enumerate(range(0,201,10))]


def read_observations(path):
    path=Path(path)
    if path.stat().st_size>100000: raise ValidationError('CSV exceeds 100000 bytes')
    with path.open(newline='',encoding='utf-8') as f:
        reader=csv.DictReader(f)
        if reader.fieldnames!=['time_min','concentration_mmol_L','split']:
            raise ValidationError('CSV header must be time_min,concentration_mmol_L,split in that order')
        try:
            rows=[{'time_min':float(r['time_min']),'concentration_mmol_L':float(r['concentration_mmol_L']),'split':r['split']} for r in reader]
        except (KeyError,ValueError,TypeError) as e: raise ValidationError('Malformed observation row') from e
    return rows


def calibrate(p):
    keys={'observations','source','k_min_per_min','k_max_per_min','css_min_mmol_L','css_max_mmol_L','grid_size'}
    object_keys(p,keys,keys)
    rows=p['observations'];source=p['source']
    object_keys(source,{'id','kind','locator','rights_confirmed'},{'id','kind','locator','rights_confirmed'})
    if source['kind'] not in {'synthetic','research_observations'}: raise ValidationError('Use synthetic or research_observations data kind')
    if source['rights_confirmed'] is not True: raise ValidationError('Confirm rights to use the supplied research data')
    if any(not isinstance(source[k],str) or not source[k].strip() or len(source[k])>1000 for k in ('id','locator')):
        raise ValidationError('A bounded source identifier and locator are required')
    if not isinstance(rows,list) or not 5<=len(rows)<=200: raise ValidationError('Supply 5 to 200 ordered observations')
    clean=[]
    for row in rows:
        object_keys(row,{'time_min','concentration_mmol_L','split'},{'time_min','concentration_mmol_L','split'})
        t=number(row['time_min'],'time_min',0,10000);c=number(row['concentration_mmol_L'],'concentration_mmol_L',0,10000)
        if row['split'] not in {'train','test'}: raise ValidationError('Observation split must be train or test')
        if clean and t<=clean[-1]['time_min']: raise ValidationError('Observation times must strictly increase')
        clean.append({'time_min':t,'concentration_mmol_L':c,'split':row['split']})
    if clean[0]['time_min']!=0 or clean[0]['split']!='train': raise ValidationError('The first row must be a training initial condition at time zero')
    train=[r for r in clean if r['split']=='train'];test=[r for r in clean if r['split']=='test']
    if len(train)<3 or len(test)<2: raise ValidationError('At least 3 training and 2 held-out observations required')
    lo=number(p['k_min_per_min'],'k_min_per_min',.000001,1);hi=number(p['k_max_per_min'],'k_max_per_min',.000001,1)
    cl=number(p['css_min_mmol_L'],'css_min_mmol_L',0,10000);ch=number(p['css_max_mmol_L'],'css_max_mmol_L',0,10000)
    if hi<=lo or ch<=cl: raise ValidationError('Grid upper bounds must exceed lower bounds')
    n=integer(p['grid_size'],'grid_size',5,101);c0=clean[0]['concentration_mmol_L']
    candidates=[];profile=[]
    for i in range(n):
        k=lo+(hi-lo)*i/(n-1);best_k=None
        for j in range(n):
            css=cl+(ch-cl)*j/(n-1)
            sse=sum((r['concentration_mmol_L']-(css+(c0-css)*math.exp(-k*r['time_min'])))**2 for r in train)
            item=(sse,k,css,i,j)
            if best_k is None or item<best_k:best_k=item
            candidates.append(item)
        profile.append({'k_per_min':k,'minimum_training_SSE':best_k[0]})
    best=min(candidates);sse,k,css,ki,ci=best
    predictions=[css+(c0-css)*math.exp(-k*r['time_min']) for r in clean]
    out=[{**r,'prediction_mmol_L':y,'residual_mmol_L':r['concentration_mmol_L']-y} for r,y in zip(clean,predictions)]
    mse=sum(r['residual_mmol_L']**2 for r in out if r['split']=='test')/len(test)
    baseline=sum((r['concentration_mmol_L']-c0)**2 for r in test)/len(test)
    return {'title':'Calibrate a declared surrogate without using held-out outcomes','status':'conditional_fit_to_operator_declared_data',
            'metrics':{'k_per_min':k,'equilibrium_mmol_L':css,'generation_mmol_L_min':k*css,
                       'training_SSE':sse,'held_out_MSE':mse,'constant_initial_value_held_out_MSE':baseline,
                       'on_search_boundary':ki in (0,n-1) or ci in (0,n-1),'candidate_grid_points':n*n},
            'rows':out,'profile':profile,'source_declaration':source,
            'series':[{'name':'supplied observations','x':[r['time_min'] for r in clean],'y':[r['concentration_mmol_L'] for r in clean],'x_unit':'min','y_unit':'mmol/L'},
                      {'name':'training-selected surrogate','x':[r['time_min'] for r in clean],'y':predictions,'x_unit':'min','y_unit':'mmol/L'}],
            'notes':['Fit C(t)=Css+(C0-Css)exp(-kt) on the declared finite grid using training rows only. C0 is fixed at the initial training observation.',
                     'No confidence interval is claimed; uncertainty in C0, correlated noise, model discrepancy and grid resolution remain unmodeled.',
                     'A boundary optimum may mean inadequate search bounds or model mismatch. Held-out error is reported without clinical interpretation.',
                     'The source kind and rights statement are operator declarations, not verified provenance. No personal identifiers are needed.']}
