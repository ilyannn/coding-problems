import unittest
from bisect import bisect


def main(seq):
    levels = []  # (3, 0) (5, -3) (6, -5)
    prev = []  # -1 0 0 0 3 3
    for ix, n in enumerate(seq):
        p = n, -ix
        if not levels or levels[-1][0] < n:
            prev.append(-levels[-1][1] if levels else -1)
            levels.append(p)
        else:
            jx = bisect(levels, p)
            prev.append(-levels[jx - 1][1] if jx else -1)
            levels[jx] = p

    def gen():
        kx = -levels[-1][1]
        while kx >= 0:
            yield seq[kx]  # 6; 5; 3
            kx = prev[kx]

    return list(gen())[::-1]  # 3 5 6


class TestMaxAscending(unittest.TestCase):
    def test_main(self):
        self.assertEqual(main([1]), [1])
        self.assertEqual(main([1, 2, 3, 4]), [1, 2, 3, 4])
        self.assertEqual(main([4, 3, 2, 1]), [1])
        self.assertEqual(main([3, 5, 6, 2, 4]), [3, 5, 6])
        self.assertEqual(main([5, 4, 3, 2, 1, 6, 7, 8, 9, 10]), [1, 6, 7, 8, 9, 10])


if __name__ == "__main__":
    _ = input()
    print(*main([int(s) for s in input().split()]))
