import unittest
from bisect import bisect_left
from math import inf
from typing import List


class SolutionShort:
    def maxEnvelopes(self, envelopes: List[List[int]]) -> int:
        m = [inf] * (len(envelopes) + 1)
        for _, h in sorted(envelopes, key=lambda x: (x[0], -x[1])):
            m[bisect_left(m, h)] = h
        return m.index(inf)


def set_val(a, v, i):
    a[i : i + 1] = [v]


class SolutionReadable:
    def maxEnvelopes(self, envelopes: List[List[int]]) -> int:
        m = []
        for _, h in sorted(envelopes, key=lambda x: (x[0], -x[1])):
            set_val(m, h, bisect_left(m, h))
        return len(m)


# noinspection PyMethodMayBeStatic
class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.solutions = [SolutionShort(), SolutionReadable()]

    def test_examples(self):
        for solution in self.solutions:
            assert solution.maxEnvelopes([[5, 4], [6, 4], [6, 7], [2, 3]]) == 3
            assert solution.maxEnvelopes([[1, 1], [1, 1], [1, 1]]) == 1

    def test_simple(self):
        for solution in self.solutions:
            assert solution.maxEnvelopes([[3, 5]]) == 1

    def test_complex(self):
        for solution in self.solutions:
            assert (
                solution.maxEnvelopes([[100, 50], [80, 60], [30, 30], [50, 100]]) == 2
            )


if __name__ == "__main__":
    unittest.main()
