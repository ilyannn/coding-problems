from typing import List
import unittest


class Solution:
    def longestCommonPrefix(self, strs: List[str]) -> str:
        a = min(strs) + "A"
        b = max(strs) + "B"
        return a[:next(i for i, (x, y) in enumerate(zip(a, b)) if x != y)]


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.f = Solution().longestCommonPrefix

    def test_empty(self):
        assert self.f(["", "dogs"]) == ""
        assert self.f(["cats", "dogs"]) == ""

    def test_example(self):
        assert self.f(["flower","flow","flight"]) == "fl"
        assert self.f(["dog","racecar","car"]) == ""

    def test_increasing(self):
        assert self.f(["dog", "dogs"]) == "dog"


if __name__ == "__main__":
    unittest.main()
