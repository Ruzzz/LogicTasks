from typing import List, Literal, Optional, Iterable, Tuple, Union
from itertools import chain

Player = Literal['x', 'o']
Board = List[List[Optional[Player]]]
Step = Tuple[Player, int, int]


class TicTacToy:

    def __init__(self, board_size: int = 3):
        self._board: Board = [[None] * board_size for _ in range(board_size)]
        self._prev_step = None
        self._winner = None

    def _next(self, value: Player, x: int, y: int):
        assert self._board[x][y] is None
        assert self._prev_step != value
        self._prev_step = value

        self._board[x][y] = value

    @classmethod
    def _check_row(cls, row: Iterable[Optional[Player]]) -> Optional[Player]:
        row = set(row)
        if len(row) == 1:
            return row.pop()

    def _find_winner(self) -> Optional[Player]:
        # check row, and cols (used transposed matrix)
        for row in chain(self._board, zip(*self._board)):
            if ret := self._check_row(row):
                return ret

        # check diagonals
        size = len(self._board)
        for board in (self._board, self._board[::-1]):
            row = (board[i][i] for i in range(size))
            if ret := self._check_row(row):
                return ret

    def play(self, steps: Iterable[Union[Step, str]]) -> Optional[Player]:
        if not self._winner:
            for step in steps:
                if isinstance(step, str):  # normalize step data
                    step = step[0], int(step[1]), int(step[2])

                self._next(*step)
                if winner := self._find_winner():
                    self._winner = winner
                    break

        return self._winner
