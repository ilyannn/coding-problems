"""2132. Stamping the Grid

https://leetcode.com/problems/stamping-the-grid/

---

Runtime: 3788 ms, faster than 66.67% of Python3 online submissions for Stamping the Grid.
Memory Usage: 42.8 MB, less than 66.67% of Python3 online submissions for Stamping the Grid.

"""

from itertools import chain
from typing import List
import random
import unittest


def add_arrays(arrays):
    return [sum(x) for x in zip(*arrays)]


assert add_arrays(([1, 2], [3, 4])) == [4, 6]


def neg_array(array):
    return (-x for x in array)


assert add_arrays([[1, 2], neg_array([3, 4])]) == [-2, -2]


def sum_row(row, stampWidth):
    """Yields number of 1s in the window of size stampWidth as the window slides to the right"""
    assert len(row) >= stampWidth
    s = sum(row[:stampWidth])
    yield s
    for p, n in zip(row, row[stampWidth:]):
        s += n - p
        yield s


assert list(sum_row([1, 0, 0, 1, 1], 2)) == [1, 0, 1, 2]
assert len(list(sum_row([random.randint(0, 100) for _ in range(10)], 4))) == 10 - 3


def sum_grid(grid, stampWidth, stampHeight, as_list=False):
    """Yields number of 1s in the stamp of size stampWidth x stampHeight as it slides to the right and down"""
    f = list if as_list else lambda x: x
    s = add_arrays(grid[:stampHeight])
    yield f(sum_row(s, stampWidth))
    for p, n in zip(grid, grid[stampHeight:]):
        s = add_arrays((s, n, neg_array(p)))
        yield list(sum_row(s, stampWidth))


assert list(sum_grid([[1, 0, 0, 1, 1], [1, 0, 0, 1, 1]], 2, 2, as_list=True)) == [
    [2, 0, 2, 4]
]
assert list(
    sum_grid([[1, 0, 0, 0, 1], [1, 1, 0, 1, 1], [0, 0, 0, 1, 0]], 1, 3, as_list=True)
) == [[2, 1, 0, 2, 2]]


class Solution:
    def possibleToStamp(
        self, grid: List[List[int]], stampHeight: int, stampWidth: int
    ) -> bool:
        m, n = len(grid), len(grid[0])

        if n < stampWidth or m < stampHeight:
            # We can't put any stamps, are there any empty spaces?
            return all(chain(*grid))

        def stamp_rows():
            for s_row in sum_grid(grid, stampWidth, stampHeight):
                # Put stamps wherever possible
                yield [0] * (stampWidth - 1) + [not x for x in s_row] + [0] * (
                    stampWidth - 1
                )

        #        for row in stamp_rows():
        #            print(*row)

        def stamps_at_point():
            zero_row = [0] * (n + stampWidth - 1)
            sgrid = (
                [zero_row] * (stampHeight - 1)
                + list(stamp_rows())
                + [zero_row] * (stampHeight - 1)
            )
            return sum_grid(sgrid, stampWidth, stampHeight)

        #        for r in zip(grid, stamps_at_point()):
        #            print(*r)

        return all(sum(v) for r in zip(grid, stamps_at_point()) for v in zip(*r))


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.f = Solution().possibleToStamp

    def test_too_large(self):
        assert self.f([[1, 1, 1], [1, 1, 1]], 3, 2)
        assert not self.f([[1, 1, 1], [1, 0, 1]], 3, 2)

    def test_examples(self):
        assert self.f(
            [[1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0]], 4, 3
        )
        assert not self.f(
            [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]], 2, 2
        )

    def test_square(self):
        assert self.f([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]], 1, 1)
        assert self.f([[1, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 1]], 1, 1)
        assert self.f([[1, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 1]], 2, 2)
        assert self.f([[1, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 1]], 2, 3)
        assert self.f([[1, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 1]], 3, 3)
        assert not self.f(
            [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 0], [0, 0, 0, 1]], 3, 3
        )


if __name__ == "__main__":
    unittest.main()
