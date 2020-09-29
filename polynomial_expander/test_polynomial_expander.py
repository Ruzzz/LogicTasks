import pytest

from polynomial_expander.polynomial_expander import PolynomialExpander


@pytest.fixture(scope='session')
def polynomial_expander():
    return PolynomialExpander()


@pytest.mark.parametrize(
    'expression, expected',
    (
        ('(2x^3+4)(6x^3+3)', '12x^6+30x^3+12'),
        ('(2x^2+4)(6x^3+3)', '12x^5+24x^3+6x^2+12'),
        ('(1x)(2x^-2+1)', 'x+2x^-1'),
        ('(-1x^3)(3x^3+2)', '-3x^6-2x^3'),
    )
)
def test_polynomial_expander(polynomial_expander, expression, expected):
    assert polynomial_expander(expression) == expected
