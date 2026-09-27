import math
import unittest
from nephrogenesis.common import ValidationError,number,integer
from nephrogenesis.units import Quantity as Q,convert
from nephrogenesis.calculators import book_benchmarks,calculate,defaults,NA,R,KB

class UnitTests(unittest.TestCase):
    def test_millilitres_to_litres(self): self.assertAlmostEqual(convert(1000,'mL','L'),1)
    def test_flow_conversion(self): self.assertAlmostEqual(convert(120,'mL/min','L/min'),.12)
    def test_kj_to_j(self): self.assertEqual(convert(50,'kJ/mol','J/mol'),50000)
    def test_concentration_conversion(self): self.assertEqual(convert(1,'mol/L','mmol/L'),1000)
    def test_power_dimensions(self): self.assertAlmostEqual((Q.of(1,'nmol/s')*Q.of(50,'kJ/mol')).to('uW'),50)
    def test_molar_not_energy(self):
        with self.assertRaises(ValidationError): Q.of(1,'J/mol').to('J')
    def test_osmolarity_not_osmolality(self):
        with self.assertRaises(ValidationError): convert(300,'mOsm/kg','mOsm/L')
    def test_chemical_not_osmoles(self):
        with self.assertRaises(ValidationError): convert(300,'mmol/L','mOsm/L')
    def test_unknown_unit(self):
        with self.assertRaises(ValidationError): Q.of(1,'dose')
    def test_nan(self):
        with self.assertRaises(ValidationError): Q.of(float('nan'),'J')
    def test_infinity(self):
        with self.assertRaises(ValidationError): Q.of(float('inf'),'J')
    def test_boolean(self):
        with self.assertRaises(ValidationError): Q.of(True,'J')
    def test_add_different_dimensions(self):
        with self.assertRaises(ValidationError): Q.of(1,'J')+Q.of(1,'J/mol')
    def test_add_convertible(self): self.assertEqual((Q.of(1,'L')+Q.of(1000,'mL')).to('L'),2)
    def test_subtraction(self): self.assertEqual((Q.of(2,'L')-Q.of(1,'L')).to('L'),1)
    def test_scalar_division(self): self.assertEqual((Q.of(2,'L')/2).to('L'),1)
    def test_zero_divisor(self):
        with self.assertRaises(ValidationError): Q.of(1,'L')/0
    def test_quantity_zero_divisor(self):
        with self.assertRaises(ValidationError): Q.of(1,'L')/Q.of(0,'s')
    def test_log_dimensionless(self): self.assertAlmostEqual((Q.of(2,'L')/Q.of(1,'L')).log(),math.log(2))
    def test_log_dimensionful(self):
        with self.assertRaises(ValidationError): Q.of(1,'L').log()
    def test_log_nonpositive(self):
        with self.assertRaises(ValidationError): Q.of(-1,'1').log()
    def test_tagged_algebra(self):
        with self.assertRaises(ValidationError): Q.of(1,'mOsm/L')*Q.of(1,'L')
    def test_avogadro_conversion(self):
        actual=(Q.of(12511.020147906465,'J/mol')/Q.of(NA,'1/mol')).to('J')
        self.assertAlmostEqual(actual/(KB*310*math.log(2)),12511.020147906465/(R*310*math.log(2)))
    def test_integer_boolean_rejected(self):
        with self.assertRaises(ValidationError): integer(True,'seed',0,100)
    def test_finite_bounds(self):
        with self.assertRaises(ValidationError): number(-1,'temperature',positive=True)

class CalculatorContracts(unittest.TestCase):
    def test_all_calculator_defaults(self):
        for k,p in defaults().items(): self.assertIn('outputs',calculate(k,p))
    def test_unknown_calculator(self):
        with self.assertRaises(ValidationError): calculate('clinical-dose',{})
    def test_extra_field_rejected(self):
        with self.assertRaises(ValidationError): calculate('filtration',{**defaults()['filtration'],'patient_name':'X'})
    def test_gfr_cannot_exceed_plasma_flow(self):
        p=defaults()['filtration'];p['gfr']['value']=800
        with self.assertRaises(ValidationError): calculate('filtration',p)
    def test_zero_plasma_osmolarity(self):
        p=defaults()['clearance'];p['plasma_osmolarity']['value']=0
        with self.assertRaises(ValidationError): calculate('clearance',p)
    def test_negative_temperature(self):
        p=defaults()['electrochemical'];p['temperature']['value']=-1
        with self.assertRaises(ValidationError): calculate('electrochemical',p)
    def test_zero_concentration_log(self):
        p=defaults()['electrochemical'];p['inside']['value']=0
        with self.assertRaises(ValidationError): calculate('electrochemical',p)
    def test_weak_gravity_boundary(self):
        p=defaults()['scales'];p['total_energy']['value']=1e50
        with self.assertRaises(ValidationError): calculate('scales',p)
    def test_wrong_atp_unit(self):
        p=defaults()['transport_energy'];p['atp_energy']['unit']='J'
        with self.assertRaises(ValidationError): calculate('transport_energy',p)
    def test_untagged_clearance_rejected(self):
        p=defaults()['clearance'];p['urine_osmolarity']['unit']='mmol/L'
        with self.assertRaises(ValidationError): calculate('clearance',p)

class BookRegressionTests(unittest.TestCase): pass
for check in book_benchmarks():
    def test(self,case=check):
        self.assertTrue(case['passed'],case)
    setattr(BookRegressionTests,'test_'+check['id'],test)
