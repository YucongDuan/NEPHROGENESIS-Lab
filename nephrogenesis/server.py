"""Loopback-only single-user teaching server. Not a production hosting stack."""
from __future__ import annotations
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from pathlib import Path
import json
from .common import ValidationError, canonical, integer
from .experiments import catalog, run_experiment
from .calculators import book_benchmarks
STATIC=Path(__file__).parent/'static'
DATA=Path(__file__).parent/'data'
ASSETS={'/':('index.html','text/html; charset=utf-8'),'/index.html':('index.html','text/html; charset=utf-8'),
        '/app.js':('app.js','text/javascript; charset=utf-8'),'/styles.css':('styles.css','text/css; charset=utf-8')}


class Handler(BaseHTTPRequestHandler):
    server_version='NephrogenesisLocal/1.0'
    sys_version=''
    timeout=5

    def log_message(self,fmt,*args):
        pass # No patient-like or request data are logged by the local server.

    def _allowed(self):
        authorities={f'127.0.0.1:{self.server.server_port}',f'localhost:{self.server.server_port}'}
        if self.headers.get('Host') not in authorities: return False
        origin=self.headers.get('Origin')
        return origin is None or origin in {f'http://{x}' for x in authorities}

    def _reply(self,status,payload,content_type='application/json; charset=utf-8'):
        if not isinstance(payload,bytes): payload=canonical(payload).encode()
        self.send_response(status)
        self.send_header('Content-Type',content_type)
        self.send_header('Content-Length',str(len(payload)))
        self.send_header('Cache-Control','no-store')
        self.send_header('X-Content-Type-Options','nosniff')
        self.send_header('Referrer-Policy','no-referrer')
        self.send_header('Content-Security-Policy',"default-src 'self'; script-src 'self'; style-src 'self'; connect-src 'self'; img-src 'self' data:; object-src 'none'; frame-ancestors 'none'; base-uri 'none'")
        self.end_headers(); self.wfile.write(payload)

    def do_GET(self):
        if not self._allowed(): return self._reply(403,{'error':'Only the local origin is allowed'})
        if self.path in ASSETS:
            name,mime=ASSETS[self.path]
            return self._reply(200,(STATIC/name).read_bytes(),mime)
        if self.path=='/api/catalog': return self._reply(200,catalog())
        if self.path=='/api/benchmarks': return self._reply(200,book_benchmarks())
        if self.path=='/api/chapters': return self._reply(200,json.loads((DATA/'chapters.json').read_text()))
        if self.path=='/api/health': return self._reply(200,{'status':'ok','mode':'local_research','version':'1.0.0'})
        return self._reply(404,{'error':'Unknown path'})

    def do_POST(self):
        if not self._allowed() or self.headers.get('X-Nephro-Request')!='local':
            return self._reply(403,{'error':'Local-origin request header required'})
        if self.path!='/api/run': return self._reply(404,{'error':'Unknown operation'})
        if self.headers.get('Transfer-Encoding'):
            return self._reply(400,{'error':'Transfer encoding is not supported'})
        if self.headers.get('Content-Type','').split(';')[0]!='application/json':
            return self._reply(415,{'error':'application/json required'})
        try:
            length=int(self.headers.get('Content-Length','-1'))
            if not 0<length<=32768: return self._reply(413,{'error':'Request must contain 1-32768 bytes'})
            raw=self.rfile.read(length)
            if len(raw)!=length: raise ValidationError('Incomplete request body')
            def reject(x): raise ValidationError(f'Invalid JSON constant: {x}')
            def pairs(items):
                d={}
                for k,v in items:
                    if k in d: raise ValidationError('Duplicate JSON keys')
                    d[k]=v
                return d
            data=json.loads(raw,parse_constant=reject,object_pairs_hook=pairs)
            if not isinstance(data,dict) or set(data)-{'experiment','parameters'} or 'experiment' not in data:
                raise ValidationError('Use experiment and parameters fields only')
            if not isinstance(data['experiment'],str): raise ValidationError('Experiment identifier must be a string')
            report=run_experiment(data['experiment'],data.get('parameters',{}))
            return self._reply(200,report)
        except (ValidationError,ValueError,TypeError,KeyError,OverflowError,RecursionError) as e:
            return self._reply(400,{'error':str(e)[:300]})
        except TimeoutError:
            return self._reply(408,{'error':'Request timed out'})


def make_server(port=8765):
    integer(port,'port',0,65535)
    return ThreadingHTTPServer(('127.0.0.1',port),Handler)


def serve(port=8765):
    with make_server(port) as httpd:
        print(f'NEPHROGENESIS-Lab: http://127.0.0.1:{httpd.server_port}',flush=True)
        print('Single-user research server. Keep local. Press Ctrl+C to stop.',flush=True)
        try: httpd.serve_forever()
        except KeyboardInterrupt: pass
