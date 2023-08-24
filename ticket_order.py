"""Problem from https://binarysearch.com/problems/Ticket-Order"""

import unittest


class Fenwick:
    def __init__(self, n):
        self.data = [0] * (n + 1)
        self.count = 0  # Same as self.leq(len(self.data)), but O(1)

    def __len__(self):
        return self.count

    def add(self, v):
        self.count += 1
        while v < len(self.data):
            self.data[v] += 1
            v += v & -v

    def leq(self, v):
        a = 0
        while v:
            a += self.data[v]
            v -= v & -v
        return a


if True:
    tree = Fenwick(10)
    assert not tree
    tree.add(5)
    assert tree
    assert not tree.leq(4)
    assert tree.leq(5) == 1


class Solution:
    def solve(self, tickets):
        n = len(tickets)
        answer = [0] * n
        # Use Fenwick tree to fill an array
        # so that we can answer the question like
        # "how many people from [A, B] have tickets[j] < t"
        done = Fenwick(n)
        # At time NOW everyone has got TICK tickets and PERSON is next
        now, tick, person = 0, 0, 0
        for t, i in sorted((t, i) for i, t in enumerate(tickets)):
            if t > tick + 1 and person:
                now += n - done.leq(person)
                tick += 1
                tick = t - 1
                now += (tick - ct) * (n - done.count)
                person = 0
            answer[i] = (
                answerp
                + left * (t - tp)
                + "number of people in the tree <= i"
                - "number of people in the tree < ip"
            )
            done.add(i)
        return answer


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.f = Solution().solve

    def test_example(self):
        assert self.f([2, 1, 2]) == [4, 2, 5]

    def test_simple(self):
        assert self.f([2]) == [2]


if __name__ == "__main__":
    unittest.main()
