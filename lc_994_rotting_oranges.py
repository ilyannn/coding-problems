"""994. Rotting Oranges

https://leetcode.com/problems/rotting-oranges/

---
Runtime: 44 ms, faster than 96.26% of Python3 online submissions for Rotting Oranges.
Memory Usage: 14.4 MB, less than 39.37% of Python3 online submissions for Rotting Oranges.
"""
from itertools import count
from typing import List
import unittest


class Solution:
    def orangesRotting(self, grid: List[List[int]]) -> int:
        R = max(16, len(grid[0]) + 2)

        def select(z):
            return {x + y * R for y, row in enumerate(grid) for x, v in enumerate(row) if v == z}

        fresh, rots = select(1), select(2)

        for step in count():
            if not fresh:
                return step
            if not rots:
                return -1
            rots = fresh.intersection(n for p in rots for n in (p + 1, p - 1, p + R, p - R))
            fresh -= rots


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.f = Solution().orangesRotting

    def test_examples(self):
        assert self.f([[2, 1, 1], [1, 1, 0], [0, 1, 1]]) == 4
        assert self.f([[2, 1, 1], [0, 1, 1], [1, 0, 1]]) == -1
        assert self.f([[0, 2]]) == 0


if __name__ == "__main__":
    unittest.main()
