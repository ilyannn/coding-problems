import unittest
from itertools import count
from math import floor


def is_workday(base, offset):
    return ((base + offset + 1) % 7) > 1


def quadratic_larger_root(a, b, c):
    """Find the larger root of the quadratic equation"""
    b /= a
    c /= a
    # (x + b/2) ** 2 = -c + b *b / 4
    r = (-c + b * b / 4) ** 0.5
    return -b / 2 + r


def bsearch_solve(f):
    """Solve the equation f(x) == 0 assuming f(0) > 0 and the function decreases"""
    l = 0
    r = 1
    while f(r) >= 0:
        r *= 3

    while r - l > 1:
        assert f(l) >= 0 > f(r)
        m = (l + r) // 2
        if f(m) >= 0:
            l = m
        else:
            r = m

    return l


class LibrarySolver:
    def __init__(self, use_quadratic=True):
        self.use_quadratic = use_quadratic

    def solve(self, k, m, d) -> int:
        """Solve the library problem using one of the two methods"""

        def simulate(from_books, from_week, to_week=None):
            left_books = from_books
            start_day = 7 * from_week + 1

            if to_week is None:
                days = count(start_day)
            else:
                days = range(start_day, 7 * to_week + 1)

            for day in days:
                left_books += (k if is_workday(d, day - 1) else 0) - day
                if left_books < 0:
                    return day - 1

        first_week = simulate(m, 0, 1)
        if first_week is not None:
            return first_week

        # f(x) = needs - has
        # f(0) <= 0 and f(infty) > 0
        # arg min f between 0 and 1
        k_needs = 49, 7, 0
        k_has = 0, 10 * k, 2 * m
        k_coef = [n - h for n, h in zip(k_needs, k_has)]

        def left_after_weeks(weeks):
            return -(k_coef[0] * weeks**2 + k_coef[1] * weeks + k_coef[2]) // 2

        if self.use_quadratic:
            weeks = floor(quadratic_larger_root(*k_coef))
        else:
            weeks = bsearch_solve(left_after_weeks)

        left = left_after_weeks(weeks)
        assert left >= 0

        return simulate(left, weeks)


class TestLibrarySolution(unittest.TestCase):
    def test_workday(self):
        self.assertFalse(is_workday(6, 1))
        self.assertTrue(is_workday(6, 2))
        self.assertTrue(is_workday(6, 6))
        self.assertFalse(is_workday(6, 7))
        self.assertTrue(is_workday(1, 0))
        self.assertFalse(is_workday(6, 0))
        self.assertFalse(is_workday(7, 0))
        self.assertFalse(is_workday(6, 1))
        self.assertTrue(is_workday(7, 1))

    def test_quadratic_larger_root(self):
        self.assertEqual(quadratic_larger_root(1, 0, -1), 1)
        self.assertEqual(quadratic_larger_root(1, -2, 1), 1)

    def test_solve_library(self):
        for parameter in [False, True]:
            solve_library = LibrarySolver(parameter).solve
            self.assertEqual(solve_library(1, 1, 1), 2)
            self.assertEqual(solve_library(1, 1, 2), 2)
            self.assertEqual(solve_library(1, 1, 3), 2)
            self.assertEqual(solve_library(1, 1, 4), 2)
            self.assertEqual(solve_library(1, 1, 5), 1)
            self.assertEqual(solve_library(1, 1, 6), 1)
            self.assertEqual(solve_library(1, 1, 7), 1)
            self.assertEqual(solve_library(1, 2, 7), 2)
            self.assertEqual(solve_library(2, 1, 7), 2)
            self.assertEqual(solve_library(2, 1, 2), 3)

    def test_solve_fails_immediately(self):
        for parameter in [False, True]:
            solve_library = LibrarySolver(parameter).solve
            self.assertEqual(solve_library(0, 0, 6), 0)
            self.assertEqual(solve_library(1, 0, 6), 0)
            self.assertEqual(solve_library(100, 0, 6), 0)


def main():
    print(LibrarySolver().solve(*(map(int, input().split()))))


if __name__ == "__main__":
    main()
