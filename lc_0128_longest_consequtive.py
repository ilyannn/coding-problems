"""128. Longest Consecutive Sequence

Runtime: 334ms
Beats 96.86% of users with Python3
"""
import unittest
from itertools import count
from typing import List


class Solution:
    def longestConsecutive(self, nums: List[int]) -> int:
        els = set(nums)

        def gen():
            for n in els:
                if n - 1 not in els and n + 1 in els:
                    for k in count(2):
                        if n + k not in els:
                            yield k
                            break

        return max(gen(), default=1) if nums else 0


class LongestConsecutiveTests(unittest.TestCase):
    def setUp(self):
        self.sol = Solution()

    def test_longestConsecutive(self):
        self.assertEqual(self.sol.longestConsecutive([]), 0)
        self.assertEqual(self.sol.longestConsecutive([100, 4, 200, 1, 3, 2]), 4)
        self.assertEqual(self.sol.longestConsecutive([1, 2, 0, 1]), 3)
        self.assertEqual(self.sol.longestConsecutive([0, 3, 7, 2, 5, 8, 4, 6, 0, 1]), 9)


if __name__ == "__main__":
    unittest.main()
