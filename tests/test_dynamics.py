import random
import unittest
from nephrogenesis.dynamics import simulate,config,rk4_step
from nephrogenesis.common import ValidationError

class DynamicsTests(unittest.TestCase):
    def test_water_conservation(self): self.assertLess(simulate()['metrics']['maximum_water_residual_L'],1e-10)
    def test_sodium_conservation(self): self.assertLess(simulate()['metrics']['maximum_sodium_residual_mmol'],1e-8)
    def test_urea_conservation(self): self.assertLess(simulate()['metrics']['maximum_urea_residual_mmol'],1e-9)
    def test_steady_state(self):
        r=simulate({'events':[],'controller':'fixed'})
        self.assertAlmostEqual(r['metrics']['final_volume_L'],14)
        self.assertAlmostEqual(r['metrics']['final_sodium_mmol_L'],140)
    def test_exact_event_integral(self):
        r=simulate({'dt_min':7,'events':[{'start_min':61.2,'end_min':122.3,'water_extra_L_min':.01,'sodium_extra_mmol_min':.3}]})
        self.assertAlmostEqual(r['trajectory'][-1]['water_input_L'],.001*360+.01*(122.3-61.2),10)
    def test_seed_reproducibility(self):
        p={'controller':'scrambled','seed':12}
        self.assertEqual(simulate(p),simulate(p))
    def test_seed_changes_scrambled_sequence(self):
        a=simulate({'controller':'scrambled','seed':12})
        b=simulate({'controller':'scrambled','seed':13})
        self.assertNotEqual(a['metrics'],b['metrics'])
    def test_zero_delay_matches_feedback(self):
        a=simulate({'controller':'delayed','delay_min':0})['trajectory']
        b=simulate({'controller':'feedback'})['trajectory']
        self.assertEqual(a,b)
    def test_positive_energy_and_budget(self):
        r=simulate();self.assertGreater(r['metrics']['coupled_energy_J'],0)
        self.assertLessEqual(r['metrics']['mean_coupled_power_W'],5+1e-9)
    def test_low_budget_enforced(self):
        r=simulate({'power_budget_W':1})
        self.assertLessEqual(r['metrics']['mean_coupled_power_W'],1+1e-9)
        self.assertGreater(r['metrics']['budget_limited_steps'],0)
    def test_passive_degenerate_case(self):
        self.assertEqual(simulate({'active_fraction':0})['metrics']['coupled_energy_J'],0)
    def test_no_negative_compartment(self):
        r=simulate({'power_budget_W':0})
        self.assertTrue(all(x['sodium_mmol_L']>0 and x['volume_L']>0 for x in r['trajectory']))
    def test_invalid_mode(self):
        with self.assertRaises(ValidationError): config({'controller':'autonomous-treatment'})
    def test_too_many_steps(self):
        with self.assertRaises(ValidationError): config({'duration_min':1000,'dt_min':.01})
    def test_event_outside_horizon(self):
        with self.assertRaises(ValidationError): config({'duration_min':30})
    def test_unknown_parameter(self):
        with self.assertRaises(ValidationError): config({'dose':3})
    def test_reverse_event(self):
        with self.assertRaises(ValidationError): config({'events':[{'start_min':10,'end_min':0,'water_extra_L_min':0,'sodium_extra_mmol_min':0}]})
    def test_negative_inflow(self):
        with self.assertRaises(ValidationError): config({'water_input_L_min':-1})
    def test_large_initial_volume(self):
        with self.assertRaises(ValidationError): config({'initial_volume_L':1e8})
    def test_nonfinite_dt(self):
        with self.assertRaises(ValidationError): config({'dt_min':float('inf')})
    def test_rk4_against_exact_linear_solution(self):
        import math
        y=[1.]
        for i in range(100): y=rk4_step(y,.01,lambda z:[-z[0]])
        self.assertAlmostEqual(y[0],math.exp(-1),9)
    def test_step_refinement(self):
        rs=[simulate({'dt_min':x})['metrics']['final_sodium_mmol_L'] for x in [1.,.5,.25]]
        self.assertLess(abs(rs[1]-rs[2]),abs(rs[0]-rs[1]))
    def test_random_parameter_conservation(self):
        rng=random.Random(93)
        for i in range(30):
            r=simulate({'dt_min':rng.uniform(.4,2),'gfr_L_min':rng.uniform(.08,.16),'active_fraction':rng.uniform(.2,.8)})
            self.assertLess(r['metrics']['maximum_sodium_residual_mmol'],1e-8)
            self.assertLess(r['metrics']['maximum_water_residual_L'],1e-9)
    def test_default_events_not_mutated(self):
        a=config();a['events'][0]['start_min']=1
        self.assertEqual(config()['events'][0]['start_min'],60)
