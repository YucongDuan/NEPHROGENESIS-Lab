"""Small explicit dimensional algebra; no expression evaluator or unit guessing.

Dimensions: length, mass, time, amount, temperature, charge. Osmole/equivalent
are semantic tags on amount. This deliberately distinguishes osmolarity from
osmolality and does not guess valence, fluid density, or indexed body area.
"""
from __future__ import annotations
from dataclasses import dataclass
import math
from .common import number, ValidationError
D0 = (0, 0, 0, 0, 0, 0)
L=(1,0,0,0,0,0); M=(0,1,0,0,0,0); S=(0,0,1,0,0,0)
N=(0,0,0,1,0,0); T=(0,0,0,0,1,0); Q=(0,0,0,0,0,1)
E=(2,1,-2,0,0,0)

@dataclass(frozen=True)
class Unit:
    factor: float
    dimensions: tuple[int, ...]
    tag: str = ''

REGISTRY = {
    '1': Unit(1,D0), 'm':Unit(1,L), 'cm':Unit(.01,L), 'nm':Unit(1e-9,L),
    'm2':Unit(1,(2,0,0,0,0,0)), 'm3':Unit(1,(3,0,0,0,0,0)),
    'L':Unit(.001,(3,0,0,0,0,0)), 'mL':Unit(1e-6,(3,0,0,0,0,0)),
    'kg':Unit(1,M), 'g':Unit(.001,M), 's':Unit(1,S), 'min':Unit(60,S), 'day':Unit(86400,S),
    'mol':Unit(1,N), 'mmol':Unit(.001,N), 'nmol':Unit(1e-9,N), 'K':Unit(1,T),
    'C':Unit(1,Q), 'J':Unit(1,E), 'kJ':Unit(1000,E),
    'W':Unit(1,(2,1,-3,0,0,0)), 'uW':Unit(1e-6,(2,1,-3,0,0,0)),
    'J/mol':Unit(1,(2,1,-2,-1,0,0)), 'kJ/mol':Unit(1000,(2,1,-2,-1,0,0)),
    'J/K':Unit(1,(2,1,-2,0,-1,0)), 'J/mol/K':Unit(1,(2,1,-2,-1,-1,0)),
    'C/mol':Unit(1,(0,0,0,-1,0,1)), '1/mol':Unit(1,(0,0,0,-1,0,0)),
    'V':Unit(1,(2,1,-2,0,0,-1)), 'mV':Unit(.001,(2,1,-2,0,0,-1)),
    'mL/min':Unit(1e-6/60,(3,0,-1,0,0,0)), 'L/min':Unit(.001/60,(3,0,-1,0,0,0)),
    'mol/s':Unit(1,(0,0,-1,1,0,0)), 'nmol/s':Unit(1e-9,(0,0,-1,1,0,0)),
    'mmol/min':Unit(.001/60,(0,0,-1,1,0,0)), 'mmol/L':Unit(1,(-3,0,0,1,0,0)),
    'mol/L':Unit(1000,(-3,0,0,1,0,0)),
    'mOsm/L':Unit(1,(-3,0,0,1,0,0),'osmole'),
    'mOsm/kg':Unit(.001,(0,-1,0,1,0,0),'osmole'),
    'mOsm/day':Unit(.001/86400,(0,0,-1,1,0,0),'osmole'),
    'mEq/day':Unit(.001/86400,(0,0,-1,1,0,0),'equivalent'),
}

@dataclass(frozen=True)
class Quantity:
    si: float
    dimensions: tuple[int, ...]
    tag: str = ''

    def __post_init__(self):
        number(self.si, 'quantity')

    @classmethod
    def of(cls, value: float, unit: str) -> 'Quantity':
        if unit not in REGISTRY:
            raise ValidationError(f'Unknown unit: {unit}; no implicit conversion is allowed')
        u=REGISTRY[unit]
        return cls(number(value, 'value')*u.factor, u.dimensions,u.tag)

    def to(self, unit: str) -> float:
        if unit not in REGISTRY:
            raise ValidationError(f'Unknown unit: {unit}')
        u=REGISTRY[unit]
        if self.dimensions != u.dimensions or self.tag != u.tag:
            raise ValidationError(f'Incompatible dimensions or semantic quantity kind for {unit}')
        return self.si/u.factor

    def __add__(self, other):
        if not isinstance(other, Quantity) or (self.dimensions,self.tag)!=(other.dimensions,other.tag):
            raise ValidationError('Cannot add unlike quantities')
        return Quantity(self.si+other.si,self.dimensions,self.tag)

    def __sub__(self, other):
        return self + other * -1

    def __mul__(self, other):
        if not isinstance(other, Quantity):
            return Quantity(self.si*number(other,'multiplier'),self.dimensions,self.tag)
        if self.tag or other.tag:
            raise ValidationError('Tagged quantity algebra requires an explicit domain equation')
        return Quantity(self.si*other.si,tuple(a+b for a,b in zip(self.dimensions,other.dimensions)))

    __rmul__=__mul__

    def __truediv__(self, other):
        if not isinstance(other,Quantity):
            denominator=number(other,'divisor')
            if denominator==0: raise ValidationError('Division by zero')
            return Quantity(self.si/denominator,self.dimensions,self.tag)
        if other.si==0: raise ValidationError('Division by zero')
        if self.tag or other.tag:
            raise ValidationError('Tagged quantity algebra requires an explicit domain equation')
        return Quantity(self.si/other.si,tuple(a-b for a,b in zip(self.dimensions,other.dimensions)))

    def log(self) -> float:
        if self.dimensions!=D0 or self.tag or self.si<=0:
            raise ValidationError('Logarithm requires a positive dimensionless ratio')
        return math.log(self.si)


def convert(value: float, source: str, target: str) -> float:
    return Quantity.of(value,source).to(target)


def measurement(item: dict, target: str, name: str, *, low=None, high=None, positive=False) -> float:
    if not isinstance(item,dict) or set(item)!={'value','unit'}:
        raise ValidationError(f'{name}: use an explicit value/unit object')
    return number(convert(item['value'],item['unit'],target),name,low,high,positive=positive)
