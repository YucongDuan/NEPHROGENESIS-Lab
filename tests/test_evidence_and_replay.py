from copy import deepcopy
import json
from pathlib import Path
import tempfile
import unittest
from nephrogenesis.common import ValidationError,load_json,canonical,digest
from nephrogenesis.evidence import demonstration_graph,validate_graph,withdraw
from nephrogenesis.ledger import build_chain,verify_chain,write_bundle,verify_bundle,replay,numerical_equal,export_csv

class EvidenceTests(unittest.TestCase):
    def test_valid_graph(self): self.assertTrue(validate_graph(demonstration_graph())['valid'])
    def test_backward_semantic_role_allowed(self):
        graph=demonstration_graph()
        self.assertEqual(graph['nodes'][-1]['role'],'P')
        self.assertTrue(validate_graph(graph)['valid'])
    def test_missing_dependency(self):
        g=demonstration_graph();g['nodes'][3]['depends_on']=['missing']
        with self.assertRaises(ValidationError): validate_graph(g)
    def test_cycle(self):
        g=demonstration_graph();g['nodes'][0]['depends_on']=['revised-question']
        with self.assertRaises(ValidationError): validate_graph(g)
    def test_duplicate_id(self):
        g=demonstration_graph();g['nodes'].append(deepcopy(g['nodes'][0]))
        with self.assertRaises(ValidationError): validate_graph(g)
    def test_missing_source(self):
        g=demonstration_graph();del g['nodes'][1]['source']
        with self.assertRaises(ValidationError): validate_graph(g)
    def test_taint_not_promoted(self):
        g=demonstration_graph();g['nodes'][4]['kind']='empirical';g['nodes'][4]['source']='declared source'
        self.assertFalse(validate_graph(g)['node_validity']['calculation'])
    def test_contract_unsatisfied(self):
        g=demonstration_graph();g['nodes'][3]['requires']=['measured_oxygen_consumption']
        self.assertFalse(validate_graph(g)['valid'])
    def test_source_withdrawal(self):
        r=withdraw(demonstration_graph(),'book-8.17')
        self.assertEqual(r['affected'],['book-8.17','calculation','interpretation','revised-question'])
    def test_withdraw_does_not_mutate(self):
        g=demonstration_graph();withdraw(g,'synthetic-flux')
        self.assertTrue(validate_graph(g)['valid'])
    def test_unknown_withdrawal(self):
        with self.assertRaises(ValidationError): withdraw(demonstration_graph(),'nothing')
    def test_invalid_role(self):
        g=demonstration_graph();g['nodes'][0]['role']='OMNISCIENCE'
        with self.assertRaises(ValidationError): validate_graph(g)

class ReplayTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name)/'run with spaces'
        self.receipt=write_bundle('transport',{},self.root)
    def tearDown(self):self.tmp.cleanup()
    def test_integrity(self):self.assertTrue(verify_bundle(self.root)['verified'])
    def test_anchor(self):self.assertTrue(verify_bundle(self.root,self.receipt['receipt_digest'])['trusted_anchor_supplied'])
    def test_replay(self):self.assertTrue(replay(self.root)['replayed'])
    def test_bitwise_replay_here(self):self.assertTrue(replay(self.root)['identical_serialization'])
    def test_wrong_anchor(self):
        with self.assertRaises(ValidationError):verify_bundle(self.root,'0'*64)
    def test_tamper(self):
        p=self.root/'result.json';p.write_text(p.read_text()+' ')
        with self.assertRaises(ValidationError):verify_bundle(self.root)
    def test_missing_file(self):
        (self.root/'protocol.json').unlink()
        with self.assertRaises(ValidationError):verify_bundle(self.root)
    def test_no_overwrite(self):
        with self.assertRaises(ValidationError):write_bundle('transport',{},self.root)
    def test_unsafe_manifest_path(self):
        p=self.root/'receipt.json';d=json.loads(p.read_text());d['files']['../escape']='x';p.write_text(json.dumps(d))
        with self.assertRaises(ValidationError):verify_bundle(self.root)
    def test_chain_tamper(self):
        c=build_chain([{'a':1},{'a':2}]);c[0]['event']['a']=7
        self.assertFalse(verify_chain(c))
    def test_truncation_with_anchor(self):
        c=build_chain([{'a':1},{'a':2}]);self.assertFalse(verify_chain(c[:-1],c[-1]['hash']))
    def test_full_rewrite_limitation_is_explicit(self):
        c=build_chain([{'a':7},{'a':8}]);self.assertTrue(verify_chain(c))
    def test_empty_chain(self):self.assertFalse(verify_chain([]))
    def test_extra_chain_fields(self):
        c=build_chain([{'a':1}]);c[0]['extra']=1;self.assertFalse(verify_chain(c))
    def test_float_tolerance(self):self.assertTrue(numerical_equal({'a':1.},{'a':1.+1e-12}))
    def test_bool_not_number(self):self.assertFalse(numerical_equal(True,1))
    def test_list_length(self):self.assertFalse(numerical_equal([1],[1,2]))
    def test_json_duplicate_keys(self):
        p=Path(self.tmp.name)/'bad.json';p.write_text('{"x":1,"x":2}')
        with self.assertRaises(ValidationError):load_json(p)
    def test_json_nan(self):
        p=Path(self.tmp.name)/'bad.json';p.write_text('{"x":NaN}')
        with self.assertRaises(ValidationError):load_json(p)
    def test_csv_formula_escape(self):
        p=Path(self.tmp.name)/'t.csv';export_csv(p,{'rows':[{'input':'=DANGEROUS()','value':-3}]})
        self.assertIn("'=DANGEROUS()",p.read_text());self.assertIn('-3',p.read_text())
    def test_html_escape(self):
        from nephrogenesis.reporting import report_html
        html=report_html([{'title':'<script>alert(1)</script>','metrics':{'x':'<svg onload=alert(1)>'}}])
        self.assertNotIn('<script>',html);self.assertIn('&lt;script&gt;',html)
