# https://leetcode.com/problems/peeking-iterator/

import pytest


class PeekingIterator:
    __slots__ = '_it', '_temp'

    def __init__(self, iterator):
        self._it = iterator
        self._temp = -1
        self.next()

    def peek(self):
        return self._temp

    def next(self):
        ret, self._temp = self._temp, self._it.next() if self._it.hasNext() else -1
        return ret

    def hasNext(self):
        return self._temp != -1


class PeekingIterator2:
    __slots__ = '_it', '_has_next', '_temp'

    def __init__(self, iterator):
        self._it = iterator
        self._peek()

    def _peek(self):
        self._has_next = self._it.hasNext()
        if self._has_next:
            self._temp = self._it.next()

    def peek(self):
        return self._temp

    def next(self):
        ret = self._temp
        self._peek()
        return ret

    def hasNext(self):
        return self._has_next


@pytest.mark.parametrize(
    'solution',
    (PeekingIterator, PeekingIterator2)
)
@pytest.mark.parametrize(
    'data, ops, expected',
    (
        (
            [1, 2, 3],
            ('next', 'peek', 'next', 'next', 'hasNext'),
            (1, 2, 2, 3, False)
        ),
    )
)
def test_peeking_iterator(solution, data, ops, expected):

    class Iterator:

        def __init__(self, sequ):
            self._sequ = sequ or []
            self._i = 0

        def hasNext(self):
            return self._i < len(self._sequ)

        def next(self):
            self._i += 1
            return self._sequ[self._i - 1]

    it = solution(Iterator(data))
    for op, result in zip(ops, expected):
        assert getattr(it, op)() == result
