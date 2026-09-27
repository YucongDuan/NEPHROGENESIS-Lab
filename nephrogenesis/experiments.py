"""Executable chapter laboratories and explicitly synthetic research experiments."""
from __future__ import annotations
import math
import random
import statistics
from .common import ValidationError, number, integer, object_keys
from .calculators import calculate, defaults as calc_defaults, R, KB, NA
from .dynamics import simulate, config as model_config
from .evidence import demonstration_graph, validate_graph, withdraw


def result(title, metrics, rows=None, series=None, notes=None):
    return {'title':title,'status':'synthetic_or_conditional_teaching_experiment',
            'metrics':metrics,'rows':rows or [],'series':series or [],'notes':notes or []}


def series(name,x,y,x_unit='min',y_unit='1'):
    return {'name':name,'x':x,'y':y,'x_unit':x_unit,'y_unit':y_unit}


def signal_experiment(p):
    n=integer(p['samples'],'samples',20,5000); seed=integer(p['seed'],'seed',0,2**32-1)
    error=number(p['error_probability'],'error_probability',0,1)
    delay=integer(p['delay_steps'],'delay_steps',0,n-1)
    rng=random.Random(seed)
    # Balanced alternating blocks are a designed finite sequence, not an ecological model.
    states=[(i//10)%2 for i in range(n)]
    obs=[s ^ (rng.random()<error) for s in states]
    shuffled=obs[:]; rng.shuffle(shuffled)
    delayed=[obs[max(0,i-delay)] for i in range(n)]
    strategies={'matched':obs,'fixed':[0]*n,'shuffled':shuffled,'delayed':delayed,
                'reversed':[1-o for o in obs], 'calibrated_remap':[1-o if error>.5 else o for o in obs]}
    rows=[]; curves=[]
    for name,actions in strategies.items():
        cumulative=[0]
        for action,state in zip(actions,states): cumulative.append(cumulative[-1]+(4 if action==state else 0))
        curves.append(series(name,list(range(n+1)),cumulative,'trial','recovered units'))
        matches=sum(a==s for a,s in zip(actions,states))
        rows.append({'strategy':name,'matched_fraction':matches/n,'allocation_energy_J':float(n),
                     'observation_count':n,'recovered_units':4*matches,'unrecovered_units':4*(n-matches)})
    # Binary symmetric channel mutual information assumes a balanced input distribution.
    h=0 if error in (0,1) else -error*math.log2(error)-(1-error)*math.log2(1-error)
    return result('Equal resource budget, different signal-to-action correspondence',
                  {'channel_information_bits':1-h,'fixed_decoder_expected_accuracy':1-error,
                   'optimally_remapped_expected_accuracy':max(error,1-error)},rows,
                  curves,
                  ['Each strategy receives the same number of observations and spends 1 J per action by construction.',
                   'Allocation energy excludes sensing and computation; this is a matched-action-budget experiment, not a total thermodynamic audit.',
                   'Calibrated remapping knows the declared error rate. It is not inferred from the test sequence.',
                   'Toy correspondence experiment; no conclusion about a new physical information field or consciousness follows.'])


def identifiability(p):
    noise=number(p['noise_sd'],'noise_sd',.001,10); horizon=number(p['horizon_min'],'horizon_min',1,1000)
    t=[horizon*i/100 for i in range(101)]
    a=[10+10*math.exp(-.02*x) for x in t]
    b=[10+10*math.exp(-.01*x) for x in t]
    scores=[(x-y)**2/noise**2 for x,y in zip(a,b)]
    j=max(range(len(t)),key=lambda k:scores[k])
    rows=[{'time_min':x,'candidate_A':y,'candidate_B':z,'squared_separation_over_variance':s}
          for x,y,z,s in zip(t,a,b,scores)]
    return result('Equal steady state, distinguishable transient',
                  {'steady_A':.2/.02,'steady_B':.1/.01,'best_candidate_time_min':t[j],
                   'maximum_design_score':scores[j]},rows,
                  [series('G=0.2, k=0.02',t,a,'min','mmol/L'),series('G=0.1, k=0.01',t,b,'min','mmol/L')],
                  ['ODE: dC/dt = G - k C, C(0)=20 mmol/L. G has units mmol/L/min; k has units 1/min.',
                   'Both candidates have C*=10. A single equilibrium observation cannot identify G and k separately.',
                   'The design score assumes independent Gaussian observation noise with stated variance. It is not a clinical measurement schedule.'])


def membrane(p):
    k=number(p['conductance_L_min'],'conductance_L_min',0,2)
    va=number(p['volume_A_L'],'volume_A_L',.01,20); vb=number(p['volume_B_L'],'volume_B_L',.01,20)
    ca=number(p['initial_A_mmol_L'],'initial_A_mmol_L',0,1000); cb=number(p['initial_B_mmol_L'],'initial_B_mmol_L',0,1000)
    total=va*ca+vb*cb; ceq=total/(va+vb); t=list(range(121))
    a=[ceq+vb/(va+vb)*(ca-cb)*math.exp(-k*(1/va+1/vb)*x) for x in t]
    b=[ceq-va/(va+vb)*(ca-cb)*math.exp(-k*(1/va+1/vb)*x) for x in t]
    return result('A permeable boundary and conserved solute',
                  {'equilibrium_mmol_L':ceq,'maximum_mass_residual_mmol':max(abs(va*x+vb*y-total) for x,y in zip(a,b))},
                  series=[series('Compartment A',t,a,'min','mmol/L'),series('Compartment B',t,b,'min','mmol/L')],
                  notes=['Exact solution of two fixed-volume well-mixed compartments with symmetric passive exchange.',
                         'Volumes do not change; this is not a coupled osmosis model or a reconstruction of the origin of life.'])


def geometry(p):
    d=number(p['diffusivity_m2_s'],'diffusivity_m2_s',positive=True)
    radii=[1e-6,1e-5,1e-4,1e-3,1e-2]
    rows=[{'radius_m':r,'surface_to_volume_per_m':3/r,'diffusion_time_s':r*r/(2*d)} for r in radii]
    return result('Increasing size changes exchange constraints',{'diffusivity_m2_s':d},rows,
                  notes=['Sphere A/V=3/r; one-dimensional characteristic diffusion estimate t=L^2/(2D).',
                         'The time estimate and spherical area ratio answer different geometric questions; neither proves a particular organ was inevitable.'])


def branching(p):
    generations=integer(p['generations'],'generations',0,15)
    rows=[]
    # Binary symmetric network: each daughter radius scales by r, length by l.
    shrink=number(p['radius_ratio'],'radius_ratio',.4,.95)
    length=number(p['length_ratio'],'length_ratio',.4,.95)
    for depth in range(generations+1):
        resistance=sum((length/(2*shrink**4))**i for i in range(depth+1))
        rows.append({'generations':depth,'terminal_count':2**depth,
                     'relative_network_resistance':resistance,'relative_terminal_area':(2*shrink**2)**depth})
    return result('More branches are not automatically better transport',{'assumed_radius_ratio':shrink},rows,
                  notes=['Symmetric cylindrical network; Poiseuille resistance normalized to the root segment.',
                         'Parallel branches are combined at each depth. Terminal count is not nephron count and does not establish organoid maturation.'])


def transport(p):
    out=number(p['excreted_mmol_min'],'excreted_mmol_min',0,1)
    loads=[number(p['low_filtered_mmol_min'],'low_filtered_mmol_min',positive=True),
           number(p['high_filtered_mmol_min'],'high_filtered_mmol_min',positive=True)]
    if out>min(loads): raise ValidationError('Excreted load exceeds a filtered load; secretion is excluded from this experiment')
    active=number(p['active_fraction'],'active_fraction',0,1)
    rows=[]
    for label,load in zip(('lower_filtered_load','higher_filtered_load'),loads):
        reabs=load-out
        energy=reabs*.001/60*active/3*50000
        rows.append({'scenario':label,'filtered_mmol_min':load,'excreted_mmol_min':out,
                     'reabsorbed_mmol_min':reabs,'coupled_power_W':energy})
    return result('The same output can conceal different work',
                  {'output_difference_mmol_min':0.0,'coupled_power_difference_W':rows[1]['coupled_power_W']-rows[0]['coupled_power_W']},rows,
                  notes=['Filtered minus reabsorbed equals excreted; secretion is set to zero.',
                         'Power uses a declared active fraction, 3 sodium per ATP and 50 kJ/mol ATP. It is not measured whole-kidney metabolism.'])


def habitats(p):
    load=number(p['daily_osmoles_mOsm'],'daily_osmoles_mOsm',0,3000)
    water=number(p['available_water_L'],'available_water_L',0,20)
    rows=[{'hypothetical_environment':name,'maximum_mOsm_L':cap,'minimum_urine_L':load/cap,
           'remaining_water_budget_L':water-load/cap} for name,cap in [('dilute_limit',300),('intermediate_limit',600),('concentrating_limit',1200)]]
    return result('A shared constraint, alternative concentrating capacities',{'daily_mOsm':load},rows,
                  notes=['Hypothetical capacities, not species measurements. No animal is ranked as evolutionarily superior.',
                         'Other water gains/losses, nitrogen chemistry, ancestry and body size are omitted.'])


def repair(p):
    slow=number(p['slow_repair_rate'],'slow_repair_rate',.0001,1)
    fast=number(p['fast_repair_rate'],'fast_repair_rate',.0001,1)
    t=list(range(181)); a=[]; b=[]; reserve=[]
    for x in t:
        # The synthetic reserve deficit has slower decay than the synthetic functional deficit.
        a.append(math.exp(-fast*x)); b.append(math.exp(-slow*x)); reserve.append(1-.4*math.exp(-slow*x))
    return result('Functional recovery and reserve recovery can separate',
                  {'functional_deficit_at_180':a[-1],'structural_deficit_at_180':b[-1],'reserve_at_180':reserve[-1]},
                  series=[series('functional deficit',t,a,'arbitrary time','1'),series('structural deficit',t,b,'arbitrary time','1'),series('reserve',t,reserve,'arbitrary time','1')],
                  notes=['Independent exponential recovery modes selected for demonstration; not a disease-course model.',
                         'A shared measured endpoint does not demonstrate identical structure or capacity for a second challenge.'])


def memory(p):
    decay=number(p['decay_rate'],'decay_rate',.001,1)
    legacy=number(p['legacy_load'],'legacy_load',0,5)
    t=list(range(121)); naive=[]; history=[]
    for x in t:
        stimulus=1 if 30<=x<60 else 0
        naive.append(stimulus)
        history.append(stimulus*(1+legacy*math.exp(-decay*x)))
    return result('An explicit hidden state changes a repeated response',{'history_state_initial':legacy},
                  series=[series('no legacy',t,naive,'arbitrary time','response'),series('with legacy',t,history,'arbitrary time','response')],
                  notes=['h(t)=h0 exp(-lambda t); response=s(t)(1+h(t)). The history variable is assumed, not inferred from a single endpoint.',
                         'This toy cannot distinguish epigenetic state, persistent exposure and measurement bias without additional observations.'])


def replacement(p):
    fraction=number(p['solute_clearance_fraction'],'solute_clearance_fraction',0,1)
    rows=[{'function':name,'declared_coverage':coverage,'evidence_status':'synthetic_design_contract'}
          for name,coverage in [('solute clearance',fraction),('fluid removal',.8),('regulated electrolyte control',.4),('endocrine signaling',0),('developmental renewal',0)]]
    return result('Replacement requires a vector of functions',{'single_clearance_coverage':fraction,'uncovered_function_count':sum(r['declared_coverage']==0 for r in rows)},rows,
                  notes=['A hypothetical device, not dialysis, transplant or any named product. Entries are design declarations, not validated performance.',
                         'No weighted overall effectiveness score is produced. Coverage of a clearance task does not imply endocrine replacement.'])


def evidence_lab(p):
    graph=demonstration_graph(); baseline=validate_graph(graph)
    revised=withdraw(graph,p['withdraw_id'])
    return result('A correction propagates through the research record',
                  {'initial_graph_valid':baseline['valid'],'affected_nodes':len(revised['affected'])},
                  [{'node':n['id'],'kind':n['kind'],'role':n['role'],'status':n['status']} for n in revised['graph']['nodes']],
                  notes=['Dependency structure is checked; truth is not certified by a graph or a hash.']) | {'before':graph,'after':revised}


def ablation(p):
    """Designed fault detection fixture, not a measured clinical/DIKWP benefit."""
    fixtures=[
        {'id':'clean','issues':[]},
        {'id':'joule_vs_molar','issues':['units']},
        {'id':'missing_source','issues':['provenance']},
        {'id':'broken_mass_budget','issues':['conservation']},
        {'id':'synthetic_as_empirical','issues':['evidence_kind']},
        {'id':'stale_dependency','issues':['dependency']},
        {'id':'mixed_failure','issues':['units','provenance','conservation']},
    ]
    # Each fault is exercised by a concrete validator, not merely read from its label.
    from .units import Quantity
    detected={}
    try: (Quantity.of(1,'J')+Quantity.of(1,'J/mol'))
    except ValidationError: detected['joule_vs_molar']=['units']
    bad=demonstration_graph(); del bad['nodes'][1]['source']
    try: validate_graph(bad)
    except ValidationError: detected['missing_source']=['provenance']
    detected['broken_mass_budget']=['conservation'] if abs(10-9-2)>1e-9 else []
    bad=demonstration_graph(); bad['nodes'][4]['kind']='empirical'; bad['nodes'][4]['source']='declared study'
    checked=validate_graph(bad)
    detected['synthetic_as_empirical']=['evidence_kind'] if not checked['node_validity']['calculation'] else []
    detected['stale_dependency']=['dependency'] if not withdraw(demonstration_graph(),'synthetic-flux')['validation']['valid'] else []
    detected['mixed_failure']=detected['joule_vs_molar']+detected['missing_source']+detected['broken_mass_budget']
    detected['clean']=[]
    levels={'untyped_record':set(),'units_only':{'units'},'units_and_sources':{'units','provenance'},
            'full_contract':{'units','provenance','conservation','evidence_kind','dependency'}}
    rows=[]
    for level,enabled in levels.items():
        for fixture in fixtures:
            found=sorted(set(detected[fixture['id']]) & enabled)
            rows.append({'validator':level,'fixture':fixture['id'],'expected_fault':bool(fixture['issues']),
                         'detected':bool(found),'detected_categories':','.join(found)})
    return result('Ablation of declared research-contract checks',{'faulty_fixtures':6,'clean_fixtures':1},rows,
                  notes=['Fault fixtures are designed to exercise these checks. Results are not independent evidence that DIKWP improves researcher judgment.',
                         'The untyped baseline stores data and performs no checks; it is not an upstream system performance benchmark.'])


def hypothesis(p):
    seed=integer(p['seed'],'seed',0,2**32-1); sd=number(p['noise_sd'],'noise_sd',.01,10)
    injected=number(p['injected_amplitude'],'injected_amplitude',-5,5); rng=random.Random(seed)
    t=[i*4 for i in range(50)]; baseline=[10+10*math.exp(-.02*x) for x in t]
    phi=[math.sin(x/15) for x in t]; y=[b+injected*f+rng.gauss(0,sd) for b,f in zip(baseline,phi)]
    train=list(range(0,50,2)); test=list(range(1,50,2))
    amp=sum(phi[i]*(y[i]-baseline[i]) for i in train)/sum(phi[i]**2 for i in train)
    rows=[]
    for name,a,k in [('fixed_baseline',0,0),('registered_sinusoidal_extension',amp,1)]:
        sse=sum((y[i]-baseline[i]-a*phi[i])**2 for i in train)
        mse=sum((y[i]-baseline[i]-a*phi[i])**2 for i in test)/len(test)
        bic=sse/sd**2+k*math.log(len(train)) # Gaussian constants cancel; known variance
        rows.append({'candidate':name,'fitted_amplitude':a,'training_SSE':sse,'BIC_without_shared_constant':bic,'held_out_MSE':mse})
    return result('A preregistered additional-effect candidate',{'seed':seed,'noise_sd':sd,'injected_amplitude':injected},rows,
                  [series('synthetic observations',t,y,'min','mmol/L'),series('fixed baseline',t,baseline,'min','mmol/L'),series('extension prediction',t,[b+amp*f for b,f in zip(baseline,phi)],'min','mmol/L')],
                  ['The sinusoid is an arbitrary added effect with a declared basis, not an information-field equation.',
                   'Baseline constants, noise variance, basis and split are fixed in advance; only the extension amplitude is fitted on even-index samples.',
                   'Held-out performance can discriminate these two candidates under this generator; it cannot establish a novel physical field.'])


def uncertainty(p):
    count=integer(p['samples'],'samples',5,100); seed=integer(p['seed'],'seed',0,2**32-1); rng=random.Random(seed)
    rows=[]
    for i in range(count):
        g=rng.uniform(.08,.16); active=rng.uniform(.4,.8)
        r=simulate({'duration_min':180.,'dt_min':1.,'gfr_L_min':g,'active_fraction':active})
        rows.append({'sample':i,'gfr_L_min':g,'active_fraction':active,**r['metrics']})
    energies=sorted(x['coupled_energy_J'] for x in rows)
    return result('Scenario uncertainty, not a patient confidence interval',
                  {'samples':count,'energy_min_J':min(energies),'energy_max_J':max(energies),'energy_median_J':statistics.median(energies)},rows,
                  notes=['Independent uniform scenario parameters: GFR 0.08-0.16 L/min and active fraction 0.4-0.8.',
                         'These bounds are teaching choices, not population distributions or posterior intervals.'])


def viability(p):
    horizon=number(p['duration_min'],'duration_min',120,600); rows=[]
    for gain in [0.,.001,.005,.01]:
        for budget in [1.,2.,5.]:
            try:
                r=simulate({'duration_min':horizon,'dt_min':1.,'volume_gain':gain,'power_budget_W':budget})
                metrics=r['metrics']
                rows.append({'volume_gain':gain,'power_budget_W':budget,'status':'completed',**metrics})
            except ValidationError as e:
                rows.append({'volume_gain':gain,'power_budget_W':budget,'status':'domain_failure','reason':str(e)})
    completed=[x for x in rows if x['status']=='completed']
    front=[]
    for a in completed:
        if not any(b['coupled_energy_J']<=a['coupled_energy_J'] and b['declared_box_time_fraction']>=a['declared_box_time_fraction'] and
                   (b['coupled_energy_J']<a['coupled_energy_J'] or b['declared_box_time_fraction']>a['declared_box_time_fraction']) for b in completed):
            front.append({'volume_gain':a['volume_gain'],'power_budget_W':a['power_budget_W']})
    return result('Finite-horizon constraint and Pareto screening',{'tested_configurations':12,'completed':len(completed),'nondominated':len(front)},rows,
                  notes=['Enumeration of 12 fixed gain/budget settings under one known disturbance. This is not an infinite-horizon viability kernel.',
                         'Pareto comparison retains time inside the declared box and coupled energy as separate objectives; no clinical optimum is inferred.']) | {'pareto_configurations':front}


def equilibrium(p):
    r=simulate({'duration_min':120.,'dt_min':p['dt_min'],'events':[],'controller':'fixed'})
    return result('Steady inputs and explicit stock-flow conservation',r['metrics'],
                  series=[series('Volume',[x['time_min'] for x in r['trajectory']],[x['volume_L'] for x in r['trajectory']],'min','L')],
                  notes=r['assumptions'])


def dynamic_lab(p):
    r=simulate(p)
    return result('Regulated compartment under a declared perturbation',r['metrics'],
                  series=[series('Volume',[x['time_min'] for x in r['trajectory']],[x['volume_L'] for x in r['trajectory']],'min','L')],
                  notes=r['assumptions']) | {'simulation':r}


from .calibration import calibrate, synthetic_observations

LABS={
    'balance':('Stock-flow balance',equilibrium,{'dt_min':.5},['1.2','1.5']),
    'physical-budget':('Physical budget',lambda p: calculate('transport_energy',p),calc_defaults()['transport_energy'],['2.5', '8.17']),
    'membrane':('Membrane exchange',membrane,{'conductance_L_min':.05,'volume_A_L':1.,'volume_B_L':2.,'initial_A_mmol_L':100.,'initial_B_mmol_L':10.},['3.2', '3.17']),
    'geometry':('Size and diffusion',geometry,{'diffusivity_m2_s':1e-9},['4.1', '4.16']),
    'habitats':('Alternative water budgets',habitats,{'daily_osmoles_mOsm':600.,'available_water_L':1.5},['5.17', '9.17']),
    'branching':('Branching networks',branching,{'generations':8,'radius_ratio':.8,'length_ratio':.8},['6.16']),
    'filtration':('Filtration accounting',lambda p:calculate('filtration',p),calc_defaults()['filtration'],['7.15']),
    'transport':('Hidden transport work',transport,{'excreted_mmol_min':.1,'low_filtered_mmol_min':8.,'high_filtered_mmol_min':16.,'active_fraction':.6},['8.15','8.17','18.8']),
    'concentration':('Concentration and clearance',lambda p:calculate('clearance',p),calc_defaults()['clearance'],['9.15']),
    'acid':('Acid excretion budget',lambda p:calculate('acid',p),calc_defaults()['acid'],['10.15']),
    'signal':('Correspondence and delay',signal_experiment,{'samples':500,'seed':98,'error_probability':.1,'delay_steps':8},['11.19','16.22','16.23']),
    'memory':('A hidden history state',memory,{'decay_rate':.01,'legacy_load':.8},['12.5', '12.17', '18.11']),
    'repair':('Recovery at two timescales',repair,{'slow_repair_rate':.005,'fast_repair_rate':.04},['13.5','13.15']),
    'replacement':('Function-vector replacement',replacement,{'solute_clearance_fraction':.95},['14.17', '18.14']),
    'identifiability':('Competing mechanism design',identifiability,{'noise_sd':.3,'horizon_min':180.},['15.4','15.8','15.19']),
    'energy-information':('Energy and information units',lambda p:calculate('landauer',p),calc_defaults()['landauer'],['16.12']),
    'scales':('Conditional physical limits',lambda p:calculate('scales',p),calc_defaults()['scales'],['17.5','17.7','17.9']),
    'evidence':('Research correction graph',evidence_lab,{'withdraw_id':'synthetic-flux'},['18.13','18.20']),
    'ablation':('Contract-check ablation',ablation,{},['18.13']),
    'hypothesis':('Held-out added-effect test',hypothesis,{'seed':98,'noise_sd':.2,'injected_amplitude':.6},['16.24','18.18','18.19']),
    'uncertainty':('Parameter ensemble',uncertainty,{'samples':20,'seed':98},['15.9']),
    'viability':('Finite-horizon screening',viability,{'duration_min':240.},['18.16']),
    'dynamics':('Conservative regulated model',dynamic_lab,{},['11.15','15.3']),
    'calibration':('Fit an explicitly supplied research curve',calibrate,{'observations':synthetic_observations(),'source':{'id':'SYN-CURVE-01','kind':'synthetic','locator':'calibration.synthetic_observations','rights_confirmed':True},'k_min_per_min':.005,'k_max_per_min':.05,'css_min_mmol_L':5.,'css_max_mmol_L':15.,'grid_size':61},['15.4','15.7','15.10']),
}


def catalog():
    from copy import deepcopy
    return [{'id':key,'title':v[0],'defaults':deepcopy(v[2]),'book_sections':v[3]} for key,v in LABS.items()]


def run_experiment(name: str, overrides: dict | None = None) -> dict:
    if name not in LABS: raise ValidationError(f'Unknown experiment: {name}')
    title,fn,defaults,sections=LABS[name]
    if overrides is None: overrides={}
    if name=='dynamics': params=model_config(overrides)
    else:
        object_keys(overrides,set(defaults))
        params={**defaults,**overrides}
    report=fn(params)
    report.update({'experiment':name,'book_sections':sections,'parameters':params})
    return report
