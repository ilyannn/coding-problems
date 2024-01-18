import unittest

from collections import Counter
from functools import cache


@cache
def howmany(bottles: tuple):
    if len(bottles) == 1:
        return bottles[0] + 1

    def sub(ix):
        bottles1 = sorted((jb - (jx == ix) for jx, jb in enumerate(bottles)))
        return tuple(b for b in bottles1 if b)

    return sum(howmany(sub(i)) for i in range(len(bottles))) + 1


def main(letters):
    c = sorted(Counter(letters).values())
    return howmany(tuple(c)) - 1


class TestHowMany(unittest.TestCase):
    def test_howmany(self):
        self.assertEqual(howmany((5,)), 6)
        self.assertEqual(howmany((1, 1)), 5)
        self.assertEqual(howmany((1, 1, 1)), 16)


class TestMain(unittest.TestCase):
    def test_main(self):
        self.assertEqual(main("ab"), 4)
        self.assertEqual(main("abc"), 15)
        self.assertEqual(main("aaaaa"), 5)


if __name__ == "__main__":
    print(main(input().strip()))
