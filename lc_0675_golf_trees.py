"""675. Cut Off Trees for Golf Event

You are asked to cut off all the trees in a forest for a golf event. The forest is represented as an m x n matrix. In this matrix:

0 means the cell cannot be walked through.
1 represents an empty cell that can be walked through.
A number greater than 1 represents a tree in a cell that can be walked through, and this number is the tree's height.
In one step, you can walk in any of the four directions: north, east, south, and west. If you are standing in a cell with a tree, you can choose whether to cut it off.

You must cut off the trees in order from shortest to tallest. When you cut off a tree, the value at its cell becomes 1 (an empty cell).

Starting from the point (0, 0), return the minimum steps you need to walk to cut off all the trees. If you cannot cut off all the trees, return -1.

You are guaranteed that no two trees have the same height, and there is at least one tree needs to be cut off.
"""

import unittest
from functools import reduce
from itertools import count
from typing import List


def near(x):
    return [x + 256, x - 256, x + 1, x - 1]


def list_dirs(a, b):
    vx = (b % 256) - (a % 256)
    vy = (b // 256) - (a // 256)
    delta = (-1, 0, 1)

    def allowed(d, v):
        if v == 0:
            return d == 0
        if v == 1:
            return d > -1
        if v == -1:
            return d < 1

    for dx in delta:
        for dy in delta:
            if abs(dx) + abs(dy) == 1:
                if allowed(dx, vx) and allowed(dy, vy):
                    yield dx + 256 * dy


def produce_near_greedy(a, target):
    directions = reduce(set.union, (list_dirs(a, b) for b in target), set())
    return lambda x: [(x + d) for d in directions]


def steps(cells, a, target, target2=None, greedy=False):
    visited, current = set(), {a}
    target = set(target)
    target2 = {a} if target2 is None else set(target2)
    near_f = produce_near_greedy(a, target) if greedy else near

    step1 = None
    step2 = None

    for step in count():
        if not current:
            return None
        target.difference_update(current)
        target2.difference_update(current)
        if not target and step1 is None:
            step1 = step
        if not target2 and step2 is None:
            step2 = step
        if step1 is not None and step2 is not None:
            return step1 + step2

        visited.update(current)
        neighbours: set = reduce(set.union, (near_f(c) for c in current), set()) # noqa
        current = neighbours.intersection(cells).difference(visited)


def m_enumerate(matrix):
    for y, row in enumerate(matrix):
        for x, cell in enumerate(row):
            yield (x + 256 * y), cell


class Solution:
    """My solution in about two hours work.

    Runtime: 4252 ms, faster than 84.48% of Python3 online submissions for Cut Off Trees for Golf Event.
    Memory Usage: 16.1 MB, less than 5.60% of Python3 online submissions for Cut Off Trees for Golf Event.

    (1) We first try the greedy algorithm and then BFS
    (2) We encode points as a 16-bit number so that moving in a direction is adding
    (3) To count number of moves from A to B to C we do a BFS from B to both A and C

    Further improvements probably require A* search
    """

    def cutOffTree(self, forest: List[List[int]]) -> int:
        trees = sorted([(-v, p) for p, v in m_enumerate(forest) if v > 1])
        cells = set((p for p, v in m_enumerate(forest) if v > 0))
        start = 0

        if steps(cells, start, (tree_loc for _, tree_loc in trees)) is None:
            return -1

        def walk(loc):
            while trees:
                _, next_loc = trees.pop()
                if (s := steps(cells, loc, [next_loc], greedy=True)) is not None:
                    yield s
                elif not trees:
                    yield steps(cells, loc, [next_loc])
                else:
                    middle_loc = next_loc
                    _, next_loc = trees.pop()
                    yield steps(cells, middle_loc, target=[next_loc], target2=[loc])
                loc = next_loc

        return sum(walk(start))


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.solution = Solution()

    def test_example(self):
        self.assertEqual(self.solution.cutOffTree([[1, 2, 3], [0, 0, 4], [7, 6, 5]]), 6)


if __name__ == "__main__":
    unittest.main()
