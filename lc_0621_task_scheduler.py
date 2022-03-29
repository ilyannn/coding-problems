from collections import Counter
from itertools import count
from typing import List
import unittest


class Solution:
    def leastInterval(self, tasks: List[str], n: int) -> int:

        task_list = [(v, 0) for v in Counter(tasks).values()]

        for time in count():
            if not task_list:
                return time

            tx, ix = max(
                ((t, i) for i, (t, b) in enumerate(task_list) if time >= b),
                default=(None, None),
            )

            if ix is not None:
                task_list[ix : ix + 1] = [(tx - 1, time + n + 1)] if tx > 1 else []


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.f = Solution().leastInterval

    def test_examples(self):
        assert self.f(["A", "A", "A", "B", "B", "B"], 2) == 8
        assert self.f(["A", "A", "A", "B", "B", "B"], 0) == 6
        assert (
            self.f(["A", "A", "A", "A", "A", "A", "B", "C", "D", "E", "F", "G"], 2)
            == 16
        )

    def test_simple(self):
        assert self.f(["A"], 100) == 1
        assert self.f(["A", "A"], 100) == 102


if __name__ == "__main__":
    unittest.main()
