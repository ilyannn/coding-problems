"""1192. Critical Connections in a Network

There are n servers numbered from 0 to n - 1 connected by undirected server-to-server connections forming a network
where connections[i] = [ai, bi] represents a connection between servers ai and bi. Any server can reach other servers
directly or indirectly through the network.

A critical connection is a connection that, if removed, will make some servers unable to reach some other server.

Return all critical connections in the network in any order.
"""

import unittest
from collections import defaultdict
from random import choice
from typing import List


class Solution:
    def criticalConnections(
        self, n: int, connections: List[List[int]]
    ) -> List[List[int]]:
        """Find critical connections

        Complexity notes:
         - dfs_reach is executed exactly once for each node (see two asserts).
         - the inner loop in dfs_rank is executed once for each nearby node.
        Thus, the complexity is O(number of edges).
        """
        nearby = defaultdict(set)
        for x, y in connections:
            nearby[x].add(y)
            nearby[y].add(x)

        rank = [0] * n  # In this array 0 means unvisited
        answer = []  # We'll collect critical edges here

        def dfs_rank(depth, node):
            """Visit the node and update its rank.

            Updates rank with minimal rank that can be visited from node (without
            going back through the node→parent edge – it's been deleted from `nearby`).
            """
            assert not rank[node]

            # Preliminary value to be corrected later
            rank[node] = depth

            for child in nearby[node]:
                # Do the DFS for any unvisited children
                if not rank[child]:
                    nearby[child].remove(node)  # Make sure we don't go back
                    dfs_rank(depth + 1, child)

                # node→f is part of a cycle iff we can reach a node of lower or same rank
                if rank[child] > depth:
                    answer.append([node, child])

            # Update the node's rank using all the information
            rank[node] = min(
                (rank[child] for child in nearby[node]), default=float("inf")
            )

        dfs_rank(1, choice(range(n)))  # Doesn't matter where we start
        assert all(rank[i] for i in range(n))  # The graph is connected
        return answer


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.solution = Solution()

    def test_1(self):
        answer = self.solution.criticalConnections(4, [[0, 1], [1, 2], [2, 0], [1, 3]])
        self.assertEqual(len(answer), 1)
        self.assertEqual(set(answer[0]), {1, 3})
