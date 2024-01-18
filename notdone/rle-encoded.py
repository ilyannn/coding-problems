# https://coderun.yandex.ru/problem/find-rle-string-length

import unittest
from abc import ABC, abstractmethod
from itertools import count


def repr_length(number):
    return 0 if number == 1 else len(str(number))


class IntervalNode(ABC):
    def __init__(self, left, length):
        self.left = left
        self.length = length
        self.right = left + length - 1
        self.repr_length = 0

    @staticmethod
    def from_pairs(left, pairs):
        if len(pairs) == 1:
            return IntervalLeaf(left, *pairs[0])

        def gen():
            D = min(len(pairs), 2)
            S = len(pairs) // D
            node_left = left
            for i in count():
                if i * S >= len(pairs):
                    break
                node = IntervalNode.from_pairs(node_left, pairs[i * S : (i + 1) * S])
                node_left = node.right + 1
                yield node

        return IntervalBranch(left, list(gen()))

    @abstractmethod
    def find_leaf(self, target):
        assert self.left <= target <= self.right

    def len_between(self, l, r):
        ll = self.find_leaf(l)
        rl = self.find_leaf(r)

        if ll is rl:
            return repr_length(r - l + 1) + 1

        llen = repr_length(ll.right - l + 1) + 1
        rlen = repr_length(r - rl.left + 1) + 1

        return rl.left - ll.right - 1 + llen + rlen


def debug(f):
    def fun(*p):
        r = f(*p)
        print(p, "->", r)
        return r

    return fun


class IntervalLeaf(IntervalNode):
    def __init__(self, left, ch, length):
        super().__init__(left, length)
        self.repr_length = repr_length(length) + 1

    def find_leaf(self, target):
        super().find_leaf(target)
        return self


class IntervalBranch(IntervalNode):
    def __init__(self, left, nodes):
        super().__init__(left, sum(node.length for node in nodes))
        self.nodes = nodes
        self.repr_length = sum(node.repr_length for node in nodes)

    def find_leaf(self, target):
        super().find_leaf(target)
        node = next(node for node in self.nodes if node.right >= target)
        return node.find_leaf(target)


def rle_encoded(string, queries):
    def gen_pairs():
        n = 0
        for c in string:
            if c.isdigit():
                n = 10 * n + int(c)
            else:
                yield c, (n or 1)
                n = 0
        assert not n

    pairs = list(gen_pairs())
    tree = IntervalNode.from_pairs(1, pairs)
    return [tree.len_between(*query) for query in queries]


class TestHelpers(unittest.TestCase):
    def test_repr_length(self):
        self.assertEqual(repr_length(1), 0)
        self.assertEqual(repr_length(10), 2)
        self.assertEqual(repr_length(100), 3)
        self.assertEqual(repr_length(123456), 6)


# Test the class `IntervalLeaf`
class TestIntervalMethods(unittest.TestCase):
    def test_leaf_find_leaf(self):
        leaf = IntervalLeaf(0, "a", 5)
        self.assertEqual(leaf.find_leaf(3), leaf)

    def test_branch_find_leaf(self):
        leaf1 = IntervalLeaf(0, "a", 5)
        leaf2 = IntervalLeaf(5, "b", 5)
        branch = IntervalBranch(0, [leaf1, leaf2])

        self.assertEqual(branch.find_leaf(2), leaf1)
        self.assertEqual(branch.find_leaf(5), leaf2)
        self.assertEqual(branch.find_leaf(7), leaf2)

    def test_len_between(self):
        node1 = IntervalLeaf(0, "a", 5)
        node2 = IntervalLeaf(5, "b", 5)
        branch = IntervalBranch(0, [node1, node2])

        self.assertEqual(branch.len_between(0, 9), 4)


class TestRleEncoded(unittest.TestCase):
    def test_rle_encoded_1(self):
        s = "10a"
        qs = [[1, 1], [3, 7], [1, 10]]
        result = rle_encoded(s, qs)
        self.assertListEqual(result, [1, 2, 3])

    def test_rle_encoded_2(self):
        s = "3a2b"
        qs = [[1, 1], [3, 4], [1, 5]]
        result = rle_encoded(s, qs)
        self.assertListEqual(result, [1, 2, 4])

    def test_rle_encoded_3(self):
        s = "3ab2c"
        qs = [[1, 3], [1, 4], [4, 5], [5, 5]]
        result = rle_encoded(s, qs)
        self.assertListEqual(result, [2, 3, 2, 1])


if __name__ == "__main__":
    s = input()
    q = int(input())
    qs = [[int(v) for v in input().split()] for _ in range(q)]
    print(*rle_encoded(s, qs), sep="\n")
