from copy import deepcopy
import csv
from pathlib import Path
import tempfile
import unittest
from nephrogenesis.common import ValidationError
from nephrogenesis.experiments import run_experiment,LABS
from nephrogenesis.calibration import read_observations
class CalibrationTests(unittest.TestCase):
    def test_recover_synthetic_known_rate(self):
        m=run_experiment('calibration')['metrics'];self.assertAlmostEqual(m['k_per_min'],.02,10)
        self.assertAlmostEqual(m['equilibrium_mmol_L'],10,10);self.assertLess(m['held_out_MSE'],1e-20)
    def test_heldout_not_used_for_selection(self):
        p=deepcopy(LABS['calibration'][2]);a=run_experiment('calibration',p)
        for r in p['observations']:
            if r['split']=='test':r['concentration_mmol_L']+=100
        b=run_experiment('calibration',p)
        self.assertEqual(a['metrics']['k_per_min'],b['metrics']['k_per_min'])
        self.assertEqual(a['metrics']['equilibrium_mmol_L'],b['metrics']['equilibrium_mmol_L'])
        self.assertGreater(b['metrics']['held_out_MSE'],100)
    def test_rights_declaration_required(self):
        p=deepcopy(LABS['calibration'][2]);p['source']['rights_confirmed']=False
        with self.assertRaises(ValidationError):run_experiment('calibration',p)
    def test_sorted_times_required(self):
        p=deepcopy(LABS['calibration'][2]);p['observations'][2]['time_min']=0
        with self.assertRaises(ValidationError):run_experiment('calibration',p)
    def test_zero_time_initial_train_required(self):
        p=deepcopy(LABS['calibration'][2]);p['observations'][0]['split']='test'
        with self.assertRaises(ValidationError):run_experiment('calibration',p)
    def test_heldout_required(self):
        p=deepcopy(LABS['calibration'][2])
        for r in p['observations']:r['split']='train'
        with self.assertRaises(ValidationError):run_experiment('calibration',p)
    def test_grid_limit(self):
        with self.assertRaises(ValidationError):run_experiment('calibration',{'grid_size':10000})
    def test_grid_boundary_warning(self):
        r=run_experiment('calibration',{'k_min_per_min':.04,'k_max_per_min':.05})
        self.assertTrue(r['metrics']['on_search_boundary'])
    def test_source_not_silently_verified(self):
        r=run_experiment('calibration');self.assertIn('operator declarations',' '.join(r['notes']))
    def test_read_csv_header(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'bad.csv';p.write_text('time,concentration\n1,2\n')
            with self.assertRaises(ValidationError):read_observations(p)
