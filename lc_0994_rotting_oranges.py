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
        """Find rotting oranges using BFS

        Additional optimizations:
             - We encode board positions using small numbers of the form x + y * R
             - Neighbors of a position p are computed as p ± 1, p ± R
             - One selects R ≥ N + 2 since a * R - 1 must be distinguishable from b * R + N
        """
        R = max(16, len(grid[0]) + 2)

        def select(z):
            return {
                x + y * R
                for y, row in enumerate(grid)
                for x, v in enumerate(row)
                if v == z
            }

        fresh, rots = select(1), select(2)

        # At each step keep the sets of fresh and currently rotting oranges
        for step in count():
            # If all oranges are rotten, we are done
            if not fresh:
                return step
            # If no oranges can rot, we stop the process as well
            if not rots:
                return -1
            # If we have some fresh and some just rotten oranges, we compute the next rotting batch
            rots = fresh.intersection(
                n for p in rots for n in (p + 1, p - 1, p + R, p - R)
            )
            fresh -= rots
        # The loop eventually terminates: either the number of elements in fresh goes down,
        # or the process is stopped during the next iteration.


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.f = Solution().orangesRotting

    def test_examples(self):
        assert self.f([[2, 1, 1], [1, 1, 0], [0, 1, 1]]) == 4
        assert self.f([[2, 1, 1], [0, 1, 1], [1, 0, 1]]) == -1
        assert self.f([[0, 2]]) == 0


if __name__ == "__main__":
    unittest.main()
