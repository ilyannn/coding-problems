"""14. Longest Common Prefix"""
import unittest
from itertools import takewhile, zip_longest
from typing import List


class Solution1:
    @staticmethod
    def longestCommonPrefix(strs: List[str]) -> str:
        return "".join(
            s.pop() for s in takewhile(lambda s: len(s) == 1, map(set, zip(*strs)))
        )


class Solution2:
    @staticmethod
    def longestCommonPrefix(strs: List[str]) -> str:
        a, b = min(strs), max(strs)
        return a[: next((i for i, (x, y) in enumerate(zip(a, b)) if x != y), len(a))]


class Solution3:
    @staticmethod
    def longestCommonPrefix(strs: List[str]) -> str:
        return strs[0][
            : next(
                (
                    i
                    for i, (x, y) in enumerate(zip_longest(min(strs), max(strs)))
                    if x != y
                ),
                len(strs[0]),
            )
        ]


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.s = [Solution1(), Solution2(), Solution3()]

    def test_empty(self):
        for s in self.s:
            assert s.longestCommonPrefix(["", "dogs"]) == ""
            assert s.longestCommonPrefix(["cats", "dogs"]) == ""

    def test_example(self):
        for s in self.s:
            assert s.longestCommonPrefix(["flower", "flow", "flight"]) == "fl"
            assert s.longestCommonPrefix(["dog", "racecar", "car"]) == ""

    def test_increasing(self):
        for s in self.s:
            assert s.longestCommonPrefix(["dog", "dogs"]) == "dog"

    def test_decreasing(self):
        for s in self.s:
            assert s.longestCommonPrefix(["ab", "a"]) == "a"


if __name__ == "__main__":
    unittest.main()
