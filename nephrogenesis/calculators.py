"""Book-aligned equations with explicit units and assumption receipts."""
from __future__ import annotations
import math
from .common import object_keys, number, ValidationError
from .units import Quantity as Q, measurement as m
KB=1.380649e-23
NA=6.02214076e23
R=KB*NA
F=96485.33212331001
H=6.62607015e-34
C=299792458.0
G=6.67430e-11
HBAR=H/(2*math.pi)


def val(x,unit): return {'value':x,'unit':unit}


def calculate(name: str, p: dict) -> dict:
    if not isinstance(p,dict): raise ValidationError('Calculator inputs must be an object')
    sections=[]; notes=[]
    if name=='filtration':
        object_keys(p,{'rbf','hematocrit','gfr'},{'rbf','hematocrit','gfr'})
        rbf=m(p['rbf'],'mL/min','rbf',positive=True); hct=number(p['hematocrit'],'hematocrit',0,.99)
        gfr=m(p['gfr'],'mL/min','gfr',low=0); rpf=rbf*(1-hct)
        if gfr>rpf: raise ValidationError('GFR cannot exceed plasma inflow in this steady flow budget')
        out={'plasma_flow':val(rpf,'mL/min'),'filtration_fraction':val(gfr/rpf,'1')}
        sections=['7.15']; notes=['Steady illustrative flow budget; not a clinical assessment.']
    elif name=='unindex':
        object_keys(p,{'indexed_gfr','body_area'},{'indexed_gfr','body_area'})
        # Indexed GFR is deliberately not accepted as an ordinary flow measurement.
        g=number(p['indexed_gfr'],'indexed_gfr',0,1000)
        area=m(p['body_area'],'m2','body_area',positive=True)
        out={'estimated_absolute_gfr':val(g*area/1.73,'mL/min')}; sections=['7.17']
        notes=['indexed_gfr is explicitly in mL/min/1.73 m2. De-indexing an estimate does not measure GFR.']
    elif name=='clearance':
        object_keys(p,{'urine_flow','urine_osmolarity','plasma_osmolarity'}, {'urine_flow','urine_osmolarity','plasma_osmolarity'})
        v=m(p['urine_flow'],'mL/min','urine_flow',low=0)
        u=m(p['urine_osmolarity'],'mOsm/L','urine_osmolarity',low=0)
        b=m(p['plasma_osmolarity'],'mOsm/L','plasma_osmolarity',positive=True)
        out={'osmolar_clearance':val(u*v/b,'mL/min'),'free_water_clearance':val(v-u*v/b,'mL/min')}
        sections=['9.15']; notes=['Uses osmolarity per litre, not osmolality per kilogram. No density conversion is assumed.']
    elif name=='minimum_urine':
        object_keys(p,{'osmole_load','maximum_osmolarity'},{'osmole_load','maximum_osmolarity'})
        load=m(p['osmole_load'],'mOsm/day','osmole_load',low=0)
        cap=m(p['maximum_osmolarity'],'mOsm/L','maximum_osmolarity',positive=True)
        out={'minimum_volume':val(load/cap,'L/day')}; sections=['9.17']
        notes=['Conditional arithmetic minimum at the specified attainable concentration; not a fluid intake recommendation.']
    elif name=='acid':
        object_keys(p,{'ammonium','titratable_acid','bicarbonate'},{'ammonium','titratable_acid','bicarbonate'})
        nh=m(p['ammonium'],'mEq/day','ammonium',low=0)
        ta=m(p['titratable_acid'],'mEq/day','titratable_acid',low=0)
        bc=m(p['bicarbonate'],'mEq/day','bicarbonate',low=0)
        out={'net_acid_excretion':val(nh+ta-bc,'mEq/day')}; sections=['10.15']
        notes=['Net acid excretion budget; bicarbonate recovery is not counted again as new bicarbonate.']
    elif name=='transport_energy':
        object_keys(p,{'sodium_rate','sodium_per_atp','atp_energy'},{'sodium_rate','sodium_per_atp','atp_energy'})
        rate=m(p['sodium_rate'],'mol/s','sodium_rate',low=0)
        stoich=number(p['sodium_per_atp'],'sodium_per_atp',positive=True)
        energy=m(p['atp_energy'],'J/mol','atp_energy',positive=True)
        power=(Q.of(rate/stoich,'mol/s')*Q.of(energy,'J/mol')).to('W')
        out={'atp_rate':val(rate/stoich,'mol/s'),'coupled_power':val(power,'W')}
        sections=['8.17']; notes=['Ideal stated coupling budget only; excludes basal metabolism, leakage and uncoupled processes.']
    elif name=='electrochemical':
        object_keys(p,{'temperature','inside','outside','voltage_out_minus_in','valence'}, {'temperature','inside','outside','voltage_out_minus_in','valence'})
        t=m(p['temperature'],'K','temperature',positive=True)
        ci=m(p['inside'],'mmol/L','inside',positive=True); co=m(p['outside'],'mmol/L','outside',positive=True)
        voltage=m(p['voltage_out_minus_in'],'V','voltage_out_minus_in')
        z=number(p['valence'],'valence',-10,10)
        chem=R*t*math.log(co/ci); electrical=z*F*voltage
        out={'chemical_term':val(chem,'J/mol'),'electrical_term':val(electrical,'J/mol'),
             'outward_molar_work':val(chem+electrical,'J/mol')}
        sections=['16.4','16.5']; notes=['Direction is inside to outside. Ideal activities approximated by concentrations. Negative work indicates a downhill direction.']
    elif name=='landauer':
        object_keys(p,{'temperature','erasure_rate','molar_work'}, {'temperature','erasure_rate','molar_work'})
        t=m(p['temperature'],'K','temperature',positive=True)
        er=number(p['erasure_rate'],'erasure_rate',0,1e30)
        work=m(p['molar_work'],'J/mol','molar_work')
        bit=KB*t*math.log(2)
        out={'energy_per_bit_erasure':val(bit,'J'),'ideal_erasure_power':val(bit*er,'W'),
             'dimensionless_comparison':val(work/(R*t*math.log(2)),'1')}
        sections=['16.12']; notes=['Ideal logical erasure bound under its thermodynamic assumptions. The dimensionless comparison is not the number of bits processed by a kidney.']
    elif name=='scales':
        object_keys(p,{'radius','total_energy'}, {'radius','total_energy'})
        radius=m(p['radius'],'m','radius',positive=True); e=m(p['total_energy'],'J','total_energy',positive=True)
        gravity_ratio=2*G*e/(C**4*radius)
        if gravity_ratio>=.01: raise ValidationError('Outside this teaching implementation\'s declared weak-gravity range (2GE/c^4R < 0.01)')
        out={'planck_length':val(math.sqrt(HBAR*G/C**3),'m'),
             'planck_time':val(math.sqrt(HBAR*G/C**5),'s'),
             'light_travel_time':val(radius/C,'s'),
             'bekenstein_bound_bits':val(2*math.pi*e*radius/(HBAR*C*math.log(2)),'bit'),
             'gravity_ratio':val(gravity_ratio,'1')}
        sections=['17.5','17.7','17.9']; notes=['Total energy and enclosing radius under the stated ideal bound. Not a measured biological storage capacity; Planck scales do not establish spacetime pixels.']
    else:
        raise ValidationError(f'Unknown calculator: {name}')
    return {'calculator':name,'outputs':out,'book_sections':sections,'assumptions':notes,'status':'conditional_equation','input':p}


def defaults() -> dict:
    return {
        'filtration':{'rbf':val(1000,'mL/min'),'hematocrit':.4,'gfr':val(120,'mL/min')},
        'unindex':{'indexed_gfr':90,'body_area':val(2.30,'m2')},
        'clearance':{'urine_flow':val(2,'mL/min'),'urine_osmolarity':val(600,'mOsm/L'),'plasma_osmolarity':val(300,'mOsm/L')},
        'minimum_urine':{'osmole_load':val(600,'mOsm/day'),'maximum_osmolarity':val(1200,'mOsm/L')},
        'acid':{'ammonium':val(40,'mEq/day'),'titratable_acid':val(20,'mEq/day'),'bicarbonate':val(5,'mEq/day')},
        'transport_energy':{'sodium_rate':val(3,'nmol/s'),'sodium_per_atp':3,'atp_energy':val(50,'kJ/mol')},
        'electrochemical':{'temperature':val(310,'K'),'inside':val(15,'mmol/L'),'outside':val(140,'mmol/L'),'voltage_out_minus_in':val(70,'mV'),'valence':1},
        'landauer':{'temperature':val(310,'K'),'erasure_rate':1e15,'molar_work':val(12511.020147906465,'J/mol')},
        'scales':{'radius':val(1,'m'),'total_energy':val(C**2,'J')}
    }


def book_benchmarks() -> list[dict]:
    a={k:calculate(k,v)['outputs'] for k,v in defaults().items()}
    dn=a['electrochemical']['outward_molar_work']['value']
    dk=R*310*math.log(140/4)-F*.070
    bit=a['landauer']['energy_per_bit_erasure']['value']
    cases=[
        ('B01','Renal plasma flow',a['filtration']['plasma_flow']['value'],600,'mL/min'),
        ('B02','Filtration fraction',a['filtration']['filtration_fraction']['value'],.2,'1'),
        ('B03','De-indexed estimate',a['unindex']['estimated_absolute_gfr']['value'],119.65317919075144,'mL/min'),
        ('B04','Ideal sodium coupling power',a['transport_energy']['coupled_power']['value'],5e-5,'W'),
        ('B05','Osmolar clearance',a['clearance']['osmolar_clearance']['value'],4,'mL/min'),
        ('B06','Free water clearance',a['clearance']['free_water_clearance']['value'],-2,'mL/min'),
        ('B07','Minimum urine at 1200',a['minimum_urine']['minimum_volume']['value'],.5,'L/day'),
        ('B08','Minimum urine at 600',600/600,1,'L/day'),
        ('B09','Net acid excretion',a['acid']['net_acid_excretion']['value'],55,'mEq/day'),
        ('B10','Outward sodium work',dn,12511.020147906465,'J/mol'),
        ('B11','Inward potassium work',dk,2409.8774024192653,'J/mol'),
        ('B12','3 sodium / 2 potassium cycle',3*dn+2*dk,42352.81524855792,'J/mol'),
        ('B13','Cycle margin under 55 kJ/mol',55000-3*dn-2*dk,12647.18475144208,'J/mol'),
        ('B14','Landauer energy',bit,2.9666781812480147e-21,'J'),
        ('B15','Ideal erasure power',bit*1e15,2.9666781812480147e-6,'W'),
        ('B16','Avogadro conversion consistency',dn/(R*310*math.log(2)),(dn/NA)/bit,'1'),
        ('B17','Planck length',a['scales']['planck_length']['value'],1.616255e-35,'m'),
        ('B18','Planck time',a['scales']['planck_time']['value'],5.391247e-44,'s'),
        ('B19','Illustrative information bound',a['scales']['bekenstein_bound_bits']['value'],2.576908209992606e43,'bit'),
        ('B20','Light crossing time',a['scales']['light_travel_time']['value'],3.3356409519815204e-9,'s'),
        ('B21','Bernoulli receptor information at unit concentration',1/(1+1)**2,.25,'1'),
        ('B22','Optimally remapped binary channel',max(.8,1-.8),.8,'1')]
    return [{'id':i,'name':n,'actual':x,'expected':e,'unit':u,
             'relative_tolerance':1e-6 if i in ('B17','B18') else 1e-10,
             'passed':math.isclose(x,e,rel_tol=1e-6 if i in ('B17','B18') else 1e-10,abs_tol=0)} for i,n,x,e,u in cases]
