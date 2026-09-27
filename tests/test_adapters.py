import unittest
from nephrogenesis.adapters import review_envelope
from nephrogenesis.experiments import run_experiment
class AdapterTests(unittest.TestCase):
    def test_export_is_not_claimed_upstream_integration(self):
        e=review_envelope(run_experiment('transport'))
        self.assertIn('require mapping',e['compatibility'])
        self.assertFalse(e['DIKWP']['K']['empirical_validation'])
    def test_all_roles_preserved(self):self.assertEqual(set(review_envelope(run_experiment('transport'))['DIKWP']),{'D','I','K','W','P'})
    def test_result_digest_reproducible(self):self.assertEqual(review_envelope(run_experiment('transport')),review_envelope(run_experiment('transport')))
