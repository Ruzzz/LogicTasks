import pytest

from tictactoy import TicTacToy, Player


@pytest.fixture
def tictactoy():
    return TicTacToy()


@pytest.mark.parametrize(
    'steps, expected',
    (
        (('x00', 'o01', 'x10', 'o11', 'x20'), 'x'),
        (('x10', 'o00', 'x11', 'o01', 'x12'), 'x'),
        (('x00', 'o10', 'x11', 'o01', 'x22'), 'x'),
        (('x20', 'o10', 'x11', 'o01', 'x02'), 'x'),
    )
)
def test_tictactoy(tictactoy: TicTacToy, steps, expected: Player):
    assert tictactoy.play(steps) == expected
