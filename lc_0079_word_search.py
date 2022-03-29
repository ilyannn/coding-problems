"""79. Word Search

https://leetcode.com/problems/word-search/

---

Submitted three times, the fastest was:
Runtime: 32 ms, faster than 99.87% of Python3 online submissions for Word Search.
"""

import unittest
from collections import Counter, defaultdict
from typing import List


# noinspection PyMethodMayBeStatic
class Solution:
    def exist(self, board: List[List[str]], word: str) -> bool:
        m, n = len(board), len(board[0])
        cur = None

        def neighbors(x, y):
            if x > 0:
                yield x - 1, y
            if x < n - 1:
                yield x + 1, y
            if y > 0:
                yield x, y - 1
            if y < m - 1:
                yield x, y + 1

        def board_at(q):
            return board[q[1]][q[0]]

        def menumerate():
            for y in range(m):
                for x in range(n):
                    yield (x, y), board[y][x]

        board_per_ch = defaultdict(set)
        for p, ch in menumerate():
            board_per_ch[ch].add(p)

        for ch, k in Counter(word).items():
            if len(board_per_ch[ch]) < k:
                return False

        cur = board_per_ch[word[0]]
        for ch in word[1:]:
            cur = set((p for q in cur for p in neighbors(*q))).intersection(
                board_per_ch[ch]
            )
            if not cur:
                return False

        visited = set()

        def dfs(remains, point):
            if not remains:
                return True
            c = word[remains - 1]
            visited.add(point)
            try:
                return any(
                    (
                        dfs(remains - 1, q)
                        for q in neighbors(*point)
                        if board_at(q) == c and q not in visited
                    )
                )
            finally:
                visited.remove(point)

        return any(dfs(len(word) - 1, c) for c in cur)


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.f = Solution().exist

    def test_examples(self):
        assert self.f(
            [["A", "B", "C", "E"], ["S", "F", "C", "S"], ["A", "D", "E", "E"]], "ABCCED"
        )

        assert self.f(
            [["A", "B", "C", "E"], ["S", "F", "C", "S"], ["A", "D", "E", "E"]], "SEE"
        )

        assert not self.f(
            [["A", "B", "C", "E"], ["S", "F", "C", "S"], ["A", "D", "E", "E"]], "ABCB"
        )

    def test_simple(self):
        assert self.f([["X"]], "X")
        assert not self.f([["X"]], "Y")


if __name__ == "__main__":
    unittest.main()
