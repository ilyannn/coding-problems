"""697. Degree of an Array

---

Runtime: 374 ms, faster than 26.03% of Python3 online submissions for Degree of an Array.
Memory Usage: 15.3 MB, less than 91.43% of Python3 online submissions for Degree of an Array.

"""

from collections import defaultdict
from typing import List
import unittest


class Solution:
    def findShortestSubArray(self, nums: List[int]) -> int:
        """One-pass solution"""
        count = defaultdict(int)

        mini = {}
        leni = {}
        for i, n in enumerate(nums):
            count[n] += 1
            mini.setdefault(n, i)
            leni[n] = i + 1 - mini[n]

        c = max(count.values())
        return min(leni[n] for n, c1 in count.items() if c1 == c)


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.f = Solution().findShortestSubArray

    def test_trivial(self):
        assert self.f([1, 1, 1]) == 3

    def test_example(self):
        assert self.f([1, 2, 2, 3, 1]) == 2
        assert self.f([1, 2, 2, 3, 1, 4, 2]) == 6


if __name__ == "__main__":
    unittest.main()
