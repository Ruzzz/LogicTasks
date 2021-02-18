# https://leetcode.com/problems/move-zeroes/

from typing import List

import pytest


class Solution(object):

    def moveZeroes(self, nums: List[int]):
        j = 0  # copy pointer
        for i, n in enumerate(nums):
            if n != 0:
                if j != i:
                    nums[j] = n
                j += 1

        for i in range(j, len(nums)):
            nums[i] = 0

        return nums


@pytest.mark.parametrize(
    'value, expected',
    (
        ([0, 1, 0, 3, 12], [1, 3, 12, 0, 0]),
        ([1, 0, 0, 2, 0, 0], [1, 2, 0, 0, 0, 0]),
        ([0, 0, 1, 2, 0, 0], [1, 2, 0, 0, 0, 0]),
        ([0, 0, 0, 0, 1, 2], [1, 2, 0, 0, 0, 0]),
    )
)
def test_move_zeroes(value, expected):
    Solution().moveZeroes(value)
    assert value == expected
