import unittest


class TestFenwickTree(unittest.TestCase):
    def setUp(self):
        self.t = FenwickTree(3)

    def test_add_and_upto(self):
        self.t.add(2)
        self.assertEqual(self.t.upto(0), 0)
        self.assertEqual(self.t.upto(1), 0)
        self.assertEqual(self.t.upto(2), 1)
        self.assertEqual(self.t.upto(3), 1)

    def test_min_free(self):
        self.t.add(2)
        self.assertEqual(self.t.min_free(), 1)
        self.t.add(1)
        self.t.add(3)
        self.assertEqual(self.t.min_free(), 4)

    def test_remove(self):
        self.t.add(2)
        self.t.add(1)
        self.assertEqual(self.t.min_free(), 3)
        self.t.add(3)
        self.t.remove(2)
        self.assertEqual(self.t.min_free(), 2)


class FenwickTree:
    """Simple Fenwick tree. The keys are numbered from 1 to 2^k."""

    def __init__(self, N):
        while N != (N & -N):
            N += N & -N
        self.N = N
        self.cell = [0] * (N + 1)

    def add(self, key, value=1):
        """Add a value to the specified key in the tree."""
        while key <= self.N:
            self.cell[key] += value
            key += key & -key

    def remove(self, key):
        """Subtract 1 from the value of the specified key in the tree."""
        self.add(key, -1)

    def upto(self, key):
        """Sum the values of the keys that are smaller or equal to the given tree."""
        s = 0
        c = min(key, self.N)
        while c:
            s += self.cell[c]
            c -= c & -c
        return s

    def min_free(self):
        """Find the smallest key for which the value is 0.

        Requirement: all values are 0 or 1.

        :return: The minimum free key (self.N + 1 if all keys are set).
        """
        r = 1
        while self.cell[r] == r:
            r *= 2
            if r > self.N:
                return self.N + 1

        b = r // 2
        while b > 1:
            # [r - b + 1; r] has the answer
            b = b // 2
            m = r - b
            if self.cell[m] < b:
                r = m
            else:
                assert self.cell[m] == b

        return r


def main():
    k, n = map(int, input().split())

    def gen():
        for train in range(n):
            arrive, leave = [int(s) for s in input().split()]
            yield arrive, False, train
            yield leave, True, train

    events = sorted(list(gen()))

    # platforms are numbered from 1 to k
    platforms = FenwickTree(k)
    # trains are numbered from 0 to n-1
    trains = []

    def find_platforms():
        for _, leave, train in events:
            if leave:
                assert train < len(trains)
                platforms.remove(trains[train])
            elif (platform := platforms.min_free()) <= k:
                assert len(trains) == train
                trains.append(platform)
                platforms.add(platform)
            else:
                return 0, train + 1
        return trains

    print(*find_platforms())


if __name__ == "__main__":
    main()
