from itertools import count


def repr_length(number):
    return 0 if number == 1 else len(str(number))


class IntervalNode:
    def __init__(self, left, count):
        self.left = left
        self.count = count
        self.right = left + count - 1
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
    def __init__(self, left, ch, count):
        super().__init__(left, count)
        self.repr_length = repr_length(count) + 1

    def find_leaf(self, target):
        super().find_leaf(target)
        return self

    #    @debug
    def len_between(self, l, r):
        if l <= self.left <= self.right <= r:
            return self.repr_length
        l = max(l, self.left)
        r = min(r, self.right)
        if r >= l:
            return 1 + repr(r - l + 1)
        return 0


class IntervalBranch(IntervalNode):
    def __init__(self, left, nodes):
        super().__init__(left, sum(node.count for node in nodes))
        self.nodes = nodes
        self.repr_length = sum(node.repr_length for node in nodes)

    def find_leaf(self, target):
        super().find_leaf(target)
        node = next(node for node in self.nodes if node.right >= target)
        return node.find_leaf(target)


def main():
    def gen_pairs():
        n = 0
        for c in input():
            if c.isdigit():
                n = 10 * n + int(c)
            else:
                yield c, (n or 1)
                n = 0
        assert not n

    pairs = list(gen_pairs())
    tree = IntervalNode.from_pairs(1, pairs)

    q = int(input())
    for _ in range(q):
        print(tree.len_between(*map(int, input().split())))


if __name__ == "__main__":
    main()
