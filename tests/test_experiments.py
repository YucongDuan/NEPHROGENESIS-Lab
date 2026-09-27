import json
from pathlib import Path
import unittest
from nephrogenesis.experiments import run_experiment,catalog,LABS
from nephrogenesis.common import ValidationError

class ExperimentTests(unittest.TestCase):
    def test_unknown_lab(self):
        with self.assertRaises(ValidationError): run_experiment('diagnose')
    def test_unknown_parameter(self):
        with self.assertRaises(ValidationError): run_experiment('signal',{'dose':3})
    def test_hidden_work(self):
        r=run_experiment('transport');self.assertEqual(r['metrics']['output_difference_mmol_min'],0)
        self.assertGreater(r['metrics']['coupled_power_difference_W'],0)
    def test_invalid_hidden_work(self):
        with self.assertRaises(ValidationError): run_experiment('transport',{'low_filtered_mmol_min':.01})
    def test_membrane_conservation(self): self.assertLess(run_experiment('membrane')['metrics']['maximum_mass_residual_mmol'],1e-10)
    def test_membrane_no_exchange(self):
        r=run_experiment('membrane',{'conductance_L_min':0});self.assertEqual(r['series'][0]['y'][0],r['series'][0]['y'][-1])
    def test_perfect_signal_and_same_action_budget(self):
        r=run_experiment('signal',{'error_probability':0})
        self.assertEqual(r['rows'][0]['matched_fraction'],1)
        self.assertEqual(len(set(x['allocation_energy_J'] for x in r['rows'])),1)
    def test_perfectly_reversed_channel_remapped(self):
        r=run_experiment('signal',{'error_probability':1})
        self.assertEqual(r['rows'][0]['matched_fraction'],0)
        self.assertEqual(r['rows'][-1]['matched_fraction'],1)
    def test_binary_information_symmetric(self):
        a=run_experiment('signal',{'error_probability':.2});b=run_experiment('signal',{'error_probability':.8})
        self.assertAlmostEqual(a['metrics']['channel_information_bits'],b['metrics']['channel_information_bits'])
    def test_information_zero_at_half(self): self.assertEqual(run_experiment('signal',{'error_probability':.5})['metrics']['channel_information_bits'],0)
    def test_equal_equilibria(self):
        r=run_experiment('identifiability');self.assertEqual(r['metrics']['steady_A'],r['metrics']['steady_B'])
    def test_discrimination_time_near_analytic(self):
        import math
        t=run_experiment('identifiability')['metrics']['best_candidate_time_min']
        self.assertLess(abs(t-math.log(2)/.01),1.81)
    def test_noise_reduces_design_score(self):
        a=run_experiment('identifiability',{'noise_sd':.3});b=run_experiment('identifiability',{'noise_sd':.6})
        self.assertAlmostEqual(a['metrics']['maximum_design_score']/b['metrics']['maximum_design_score'],4)
    def test_correction_propagates(self): self.assertEqual(run_experiment('evidence')['metrics']['affected_nodes'],5)
    def test_ablation_full_catches_designed_faults(self):
        r=run_experiment('ablation')
        self.assertTrue(all(x['expected_fault']==x['detected'] for x in r['rows'] if x['validator']=='full_contract'))
    def test_synthetic_hypothesis_reproducible(self): self.assertEqual(run_experiment('hypothesis'),run_experiment('hypothesis'))
    def test_synthetic_extension_on_heldout(self):
        r=run_experiment('hypothesis');self.assertLess(r['rows'][1]['held_out_MSE'],r['rows'][0]['held_out_MSE'])
    def test_ensemble_reproducible(self): self.assertEqual(run_experiment('uncertainty',{'samples':5}),run_experiment('uncertainty',{'samples':5}))
    def test_ensemble_limits(self):
        with self.assertRaises(ValidationError): run_experiment('uncertainty',{'samples':1000000})
    def test_pareto_front_not_empty(self): self.assertGreater(run_experiment('viability')['metrics']['nondominated'],0)
    def test_chapters_complete(self):
        p=Path(__file__).resolve().parents[1]/'nephrogenesis/data/chapters.json'
        chapters=json.loads(p.read_text());self.assertEqual([x['chapter'] for x in chapters],list(range(1,19)))
        self.assertEqual(len({x['experiment'] for x in chapters}),18)
        self.assertTrue(all(x['source_chapter_sha256'] and x['book_sections'] for x in chapters))
    def test_defaults_are_independent(self):
        a=catalog();a[0]['defaults']['dt_min']=9
        self.assertEqual(catalog()[0]['defaults']['dt_min'],.5)

class AllExperimentSmokeTests(unittest.TestCase): pass
for key in LABS:
    def test(self,name=key):
        report=run_experiment(name)
        self.assertEqual(report['experiment'],name)
        self.assertTrue(report['book_sections'])
        json.dumps(report,allow_nan=False)
    setattr(AllExperimentSmokeTests,'test_'+key.replace('-','_'),test)

class TraceConsistencyTest(unittest.TestCase):
    def test_signal_cumulative_trace_matches_summary(self):
        r=run_experiment('signal')
        for row,line in zip(r['rows'],r['series']):
            self.assertEqual(row['recovered_units'],line['y'][-1])
            self.assertEqual(len(line['y']),501)
