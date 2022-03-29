"""329. Longest Increasing Path in a Matrix

Given an m x n integers matrix, return the length of the longest increasing path in matrix.

From each cell, you can either move in four directions: left, right, up, or down. You may not move diagonally or move outside the boundary (i.e., wrap-around is not allowed).

---

Writing time: 15 minutes
Debugging time: 10 minutes
Writing score: 😕😕😕😕🤬🤬

Runtime: 828 ms, faster than 12.95% of Python3 online submissions for Longest Increasing Path in a Matrix.
Memory Usage: 22.3 MB, less than 5.23% of Python3 online submissions for Longest Increasing Path in a Matrix.

"""

from collections import defaultdict
from typing import List


class Solution:
    def longestIncreasingPath(self, matrix: List[List[int]]) -> int:
        m, n = len(matrix), len(matrix[0])
        R = n + 2  # 😕 Now unused

        # 😕 This has been rewritten back to regular pairs
        def m_enumerate():
            for y, row in enumerate(matrix):
                for x, v in enumerate(row):
                    yield (x, y), v

        def neighbors(x, y):
            if x > 0:
                yield x - 1, y
            if x < n - 1:
                yield x + 1, y
            if y > 0:
                yield x, y - 1
            if y < m - 1:
                yield x, y + 1

        edges = defaultdict(set)
        cur = set()
        incoming = set()
        for p, v in m_enumerate():
            cur.add(p)
            for q in neighbors(*p):
                # 🤬 Neighbors weren't handled correctly
                if matrix[q[1]][q[0]] > v:
                    edges[p].add(q)
                    incoming.add(q)

        def forward(s):
            return {q for p in s for q in edges[p]}  # 😕 Whitespace syntax

        cur -= incoming

        for step in count():  # 😕 Wasn't imported
            # 🤬 Algorithm was rewritten
            if not cur:
                return step
            cur = forward(cur)
