"""14. Longest Common Prefix"""
from itertools import takewhile
from typing import List
import unittest


class Solution1:
    def longestCommonPrefix(self, strs: List[str]) -> str:
        return "".join(s.pop() for s in takewhile(lambda s: len(s) == 1, map(set, zip(*strs))))


class Solution2:
    def longestCommonPrefix(self, strs: List[str]) -> str:
        a, b = min(strs), max(strs)
        return a[:next((i for i, (x, y) in enumerate(zip(a, b)) if x != y), len(a))]


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.s = [Solution1(), Solution2()]

    def test_empty(self):
        for s in self.s:
            assert s.longestCommonPrefix(["", "dogs"]) == ""
            assert s.longestCommonPrefix(["cats", "dogs"]) == ""

    def test_example(self):
        for s in self.s:
            assert s.longestCommonPrefix(["flower","flow","flight"]) == "fl"
            assert s.longestCommonPrefix(["dog","racecar","car"]) == ""

    def test_increasing(self):
        for s in self.s:
            assert s.longestCommonPrefix(["dog", "dogs"]) == "dog"


if __name__ == "__main__":
    unittest.main()
