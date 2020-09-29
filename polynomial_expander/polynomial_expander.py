import re
from typing import List


class Monomial:
    __slots__ = 'coefficient', 'indeterminate', 'power'

    def __init__(self, coefficient: int, indeterminate: str = None, power: int = 0):
        self.coefficient = coefficient
        self.indeterminate = indeterminate
        self.power = power

    def __str__(self):
        ret = '' if self.coefficient == 1 and self.indeterminate else str(self.coefficient)
        if self.indeterminate:
            ret = ret + self.indeterminate
            if self.power != 1:
                ret = f'{ret}^{self.power}'
        if ret[0] != '-':
            ret = '+' + ret
        return ret

    def __mul__(self, other: 'Monomial'):
        coefficient = self.coefficient * other.coefficient
        indeterminate = self.indeterminate or other.indeterminate
        power = self.power + other.power
        return Monomial(coefficient, indeterminate, power)

    def __add__(self, other: 'Monomial'):
        assert self.power == other.power
        return Monomial(self.coefficient + other.coefficient, self.indeterminate, self.power)


Polynomial = List[Monomial]


class PolynomialParser:

    _polynomials_re = re.compile(r'(?<=\().*?(?=\))')
    _monomials_re = re.compile(r'([+-]?\w+)(\^[+-]?\d+)?')

    def __call__(self, expression: str) -> List[Polynomial]:
        polynomials = []
        for polynomial_match in self._polynomials_re.finditer(expression):
            polynomial = []
            for monomial_match in self._monomials_re.finditer(polynomial_match[0]):
                indeterminate = None
                power = 0
                coefficient = monomial_match[1]
                if coefficient[-1].isalpha():
                    indeterminate = coefficient[-1]
                    coefficient = coefficient[:-1]
                    if monomial_match.lastindex == 2:
                        power = int(monomial_match[2][1:])  # skip char ^
                    else:
                        power = 1
                coefficient = int(coefficient)
                polynomial.append(Monomial(coefficient, indeterminate, power))
            if polynomial:
                polynomial.sort(key=lambda x: -x.power)
                polynomials.append(polynomial)
        assert len(polynomials) == 2
        return polynomials


class PolynomialExpander:

    def __init__(self):
        self._parser = PolynomialParser()

    def __call__(self, expression: str):
        polynomials = self._parser(expression)
        expanded_monomials = []
        for monomial1 in polynomials[0]:
            for monomial2 in polynomials[1]:
                expanded_monomials.append(monomial1 * monomial2)
        expanded_monomials.sort(key=lambda x: -x.power)

        ret = [expanded_monomials[0]]
        for x in expanded_monomials[1:]:
            if x.power == ret[-1].power:
                ret[-1] += x
            else:
                ret.append(x)

        # to string
        ret = ''.join(str(x) for x in ret)
        if ret[0] == '+':
            ret = ret[1:]
        return ret
