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

    def _find_winner(self) -> Optional[Player]:
        # check row, cols (used transposed matrix) and diagonals
        board_size = len(self._board)
        diagonals = (
            (self._board[i][i] for i in range(board_size)),
            (self._board[i][board_size - i - 1] for i in range(board_size)),
        )
        for row in chain(self._board, zip(*self._board), diagonals):
            row = set(row)
            if len(row) == 1:
                return row.pop()

    def play(self, steps: Iterable[Union[Step, str]]) -> Optional[Player]:
        if not self._winner:
            find_winner_limit = len(self._board) * 2 - 2
            for step_no, step in enumerate(steps):
                if isinstance(step, str):  # normalize step data
                    step = step[0], int(step[1]), int(step[2])

                self._next(*step)
                if step_no < find_winner_limit:
                    continue
                if winner := self._find_winner():
                    self._winner = winner
                    break

        return self._winner
