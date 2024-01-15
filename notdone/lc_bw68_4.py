"""
You are given two positive integers left and right with left <= right. Calculate the product of all integers in the inclusive range [left, right].

Since the product may be very large, you will abbreviate it following these steps:

Count all trailing zeros in the product and remove them. Let us denote this count as C.
For example, there are 3 trailing zeros in 1000, and there are 0 trailing zeros in 546.
Denote the remaining number of digits in the product as d. If d > 10, then express the product as <pre>...<suf> where <pre> denotes the first 5 digits of the product, and <suf> denotes the last 5 digits of the product after removing all trailing zeros. If d <= 10, we keep it unchanged.
For example, we express 1234567654321 as 12345...54321, but 1234567 is represented as 1234567.
Finally, represent the product as a string "<pre>...<suf>eC".
For example, 12345678987600000 will be represented as "12345...89876e5".

"""

import bisect
import operator
import unittest
from collections import *
from functools import reduce
from itertools import *
from string import *

from sortedcontainers import SortedList


# noinspection PyMethodMayBeStatic
class Solution:
    def abbreviateProduct(self, left: int, right: int) -> str:
        return str(reduce(operator.mul, range(left, right + 1))) + "e0"


# noinspection PyMethodMayBeStatic
class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.f = Solution().abbreviateProduct

    def test_passing(self):
        assert self.f(1, 4) == "24e0"

    def test_failing1(self):
        assert self.f(2, 11) == "399168e2"

    def test_failing2(self):
        assert self.f(999998, 1000000) == "99999...00002e6"


if __name__ == "__main__":
    unittest.main()
