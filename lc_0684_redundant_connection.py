# https://leetcode.com/problems/redundant-connection/solutions/4598163/strip-out-the-leaves-and-the-cycle-is-revealed
"""
We apply topological sort to remove everything except the cycle.
Time complexity: O(n) (we perform constant operations per vertex), assuming accessing the dictionary is constant.
Space complexity: O(n) (we store constant additional info per node)
"""
import unittest
from collections import defaultdict
from typing import List


class Solution:
    def findRedundantConnection(self, edges: List[List[int]]) -> List[int]:
        # Process the edges into a vertex dictionary.
        v = defaultdict(set)
        for a, b in edges:
            v[a].add(b)
            v[b].add(a)

        # Strip out the tree part, starting from the leaves.
        leaves = {x for x, e in v.items() if len(e) == 1}

        while leaves:
            x = leaves.pop()
            y = v[x].pop()
            assert not v[x]
            del v[x]
            v[y].remove(x)
            if len(v[y]) == 1:
                leaves.add(y)

        # Only the cycle is left now.
        assert all(len(e) == 2 for e in v.values())

        for a, b in reversed(edges):
            if a in v and b in v[a]:
                return [a, b]


class TestSolution(unittest.TestCase):
    def setUp(self):
        self.solution = Solution().findRedundantConnection

    def test_findRedundantConnection(self):
        self.assertEqual(
            self.solution([[1, 2], [1, 3], [2, 3]]),
            [2, 3],
        )
        self.assertEqual(
            self.solution([[1, 2], [2, 3], [3, 4], [1, 4], [1, 5]]),
            [1, 4],
        )


if __name__ == "__main__":
    unittest.main()
