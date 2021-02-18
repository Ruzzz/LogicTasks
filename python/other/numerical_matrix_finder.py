import string
from typing import List, Tuple, Union, Optional

RowT = str
MatrixT = List[RowT]  # [y, x]
CoordT = Union[bool, Tuple[int, int]]  # x, y


def is_digit(char) -> bool:
    return char in string.digits


class NumericalMatrixFinder:

    def __init__(self,
                 scan_width=2,
                 scan_height=2,
                 min_matrix_width=4,
                 min_matrix_height=4):
        if scan_width > min_matrix_width or scan_height > min_matrix_height:
            raise Exception('Minimum input matrix size must be greater than output matrix')
        if scan_width < 2 or scan_height < 2:
            raise Exception('Matrix size for scanning must be no less than 2x2')

        self.scan_width = scan_width
        self.scan_height = scan_height
        self.min_matrix_width = min_matrix_width
        self.min_matrix_height = min_matrix_height

    def __call__(self, matrix: MatrixT) -> CoordT:
        return self.search(matrix)

    def search(self, matrix: MatrixT) -> CoordT:
        """
        :param matrix: Valid matrix
        :return: Coordinates (x, y) of left-top 2x2 numerical matrix or False.
                 Coordinates is 1 based (not zero based).
        """
        if self.validate_matrix(matrix):
            len_y = len(matrix) - self.scan_height + 1
            len_x = -1
            y = 0
            while y < len_y:
                row = matrix[y]
                if len_x == -1:
                    len_x = len(row) - self.scan_width + 1
                x = 0
                while x < len_x:
                    sequ_size = self._find_numerical_sequ_size(row, x)
                    if sequ_size == self.scan_width:  # found first valid row
                        for i in range(1, self.scan_height):
                            next_row = matrix[y + i]
                            sequ_size = self._find_numerical_sequ_size(next_row, x)
                            if sequ_size != self.scan_width:
                                x += 1
                                break
                        else:
                            return x + 1, y + 1
                    else:
                        x += sequ_size + 1
                y += 1

        return False

    def _find_numerical_sequ_size(self, row: RowT, index: int) -> Optional[int]:
        """
        :param index: Scan from
        :return: Size of numerical sequence
        """

        for i in range(self.scan_width):
            if not is_digit(row[index + i]):
                return i

        return self.scan_width

    def validate_matrix(self, matrix: MatrixT) -> bool:
        if not isinstance(matrix, List) or len(matrix) < self.min_matrix_height:
            return False

        matrix_width = 0
        for row in matrix:
            if not isinstance(row, RowT):
                return False

            if not matrix_width:
                matrix_width = len(row)
                if matrix_width < self.min_matrix_width:
                    return False
            else:
                if len(row) != matrix_width:
                    return False

        return True
