# https://leetcode.com/problems/longest-substring-without-repeating-characters/

import pytest


class Solution:

    def lengthOfLongestSubstring(self, s: str) -> int:
        ret = 0
        indexes = {}
        start = 0
        for i, char in enumerate(s):
            if char in indexes:
                ret = max(ret, i - start)
                start = max(start, indexes[char] + 1)
            indexes[char] = i
        return max(ret, len(s) - start)


class Solution2:

    def lengthOfLongestSubstring(self, s: str) -> int:
        size = len(s)
        if size < 2:
            return size
        chars = set()
        ret = start = end = 0
        while start < size and end < size:
            char = s[end]
            if char not in chars:
                chars.add(char)
                end += 1
            else:
                chars.remove(s[start])
                ret = max(ret, end - start)
                start += 1
        return max(ret, size - start)


@pytest.mark.parametrize(
    'solution',
    (Solution, Solution2,)
)
@pytest.mark.parametrize(
    's, expected',
    (
        (' ', 1),
        ('ab', 2),
        ('abcaecbb', 4),
        ('abcabcbb', 3),
        ('bbbbb', 1),
        ('pwwkew', 3),
    )
)
def test_length_of_longest_substring(solution, s, expected):
    assert solution().lengthOfLongestSubstring(s) == expected
