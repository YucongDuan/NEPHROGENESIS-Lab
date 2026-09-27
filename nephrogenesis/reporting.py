"""Offline HTML reports; all dynamic strings are escaped, no network resources."""
from __future__ import annotations
import html
import json
from .common import canonical


def chart(series):
    if not series: return ''
    # Compare only compatible axes. Other units remain available in the full result.
    first=series[0]; selected=[s for s in series if s['x_unit']==first['x_unit'] and s['y_unit']==first['y_unit']]
    xs=[v for s in selected for v in s['x']]; ys=[v for s in selected for v in s['y']]
    if not xs or not ys: return ''
    lo,hi=min(ys),max(ys); left,right=min(xs),max(xs)
    if hi==lo: hi=lo+1
    if right==left: right=left+1
    colors=['#245c78','#b35d32','#51844e','#8754a1','#525b66','#c18c1c']
    paths=[]; labels=[]
    for i,s in enumerate(selected):
        points=' '.join(f'{45+(x-left)/(right-left)*650:.2f},{240-(y-lo)/(hi-lo)*205:.2f}' for x,y in zip(s['x'],s['y']))
        paths.append(f'<polyline fill="none" stroke="{colors[i%6]}" stroke-width="2" points="{points}"/>')
        labels.append(f'<span>{html.escape(s["name"])}</span>')
    return f'<figure><svg viewBox="0 0 730 280" role="img" aria-label="Experiment trajectory"><path d="M45 25V240H700" fill="none" stroke="#879299"/>'+''.join(paths)+f'<text x="45" y="270">{left:g} to {right:g} {html.escape(first["x_unit"])}</text><text x="45" y="20">{lo:.5g} to {hi:.5g} {html.escape(first["y_unit"])}</text></svg><figcaption>'+ ' | '.join(labels)+'</figcaption></figure>'


def report_html(reports: list[dict], title='NEPHROGENESIS-Lab | Experiment Report') -> str:
    body=[]
    for report in reports:
        metrics=report.get('metrics',report.get('outputs',{}))
        cards=''.join(f'<div><b>{html.escape(k.replace("_"," "))}</b><p>{html.escape(str(v))}</p></div>' for k,v in metrics.items())
        rows=report.get('rows',[])
        table=''
        if rows:
            keys=list(dict.fromkeys(k for r in rows for k in r))
            table='<div class="scroll"><table><tr>'+''.join(f'<th>{html.escape(k)}</th>' for k in keys)+'</tr>'
            table+=''.join('<tr>'+''.join(f'<td>{html.escape(str(r.get(k,"")))}</td>' for k in keys)+'</tr>' for r in rows[:200])+'</table></div>'
            if len(rows)>200: table+=f'<p>Showing 200 of {len(rows)} rows. The complete run JSON / CSV retains every row.</p>'
        notes=report.get('notes',report.get('assumptions',[]))
        body.append('<section><h2>'+html.escape(report.get('title',report.get('experiment',report.get('calculator','Experiment'))))+'</h2><p class="tag">'+html.escape(report.get('status',''))+'</p><div class="metrics">'+cards+'</div>'+chart(report.get('series',[]))+table+''.join('<p class="note">'+html.escape(n)+'</p>' for n in notes)+'<details><summary>Parameters, full result and source sections</summary><pre>'+html.escape(json.dumps(report,indent=2,ensure_ascii=True))+'</pre></details></section>')
    return '''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'''+html.escape(title)+'''</title><style>
body{font:16px/1.65 system-ui,sans-serif;color:#23313b;background:#eef2f4;margin:0}main{max-width:1120px;margin:auto;padding:38px 24px}header{background:#183f53;color:white;padding:35px}h1{font-size:38px;line-height:1.15}h2{font-size:25px}section{background:white;padding:28px;margin:24px 0;border:1px solid #dbe2e5}.tag{font:13px monospace;color:#526879}.metrics{display:flex;gap:12px;flex-wrap:wrap}.metrics div{padding:12px;border:1px solid #dbe2e5;min-width:150px;max-width:300px;overflow-wrap:anywhere}.metrics b{font-size:13px}.metrics p{margin:8px 0;font-size:19px}.note{border-left:3px solid #b35d32;padding-left:14px}pre{white-space:pre-wrap;font:12px/1.45 monospace;overflow-wrap:anywhere}svg{width:100%;max-height:360px}table{border-collapse:collapse;font-size:13px}td,th{padding:8px;border-bottom:1px solid #dbe2e5;text-align:left;white-space:nowrap}.scroll{overflow:auto}figcaption{font-size:13px;color:#526879}details{margin-top:18px}a{color:inherit}</style></head><body><header><p>BOOK COMPANION / EXECUTABLE SCIENCE</p><h1>NEPHROGENESIS-Lab</h1><p>Energy, information and the maintenance of viable differences.</p><p>Synthetic research and education. No clinical decision support or proof of a new physical field.</p></header><main>'''+''.join(body)+'''<footer>Local, reproducible output. Integrity receipts detect changes relative to an independently preserved trust anchor; they do not establish scientific truth.</footer></main></body></html>'''
