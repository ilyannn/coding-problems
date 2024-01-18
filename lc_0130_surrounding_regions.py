import unittest
from typing import List


class Solution:
    def solve(self, grid: List[List[str]]) -> None:
        m, n = len(grid[0]), len(grid)
        zeros = {
            (x, y)
            for y, row in enumerate(grid)
            for x, ch in enumerate(row)
            if ch == "O"
        }
        saved = {(x, y) for x, y in zeros if not x or not y or x == m - 1 or y == n - 1}

        def neighbors(x, y):
            yield x + 1, y
            yield x - 1, y
            yield x, y + 1
            yield x, y - 1

        unsaved = zeros - saved

        q = list(saved)
        while q:
            p = q.pop()
            for n in neighbors(*p):
                if n in unsaved:
                    unsaved.remove(n)
                    q.append(n)

        for x, y in unsaved:
            grid[y][x] = "X"


class TestSolution(unittest.TestCase):
    def test_solve(self):
        s = Solution()

        grid = [
            ["X", "X", "X", "X"],
            ["X", "O", "O", "X"],
            ["X", "X", "O", "X"],
            ["X", "O", "X", "X"],
        ]
        s.solve(grid)

        expected = [
            ["X", "X", "X", "X"],
            ["X", "X", "X", "X"],
            ["X", "X", "X", "X"],
            ["X", "O", "X", "X"],
        ]

        self.assertEqual(grid, expected)


if __name__ == "__main__":
    unittest.main()
