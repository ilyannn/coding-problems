import unittest
from typing import List


class Solution:
    def largestIsland(self, grid: List[List[int]]) -> int:
        N = len(grid)
        R = range(N)

        def compact(x, y):
            return -x * N - y - 1

        def neighbors(x, y):
            return set(
                n
                for n in [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
                if all(c in R for c in n)
            )

        g = {(x, y): grid[x][y] for x in R for y in R}

        def dfs(p, i):
            if g.get(p) == 1:
                yield p
                g[p] = i
                for n in neighbors(*p):
                    yield from dfs(n, i)

        isles = {compact(*k): len(list(dfs(k, compact(*k)))) for k in g}

        return max(
            list(isles.values())
            + [
                sum(isles[isle] for isle in set(g[n] for n in neighbors(*k)) if isle)
                + 1
                for k, v in g.items()
                if not v
            ]
        )


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.solution = Solution()

    def test_empty(self):
        grid = [[0, 0], [0, 0]]
        self.assertEqual(self.solution.largestIsland(grid), 1)

    def test_three(self):
        grid = [[0, 1], [1, 0]]
        self.assertEqual(self.solution.largestIsland(grid), 3)

    def test_square(self):
        grid = [[1, 1], [1, 1]]
        self.assertEqual(self.solution.largestIsland(grid), 4)
