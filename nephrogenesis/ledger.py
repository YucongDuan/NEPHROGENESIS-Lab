"""Deterministic local experiment receipts and recomputation verification.

Hashes detect changes against a trusted receipt. An attacker who can rewrite all
files and the receipt can re-seal a fabricated history; there is no signature or
external timestamp in this implementation.
"""
from __future__ import annotations
from pathlib import Path
import csv
import hashlib
import json
import math
from . import __version__
from .common import ValidationError, canonical, digest, source_digest, load_json, write_json
from .experiments import run_experiment


def build_chain(events: list[dict]) -> list[dict]:
    chain=[]; previous='0'*64
    for i,event in enumerate(events):
        payload={'sequence':i,'previous_hash':previous,'event':event}
        previous=digest(payload)
        chain.append({**payload,'hash':previous})
    return chain


def verify_chain(chain: list[dict], trusted_head: str | None = None) -> bool:
    if not isinstance(chain,list) or not chain: return False
    previous='0'*64
    for i,row in enumerate(chain):
        if not isinstance(row,dict) or set(row)!={'sequence','previous_hash','event','hash'}: return False
        payload={k:row[k] for k in ('sequence','previous_hash','event')}
        if row['sequence']!=i or row['previous_hash']!=previous or row['hash']!=digest(payload): return False
        previous=row['hash']
    return trusted_head is None or previous==trusted_head


def _safe_child(root: Path, name: str) -> Path:
    if not isinstance(name,str) or not name or name in {'.','..'} or '/' in name or '\\' in name:
        raise ValidationError('Receipt contains an unsafe filename')
    path=root/name
    if path.is_symlink() or path.resolve().parent != root.resolve():
        raise ValidationError('Receipt symlinks and path escapes are not allowed')
    return path


def export_csv(path: Path, report: dict) -> bool:
    rows=report.get('rows',[])
    if report.get('simulation'): rows=report['simulation']['trajectory']
    if not rows: return False
    fields=sorted(set().union(*(r.keys() for r in rows)))
    def safe(v):
        if isinstance(v,(list,dict)): return canonical(v)
        if isinstance(v,str) and v.startswith(('=','+','-','@','\t','\r')): return "'"+v
        return v
    with path.open('w',newline='',encoding='utf-8') as f:
        writer=csv.DictWriter(f,fieldnames=fields); writer.writeheader()
        for row in rows: writer.writerow({k:safe(v) for k,v in row.items()})
    return True


def write_bundle(name: str, parameters: dict, root: str | Path) -> dict:
    root=Path(root)
    if root.exists() and (not root.is_dir() or any(root.iterdir())):
        raise ValidationError('Output directory must be absent or empty; experiment bundles are not overwritten')
    report=run_experiment(name,parameters)
    root.mkdir(parents=True,exist_ok=True)
    protocol={'experiment':name,'parameters':report['parameters'],'software_version':__version__,'code_digest':source_digest()}
    chain=build_chain([
        {'role':'P','action':'declare_question','experiment':name},
        {'role':'D','action':'record_inputs','input_digest':digest(protocol),'evidence_kind':'synthetic_or_conditional'},
        {'role':'I','action':'bind_sections_and_units','book_sections':report['book_sections']},
        {'role':'K','action':'execute_model','result_digest':digest(report)},
        {'role':'W','action':'retain_limits','clinical_validation':False,'new_field_established':False},
        {'role':'P','action':'make_replayable','next_question':'What observation would falsify these assumptions?'}])
    write_json(root/'protocol.json',protocol); write_json(root/'result.json',report)
    (root/'ledger.jsonl').write_text(''.join(canonical(x)+'\n' for x in chain),encoding='utf-8')
    csv_created=export_csv(root/'table.csv',report)
    from .reporting import report_html
    (root/'report.html').write_text(report_html([report]),encoding='utf-8')
    files=['protocol.json','result.json','ledger.jsonl','report.html']+(['table.csv'] if csv_created else [])
    receipt={'format':'nephrogenesis-run-v1','code_digest':protocol['code_digest'],'ledger_head':chain[-1]['hash'],
             'files':{n:hashlib.sha256((root/n).read_bytes()).hexdigest() for n in files},
             'trust_model':'Local unkeyed hashes; external preservation of receipt digest is needed against complete rewriting.'}
    write_json(root/'receipt.json',receipt)
    return {'path':str(root),'receipt_digest':digest(receipt),'experiment':name,'result_digest':digest(report)}


def verify_bundle(root: str | Path, trusted_receipt_digest: str | None = None) -> dict:
    root=Path(root); receipt=load_json(_safe_child(root,'receipt.json'))
    if receipt.get('format')!='nephrogenesis-run-v1': raise ValidationError('Unknown run receipt format')
    if trusted_receipt_digest and digest(receipt)!=trusted_receipt_digest:
        raise ValidationError('Receipt does not match the supplied external trust anchor')
    files=receipt.get('files')
    if not isinstance(files,dict) or not {'protocol.json','result.json','ledger.jsonl','report.html'}<=set(files):
        raise ValidationError('Incomplete run receipt')
    for name,expected in files.items():
        path=_safe_child(root,name)
        if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest()!=expected:
            raise ValidationError(f'File digest mismatch: {name}')
    try:
        chain=[json.loads(x) for x in _safe_child(root,'ledger.jsonl').read_text().splitlines()]
    except (ValueError,RecursionError) as exc: raise ValidationError('Malformed ledger') from exc
    if len(chain)!=6 or not verify_chain(chain,receipt['ledger_head']): raise ValidationError('Broken or incomplete experiment ledger')
    protocol=load_json(root/'protocol.json'); report=load_json(root/'result.json')
    if chain[1]['event'].get('input_digest')!=digest(protocol) or chain[3]['event'].get('result_digest')!=digest(report):
        raise ValidationError('Ledger does not bind the actual protocol or result')
    if protocol.get('code_digest')!=receipt['code_digest']: raise ValidationError('Inconsistent code identity')
    return {'verified':True,'trusted_anchor_supplied':bool(trusted_receipt_digest),
            'receipt_digest':digest(receipt),'code_matches_current':source_digest()==receipt['code_digest']}


def numerical_equal(a,b,rtol=1e-10,atol=1e-12):
    if isinstance(a,bool) or isinstance(b,bool): return type(a)==type(b) and a==b
    if isinstance(a,(float,int)) and isinstance(b,(float,int)):
        return math.isclose(a,b,rel_tol=rtol,abs_tol=atol)
    if type(a)!=type(b): return False
    if isinstance(a,dict): return set(a)==set(b) and all(numerical_equal(a[k],b[k],rtol,atol) for k in a)
    if isinstance(a,list): return len(a)==len(b) and all(numerical_equal(x,y,rtol,atol) for x,y in zip(a,b))
    return a==b


def replay(root: str | Path) -> dict:
    check=verify_bundle(root)
    if not check['code_matches_current']: raise ValidationError('Model/code identity changed; re-run under the original release or create a new experiment')
    protocol=load_json(Path(root)/'protocol.json'); original=load_json(Path(root)/'result.json')
    actual=run_experiment(protocol['experiment'],protocol['parameters'])
    same=numerical_equal(actual,original)
    return {**check,'replayed':same,'identical_serialization':digest(actual)==digest(original),
            'relative_tolerance':1e-10,'absolute_tolerance':1e-12}
