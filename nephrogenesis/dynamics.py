"""Reduced, conservative, hybrid compartment model. No patient calibration.

RK4 advances states and cumulative fluxes with the same quadrature. Sensor-based
actuation is held during each step: solver convergence is not a claim of fourth
order convergence for the entire delayed hybrid controller.
"""
from __future__ import annotations
import bisect
import math
import random
from .common import ValidationError, number, integer, object_keys

DEFAULT = {
    'duration_min':360.0, 'dt_min':.5, 'initial_volume_L':14.0,
    'initial_sodium_mmol':1960.0, 'initial_urea_mmol':70.0,
    'gfr_L_min':.12, 'water_input_L_min':.001, 'sodium_input_mmol_min':.10,
    'urea_generation_mmol_min':.024, 'urea_clearance_fraction':.04,
    'controller':'feedback', 'delay_min':0.0, 'seed':98,
    'volume_gain':.005, 'osmotic_gain':.00005, 'sodium_gain':.03,
    'active_fraction':.6, 'atp_energy_J_mol':50000.0, 'power_budget_W':5.0,
    'events':[{'start_min':60.0,'end_min':120.0,'water_extra_L_min':.006,'sodium_extra_mmol_min':.4}],
}
NUMERIC_BOUNDS={
    'duration_min':(.1,2880), 'dt_min':(.01,10), 'initial_volume_L':(.1,40),
    'initial_sodium_mmol':(.01,20000), 'initial_urea_mmol':(.001,10000),
    'gfr_L_min':(.001,.5), 'water_input_L_min':(0,.05), 'sodium_input_mmol_min':(0,5),
    'urea_generation_mmol_min':(0,5), 'urea_clearance_fraction':(0,1),
    'delay_min':(0,2880),'volume_gain':(0,.1),'osmotic_gain':(0,.001), 'sodium_gain':(0,1),
    'active_fraction':(0,1),'atp_energy_J_mol':(1000,100000),'power_budget_W':(0,100),
}
MODES={'fixed','feedback','delayed','scrambled','reversed'}


def config(overrides: dict | None = None) -> dict:
    if overrides is None: overrides={}
    object_keys(overrides,set(DEFAULT))
    p={**DEFAULT,**overrides}
    for k,(lo,hi) in NUMERIC_BOUNDS.items(): p[k]=number(p[k],k,lo,hi)
    integer(p['seed'],'seed',0,2**32-1)
    if p['controller'] not in MODES: raise ValidationError(f'controller must be one of {sorted(MODES)}')
    if p['duration_min']/p['dt_min']>20000: raise ValidationError('At most 20000 base steps are allowed')
    if not isinstance(p['events'],list) or len(p['events'])>20: raise ValidationError('At most 20 events allowed')
    events=[]
    for event in p['events']:
        keys={'start_min','end_min','water_extra_L_min','sodium_extra_mmol_min'}
        object_keys(event,keys,keys)
        e={k:number(v,k) for k,v in event.items()}
        if not 0<=e['start_min']<e['end_min']<=p['duration_min']:
            raise ValidationError('Event interval must be ordered and inside the simulation horizon')
        number(e['water_extra_L_min'],'water_extra',0,.05)
        number(e['sodium_extra_mmol_min'],'sodium_extra',0,5)
        events.append(e)
    p['events']=events
    return p


def rk4_step(y,dt,derivative):
    k1=derivative(y)
    k2=derivative([a+dt*b/2 for a,b in zip(y,k1)])
    k3=derivative([a+dt*b/2 for a,b in zip(y,k2)])
    k4=derivative([a+dt*b for a,b in zip(y,k3)])
    return [a+dt*(b+2*c+2*d+e)/6 for a,b,c,d,e in zip(y,k1,k2,k3,k4)]


def _domain(y):
    if any(not math.isfinite(x) for x in y) or y[0]<.05 or y[1]<=0 or y[2]<=0:
        raise ValidationError('State left the positive compartment domain; shorten dt or change the scenario. No clipping was applied.')


def simulate(overrides: dict | None = None) -> dict:
    p=config(overrides); rng=random.Random(p['seed'])
    # states: water, Na, urea, outputs of each, inputs of each, coupled energy
    y=[p['initial_volume_L'],p['initial_sodium_mmol'],p['initial_urea_mmol']]+[0.0]*7
    times=[0.]; history=[(y[0],y[1]/y[0])]
    rows=[]; maximum=[0.0,0.0,0.0]; time_viable=0.; capped_steps=0
    boundaries=sorted({0.,p['duration_min'],*(x[k] for x in p['events'] for k in ('start_min','end_min'))})
    t=0.
    def record():
        residual=[y[i]-[p['initial_volume_L'],p['initial_sodium_mmol'],p['initial_urea_mmol']][i]-y[6+i]+y[3+i] for i in range(3)]
        for i in range(3): maximum[i]=max(maximum[i],abs(residual[i]))
        return {'time_min':t,'volume_L':y[0],'sodium_mmol_L':y[1]/y[0],
                'urea_mmol_L':y[2]/y[0],'water_excreted_L':y[3],'sodium_excreted_mmol':y[4],
                'urea_excreted_mmol':y[5],'water_input_L':y[6], 'sodium_input_mmol':y[7],
                'urea_generated_mmol':y[8],'coupled_energy_J':y[9],
                'water_residual_L':residual[0],'sodium_residual_mmol':residual[1],'urea_residual_mmol':residual[2]}
    rows.append(record())
    while t < p['duration_min']-1e-10:
        future=boundaries[bisect.bisect_right(boundaries,t+1e-10):]
        dt=min(p['dt_min'],p['duration_min']-t, future[0]-t if future else p['duration_min']-t)
        sense=history[-1]
        if p['controller']=='delayed':
            idx=max(0,bisect.bisect_right(times,t-p['delay_min'])-1); sense=history[idx]
        elif p['controller']=='scrambled': sense=history[rng.randrange(len(history))]
        dv,dc=sense[0]-14.,sense[1]-140.
        if p['controller']=='fixed': dv=dc=0.
        if p['controller']=='reversed': dv,dc=-dv,-dc
        water=max(.0001,min(.015,.001+p['volume_gain']*dv-p['osmotic_gain']*dc))
        sodium=max(0,min(.8,.1+p['sodium_gain']*dc+.02*dv))
        g=p['gfr_L_min']
        rw=max(0,min(1,1-water/g))
        rn=max(0,min(1,1-sodium/(g*(y[1]/y[0]))))
        mid=t+dt/2
        wi=p['water_input_L_min']+sum(e['water_extra_L_min'] for e in p['events'] if e['start_min']<=mid<e['end_min'])
        ni=p['sodium_input_mmol_min']+sum(e['sodium_extra_mmol_min'] for e in p['events'] if e['start_min']<=mid<e['end_min'])
        ui=p['urea_generation_mmol_min']; active=p['active_fraction']
        cap=math.inf if active==0 else p['power_budget_W']*60*3/(.001*active*p['atp_energy_J_mol'])
        if g*y[1]/y[0]*rn > cap: capped_steps+=1
        def derivative(z):
            _domain(z)
            filtered=g*z[1]/z[0]
            reabsorbed=min(filtered*rn,cap)
            wo=g*(1-rw); no=filtered-reabsorbed; uo=g*z[2]/z[0]*p['urea_clearance_fraction']
            energy=reabsorbed*.001*active/3*p['atp_energy_J_mol'] # J/min
            return [wi-wo,ni-no,ui-uo,wo,no,uo,wi,ni,ui,energy]
        if 13.5<=y[0]<=14.5 and 135<=y[1]/y[0]<=145: time_viable+=dt
        y=rk4_step(y,dt,derivative); _domain(y)
        t=min(p['duration_min'],t+dt); times.append(t); history.append((y[0],y[1]/y[0])); rows.append(record())
    return {'model':'regulated-compartment-v1','status':'synthetic_unvalidated_model','config':p,'trajectory':rows,
            'metrics':{'maximum_water_residual_L':maximum[0],'maximum_sodium_residual_mmol':maximum[1],
                       'maximum_urea_residual_mmol':maximum[2],'coupled_energy_J':y[9],
                       'mean_coupled_power_W':y[9]/(60*p['duration_min']),
                       'declared_box_time_fraction':time_viable/p['duration_min'],'budget_limited_steps':capped_steps,
                       'final_volume_L':y[0],'final_sodium_mmol_L':y[1]/y[0]},
            'assumptions':['Single well-mixed compartment; no vascular, glomerular or medullary geometry.',
                           'Filtered and reabsorbed sodium are reduced budget quantities, not a full nephron solver.',
                           'Active fraction and ATP stoichiometry are fixed scenario assumptions; basal metabolism is excluded.',
                           'Viability box [13.5,14.5] L and [135,145] mmol/L is a chosen teaching constraint, not a survival threshold.',
                           'Delayed and scrambled sensors are synthetic causal interventions, not empirical neural mechanisms.']}
