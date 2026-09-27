import http.client
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import threading
import unittest
from nephrogenesis.server import make_server

class HTTPTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server=make_server(0);cls.port=cls.server.server_port
        cls.thread=threading.Thread(target=cls.server.serve_forever,daemon=True);cls.thread.start()
    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown();cls.server.server_close();cls.thread.join()
    def request(self,method,path,body=None,headers=None):
        c=http.client.HTTPConnection('127.0.0.1',self.port,timeout=5)
        c.request(method,path,body=body,headers=headers or {})
        r=c.getresponse();data=r.read();status=r.status;hdr=dict(r.getheaders());c.close();return status,data,hdr
    def post(self,p,headers=None):
        h={'Content-Type':'application/json','X-Nephro-Request':'local'};h.update(headers or {})
        return self.request('POST','/api/run',json.dumps(p),h)
    def test_health(self):self.assertEqual(self.request('GET','/api/health')[0],200)
    def test_index(self):self.assertIn(b'Experiment workbench',self.request('GET','/')[1])
    def test_assets(self):
        for p in ['/styles.css','/app.js']:self.assertEqual(self.request('GET',p)[0],200)
    def test_catalog(self):self.assertEqual(len(json.loads(self.request('GET','/api/catalog')[1])),24)
    def test_chapters(self):self.assertEqual(len(json.loads(self.request('GET','/api/chapters')[1])),18)
    def test_benchmarks(self):self.assertEqual(len(json.loads(self.request('GET','/api/benchmarks')[1])),22)
    def test_unknown_path(self):self.assertEqual(self.request('GET','/secrets')[0],404)
    def test_traversal(self):self.assertEqual(self.request('GET','/../README.md')[0],404)
    def test_foreign_host(self):self.assertEqual(self.request('GET','/',headers={'Host':'attacker.invalid'})[0],403)
    def test_foreign_origin(self):self.assertEqual(self.request('GET','/',headers={'Origin':'https://attacker.invalid'})[0],403)
    def test_no_cors(self):self.assertNotIn('Access-Control-Allow-Origin',self.request('GET','/')[2])
    def test_security_headers(self):
        h=self.request('GET','/')[2];self.assertEqual(h['X-Content-Type-Options'],'nosniff');self.assertIn("frame-ancestors 'none'",h['Content-Security-Policy'])
    def test_run(self):self.assertEqual(self.post({'experiment':'transport'})[0],200)
    def test_invalid_lab(self):self.assertEqual(self.post({'experiment':'prescribe'})[0],400)
    def test_invalid_param(self):self.assertEqual(self.post({'experiment':'signal','parameters':{'samples':-1}})[0],400)
    def test_missing_local_header(self):self.assertEqual(self.request('POST','/api/run','{}',{'Content-Type':'application/json'})[0],403)
    def test_wrong_content_type(self):self.assertEqual(self.post({'experiment':'transport'},{'Content-Type':'text/plain'})[0],415)
    def test_oversized(self):
        self.assertEqual(self.request('POST','/api/run','x'*40000,{'Content-Type':'application/json','X-Nephro-Request':'local'})[0],413)
    def test_duplicate_json_key(self):
        self.assertEqual(self.request('POST','/api/run','{"experiment":"signal","experiment":"transport"}',{'Content-Type':'application/json','X-Nephro-Request':'local'})[0],400)
    def test_nonfinite_json(self):
        self.assertEqual(self.request('POST','/api/run','{"experiment":"signal","parameters":{"samples":NaN}}',{'Content-Type':'application/json','X-Nephro-Request':'local'})[0],400)

class CLITests(unittest.TestCase):
    def invoke(self,*args):
        return subprocess.run([sys.executable,'-m','nephrogenesis',*args],capture_output=True,text=True,timeout=20)
    def test_verify(self):self.assertEqual(self.invoke('verify').returncode,0)
    def test_bad_command(self):self.assertEqual(self.invoke('run','not-real','--out','unused').returncode,2)
    def test_run_and_replay(self):
        with tempfile.TemporaryDirectory() as d:
            p=str(Path(d)/'experiment with spaces')
            self.assertEqual(self.invoke('run','identifiability','--out',p).returncode,0)
            self.assertEqual(self.invoke('verify-run',p).returncode,0)
            self.assertEqual(self.invoke('replay',p).returncode,0)
    def test_calculate(self):self.assertEqual(self.invoke('calculate','filtration').returncode,0)
