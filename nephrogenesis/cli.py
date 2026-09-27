"""Command-line entry points for reproducible laboratories."""
from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path
from .common import ValidationError, write_json, load_json
from .calculators import book_benchmarks, calculate, defaults
from .experiments import catalog, run_experiment
from .ledger import write_bundle, verify_bundle, replay
from .evidence import validate_graph, withdraw
from .reporting import report_html


def main(argv=None):
    parser=argparse.ArgumentParser(prog='nephrogenesis',description='Executable kidney-history companion; synthetic research only.')
    sub=parser.add_subparsers(dest='command',required=True)
    sub.add_parser('catalog'); sub.add_parser('verify')
    fit=sub.add_parser('fit'); fit.add_argument('--data',required=True);fit.add_argument('--metadata',required=True);fit.add_argument('--out',required=True)
    run=sub.add_parser('run'); run.add_argument('experiment'); run.add_argument('--config'); run.add_argument('--out',required=True)
    demo=sub.add_parser('demo'); demo.add_argument('--out',default='runs/demo')
    verify=sub.add_parser('verify-run'); verify.add_argument('directory'); verify.add_argument('--trusted-receipt')
    rep=sub.add_parser('replay'); rep.add_argument('directory')
    calc=sub.add_parser('calculate'); calc.add_argument('calculator'); calc.add_argument('--config'); calc.add_argument('--out')
    evidence=sub.add_parser('evidence'); evidence.add_argument('file'); evidence.add_argument('--withdraw'); evidence.add_argument('--out')
    server=sub.add_parser('serve'); server.add_argument('--port',type=int,default=8765)
    args=parser.parse_args(argv)
    try:
        if args.command=='catalog': output=catalog()
        elif args.command=='verify':
            checks=book_benchmarks(); output={'passed':all(x['passed'] for x in checks),'checks':checks}
            print(json.dumps(output,indent=2)); return 0 if output['passed'] else 1
        elif args.command=='fit':
            from .calibration import read_observations
            output=write_bundle('calibration',{'observations':read_observations(args.data),'source':load_json(args.metadata)},args.out)
        elif args.command=='run': output=write_bundle(args.experiment,load_json(args.config) if args.config else {},args.out)
        elif args.command=='demo':
            root=Path(args.out)
            if root.exists() and any(root.iterdir()): raise ValidationError('Demo output directory must be empty')
            reports=[]; receipts=[]
            for item in catalog():
                receipts.append(write_bundle(item['id'],{},root/item['id']))
                reports.append(load_json(root/item['id']/'result.json'))
            write_json(root/'summary.json',{'experiments':len(reports),'receipts':receipts})
            (root/'index.html').write_text(report_html(reports),encoding='utf-8')
            output={'experiments':len(reports),'report':str(root/'index.html'),'summary':str(root/'summary.json')}
        elif args.command=='verify-run': output=verify_bundle(args.directory,args.trusted_receipt)
        elif args.command=='replay':
            output=replay(args.directory)
            print(json.dumps(output,indent=2)); return 0 if output['replayed'] else 1
        elif args.command=='calculate':
            p=load_json(args.config) if args.config else defaults().get(args.calculator,{})
            output=calculate(args.calculator,p)
            if args.out: write_json(args.out,output)
        elif args.command=='evidence':
            g=load_json(args.file); output=withdraw(g,args.withdraw) if args.withdraw else validate_graph(g)
            if args.out: write_json(args.out,output)
        else:
            from .server import serve
            serve(args.port); return 0
        print(json.dumps(output,indent=2,ensure_ascii=True,allow_nan=False)); return 0
    except (ValidationError,OSError,ValueError,TypeError,KeyError) as e:
        print(f'Error: {e}',file=sys.stderr); return 2

if __name__=='__main__': raise SystemExit(main())
