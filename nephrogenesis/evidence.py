"""Typed evidence DAG, explicit inferential limits and transitive invalidation."""
from __future__ import annotations
from copy import deepcopy
from .common import ValidationError, object_keys
ROLES={'D','I','K','W','P'}
KINDS={'book','empirical','formal','synthetic','hypothesis','derived'}


def validate_graph(graph: dict) -> dict:
    object_keys(graph,{'nodes'},{'nodes'})
    nodes=graph['nodes']
    if not isinstance(nodes,list) or len(nodes)>1000: raise ValidationError('Expected at most 1000 evidence nodes')
    index={}
    for node in nodes:
        object_keys(node,{'id','kind','role','text','depends_on','status','source','requires','provides'}, {'id','kind','role','text','depends_on','status'})
        if not isinstance(node['id'],str) or not node['id'] or node['id'] in index:
            raise ValidationError('Duplicate or empty evidence identifier')
        if node['kind'] not in KINDS or node['role'] not in ROLES:
            raise ValidationError('Unknown evidence kind or DIKWP role')
        if node['status'] not in {'active','withdrawn','stale'}: raise ValidationError('Invalid evidence status')
        if not isinstance(node['text'],str) or not isinstance(node['depends_on'],list) or not all(isinstance(x,str) for x in node['depends_on']):
            raise ValidationError('Invalid evidence text/dependencies')
        for key in ('requires','provides'):
            if not isinstance(node.get(key,[]),list) or not all(isinstance(x,str) for x in node.get(key,[])):
                raise ValidationError('Invalid evidence contract')
        if node['kind'] in {'empirical','book','formal'} and not node.get('source'):
            raise ValidationError('External/formal evidence requires an explicit source locator')
        index[node['id']]=node
    order=[]; colors={}
    def visit(key):
        if key not in index: raise ValidationError(f'Missing dependency: {key}')
        if colors.get(key)==1: raise ValidationError('Evidence dependency cycle')
        if colors.get(key)==2: return
        colors[key]=1
        for parent in index[key]['depends_on']: visit(parent)
        colors[key]=2; order.append(key)
    try:
        for key in index: visit(key)
    except RecursionError as exc: raise ValidationError('Evidence dependency depth is too large') from exc
    ancestry={}; valid={}; reasons={}
    for key in order:
        node=index[key]; parents=node['depends_on']; inherited=set()
        for parent in parents: inherited.update(ancestry[parent]); inherited.add(index[parent]['kind'])
        ancestry[key]=inherited
        why=[]
        if node['status']!='active': why.append(node['status'])
        if any(not valid[p] for p in parents): why.append('invalid_dependency')
        if node['kind']=='empirical' and inherited.intersection({'synthetic','hypothesis'}):
            why.append('synthetic_or_hypothesis_cannot_establish_empirical_status')
        provided={v for p in parents for v in index[p].get('provides',[])}
        if set(node.get('requires',[]))-provided: why.append('unsatisfied_input_contract')
        valid[key]=not why; reasons[key]=why
    return {'valid':all(valid.values()),'topological_order':order,'node_validity':valid,'reasons':reasons,
            'note':'A valid graph verifies declared structure and status, not the truth of an external source.'}


def withdraw(graph: dict, node_id: str) -> dict:
    validate_graph(graph)
    result=deepcopy(graph); ids={n['id'] for n in result['nodes']}
    if node_id not in ids: raise ValidationError('Unknown node to withdraw')
    affected={node_id}
    changed=True
    while changed:
        changed=False
        for n in result['nodes']:
            if n['id'] not in affected and set(n['depends_on']) & affected:
                affected.add(n['id']); changed=True
    for n in result['nodes']:
        if n['id']==node_id: n['status']='withdrawn'
        elif n['id'] in affected: n['status']='stale'
    return {'graph':result,'affected':sorted(affected),'validation':validate_graph(result)}


def demonstration_graph() -> dict:
    return {'nodes':[
        {'id':'question','kind':'derived','role':'P','text':'Can equal sodium output conceal unequal ideal transport work?','depends_on':[],'status':'active'},
        {'id':'book-8.17','kind':'book','role':'K','text':'Ideal sodium / ATP coupling budget.','depends_on':[], 'status':'active','source':'A Brief History of the Kidney, section 8.17'},
        {'id':'synthetic-flux','kind':'synthetic','role':'D','text':'Declared mmol/min rates; not patient observations.','depends_on':['question'],'status':'active','provides':['sodium_mol_s']},
        {'id':'conversion','kind':'derived','role':'I','text':'Make the unit conversion and model boundary explicit.','depends_on':['synthetic-flux'],'status':'active','requires':['sodium_mol_s'],'provides':['typed_flux']},
        {'id':'calculation','kind':'derived','role':'K','text':'Compute conditional work under fixed stoichiometry.','depends_on':['conversion','book-8.17'],'status':'active','requires':['typed_flux'],'provides':['conditional_work']},
        {'id':'interpretation','kind':'derived','role':'W','text':'Compare costs without calling either scenario a treatment.','depends_on':['calculation'],'status':'active','requires':['conditional_work']},
        {'id':'revised-question','kind':'derived','role':'P','text':'Which additional flux measurement distinguishes mechanisms?','depends_on':['interpretation'],'status':'active'},
    ]}
