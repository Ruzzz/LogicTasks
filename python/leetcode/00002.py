# https://leetcode.com/problems/add-two-numbers/

import pytest


class ListNode:

    def __init__(self, val=0, next=None):
        # assert 0 <= val <= 9
        self.val = val
        self.next = next


class Solution:

    def addTwoNumbers(self, l1: ListNode, l2: ListNode) -> ListNode:
        first = prev = None
        cf = 0
        while l1 or l2 or cf:
            n = cf
            if l1:
                n, l1 = n + l1.val, l1.next
            if l2:
                n, l2 = n + l2.val, l2.next
            cf = 1 if n > 9 else 0
            if cf:
                n -= 10

            node = ListNode(n)
            if prev:
                prev.next = node
            prev = node
            if not first:
                first = node
        return first


@pytest.mark.parametrize(
    'l1, l2, expected',
    (
        ([2, 4, 3], [5, 6, 4], [7, 0, 8]),
        ([0], [0], [0]),
        ([9, 9, 9, 9, 9, 9, 9], [9, 9, 9, 9], [8, 9, 9, 9, 0, 0, 0, 1]),
    )
)
def test_add_two_numbers(l1, l2, expected):

    def from_list(arr):
        ret = None
        arr.reverse()
        for x in arr:
            ret = ListNode(x, ret)
        return ret

    def to_list(node):
        ret = []
        while node:
            ret.append(node.val)
            node = node.next
        return ret

    assert to_list(Solution().addTwoNumbers(from_list(l1), from_list(l2))) == expected
