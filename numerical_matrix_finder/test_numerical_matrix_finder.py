import pytest

from numerical_matrix_finder import CoordT, MatrixT, NumericalMatrixFinder


@pytest.mark.parametrize(
    'scan_width, scan_height, min_matrix_width, min_matrix_height',
    (
        (2, 2, 1, 1),
        (1, 1, 4, 4),
        (4, 4, 2, 2),
    )
)
def test_invalid_settings(scan_width, scan_height, min_matrix_width, min_matrix_height):
    with pytest.raises(Exception):
        NumericalMatrixFinder(scan_width, scan_height, min_matrix_width, min_matrix_height)


finder_2x2 = NumericalMatrixFinder()
finder_4x3 = NumericalMatrixFinder(4, 3)


# Standard matrices that used in many tests
MATRIX_2x2_1 = [
    'df4a',
    'Ap21',
    'Fy36',
    'acvb'
]
MATRIX_4x3_1 = [
    'df4abz',
    'A1234z',
    'F2345z',
    'a5678z',
    'af876z'
]


@pytest.mark.parametrize(
    'finder, matrix, valid',
    (
        (finder_2x2, MATRIX_2x2_1, True),
        (finder_2x2, [], False),
        (finder_2x2, ['a'], False),
        (finder_2x2, ['a', '1'], False),
        (finder_2x2, ['abcd', 'abcd', 'abcde', 'abcd'], False),

        (finder_4x3, MATRIX_4x3_1, True),
        (finder_4x3, [], False),
        (finder_4x3, ['a'], False),
        (finder_4x3, ['a', '1'], False),
        (finder_4x3, ['abcd', 'abcd', 'abcde', 'abcd'], False),
    ),
    ids=[
        'valid',
        'empty',
        'invalid size',
        'invalid size',
        'different width',

        'valid',
        'empty',
        'invalid size',
        'invalid size',
        'different width',
    ]
)
def test_validation(finder, matrix: MatrixT, valid: bool):
    assert finder.validate_matrix(matrix) == valid


@pytest.mark.parametrize(
    'finder, matrix, expected_response',
    (
        (
            finder_2x2,
            MATRIX_2x2_1,
            (3, 2)
        ),
        (
            finder_2x2,
            [
                '123a',
                '3421',
                'Fy36',
                'acvb'
            ],
            (1, 1)
        ),
        (
            finder_2x2,
            [
                '1s4az',
                '34k1z',
                'Fy361',
                'acv20'
            ],
            (4, 3)
        ),
        (
            finder_2x2,
            [
                '1s4az',
                '34k1z',
                'Fy361',
                'acv2a'
            ],
            False
        ),
        (
            finder_2x2,
            [
                '1s',
                '34'
            ],
            False
        ),

        (
            finder_4x3,
            MATRIX_4x3_1,
            (2, 2)
        ),
        (
            finder_4x3,
            [
                '1234bz',
                '21234z',
                '32345z',
                'a5678z',
                'af876z'
            ],
            (1, 1)
        ),
        (
            finder_4x3,
            [
                'a1s4az',
                'a1s4az',
                'a1s4az',
                'b31234',
                'zF5678',
                'xa9087'
            ],
            (3, 4)
        ),
        (
            finder_4x3,
            [
                '12a4bz',
                '21a34z',
                '32345z',
                'a5678z',
                'af876z'
            ],
            False
        ),
        (
            finder_4x3,
            [
                '1s',
                '34'
            ],
            False
        )
    )
)
def test_search(finder, matrix: MatrixT, expected_response: CoordT):
    assert finder.search(matrix) == expected_response
