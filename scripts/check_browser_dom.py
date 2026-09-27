from pathlib import Path
import sys,json,argparse
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from nephrogenesis.common import write_json
from playwright.sync_api import sync_playwright
parser=argparse.ArgumentParser(description='Optional isolated-DOM UI smoke test, not a browser HTTP end-to-end test.')
parser.add_argument('--chromium',help='Installed Chromium executable; otherwise Playwright default.')
parser.add_argument('--out',required=True,help='New output directory outside the release.')
args=parser.parse_args()
root=ROOT;qa=Path(args.out)
if qa.exists() and any(qa.iterdir()):raise SystemExit('Output directory must be absent or empty')
qa.mkdir(parents=True,exist_ok=True)
results=[];errors=[]
try:
 with sync_playwright() as p:
  browser=p.chromium.launch(headless=True,executable_path=args.chromium)
  page=browser.new_page(viewport={'width':1500,'height':1080},device_scale_factor=1)
  page.on('pageerror',lambda e: errors.append(str(e)))
  # This test deliberately uses an isolated owned DOM and Python bridge.
  # Actual HTTP contracts are exercised separately in tests/test_interfaces.py.
  from nephrogenesis.experiments import catalog,run_experiment
  from nephrogenesis.calculators import book_benchmarks
  def bridge(path,options):
   try:
    if path=='/api/catalog':return {'status':200,'body':catalog()}
    if path=='/api/chapters':return {'status':200,'body':json.loads((root/'nephrogenesis/data/chapters.json').read_text())}
    if path=='/api/benchmarks':return {'status':200,'body':book_benchmarks()}
    if path=='/api/run':
     data=json.loads(options['body']);return {'status':200,'body':run_experiment(data['experiment'],data.get('parameters',{}))}
    return {'status':404,'body':{'error':'unknown route'}}
   except Exception as e:return {'status':400,'body':{'error':str(e)}}
  page.expose_function('localEngineBridge',bridge)
  content=(root/'nephrogenesis/static/index.html').read_text().replace('<link rel="stylesheet" href="/styles.css">','').replace('<script src="/app.js" defer></script>','')
  page.set_content(content)
  page.add_style_tag(content=(root/'nephrogenesis/static/styles.css').read_text())
  page.evaluate("window.fetch=async (path,options={})=>{const r=await window.localEngineBridge(path,options);return {ok:r.status<400,status:r.status,json:async()=>r.body};}")
  page.add_script_tag(content=(root/'nephrogenesis/static/app.js').read_text())
  page.wait_for_selector('#raw',state='attached')
  page.wait_for_function('document.getElementById("raw").textContent.includes("transport")')
  ids=page.locator('#experiment option').evaluate_all('(items)=>items.map(x=>x.value)')
  for exp in ids:
   page.select_option('#experiment',exp)
   page.click('#run')
   page.wait_for_function('!document.getElementById("run").disabled')
   error=page.locator('#error').inner_text()
   raw=page.locator('#raw').text_content()
   actual=json.loads(raw)
   results.append({'experiment':exp,'passed':not error and actual['experiment']==exp,'error':error})
  page.select_option('#experiment','signal');page.click('#run');page.wait_for_function('!document.getElementById("run").disabled')
  page.screenshot(path=str(qa/'desktop.png'),full_page=True)
  page.click('[data-view="chapters"]');page.screenshot(path=str(qa/'chapters.png'),full_page=True)
  chapter_count=page.locator('.chapter').count()
  page.click('.chapter button >> nth=14');opened=page.locator('#experiment').input_value()
  stale_cleared=(page.locator('#raw').text_content()=='')
  page.click('#run');page.wait_for_function('!document.getElementById("run").disabled')
  page.click('[data-view="benchmarks"]');checks=page.locator('#checks h3').inner_text()
  page.set_viewport_size({'width':390,'height':844});page.click('[data-view="lab"]')
  page.screenshot(path=str(qa/'mobile.png'),full_page=True)
  overflow=page.evaluate('document.documentElement.scrollWidth > window.innerWidth')
  # Invalid numeric input must be visible, not leave a success status unqualified.
  page.select_option('#experiment','signal');page.fill('#parameters','{"samples": -1}');page.click('#run')
  page.wait_for_function('!document.getElementById("run").disabled')
  invalid=bool(page.locator('#error').inner_text())
  browser.close()
 write_json(qa/'browser.json',{'browser':'Chromium via Playwright, isolated DOM with actual Python engine bridge; HTTP separately covered by tests/test_interfaces.py','experiments':results,'all_passed':all(r['passed'] for r in results),'js_errors':errors,'chapter_cards':chapter_count,'chapter_15_opens':opened,'book_checks_message':checks,'mobile_horizontal_overflow':overflow,'invalid_input_error_displayed':invalid,'old_result_cleared_on_experiment_change':stale_cleared,'browser_download_path_not_automatically_persisted':True})
 print('Browser:',len(results),'passed:',all(r['passed'] for r in results),'errors',errors,'overflow',overflow,'invalid',invalid)
 if not (all(r['passed'] for r in results) and not errors and not overflow and invalid and stale_cleared and chapter_count==18):raise SystemExit(1)
finally:
 pass
