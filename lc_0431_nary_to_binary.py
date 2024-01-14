"""431.  Encode N-ary Tree to Binary Tree"""

import operator
import unittest
from typing import Optional


class NAryNode:
    def __init__(self, val=None, children=None):
        self.val = val
        self.children = children or []

    def __eq__(self, other):
        if not hasattr(other, "val") or not hasattr(other, "children"):
            return False
        if self.val != other.val:
            return False
        if len(self.children) != len(other.children):
            return False
        return all(map(operator.eq, self.children, other.children))

    def __len__(self):
        return 1 + sum(map(len, self.children))

    def __str__(self):
        parts = [str(x) for x in (self.val, *self.children)]
        return parts[0] if len(parts) == 1 else f"({', '.join(parts)})"

    def __repr__(self):
        return f"NAryNode(val={repr(self.val)}, children={self.children})"


def tuple_to_nary(data):
    match data:
        case (val, *kids):
            return NAryNode(val, [tuple_to_nary(kid) for kid in kids])
        case val:
            return NAryNode(val)


assert tuple_to_nary((4, 6)) == NAryNode(4, [NAryNode(6)])
assert tuple_to_nary((4, (6, 7))) == NAryNode(4, [NAryNode(6, [NAryNode(7)])])
assert str(tuple_to_nary((4, (6, 7)))) == str((4, (6, 7)))
assert eval(repr(tuple_to_nary(("3", "5")))) == NAryNode("3", [NAryNode("5")])


class BinaryNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

    def __eq__(self, other):
        if (
            not hasattr(other, "val")
            or not hasattr(other, "left")
            or not hasattr(other, "right")
        ):
            return False
        if self.val != other.val:
            return False
        if not self.left and other.left:
            return False
        if self.left and not self.left == other.left:
            return False
        if not self.right and other.right:
            return False
        if self.right and not self.right == other.right:
            return False
        return True

    def __len__(self):
        return 1 + len(self.right or []) + len(self.left or [])

    def __str__(self):
        l = str(self.left) if self.left else ""
        r = str(self.right) if self.right else ""

        return f"({l} {self.val} {r})"


assert BinaryNode(5, BinaryNode(1)) == BinaryNode(5, BinaryNode(1))
assert BinaryNode(5, BinaryNode(1)) != BinaryNode(5, BinaryNode(2))
assert BinaryNode(5, BinaryNode(1)) != BinaryNode(5, None, BinaryNode(1))


def go_a_viking(vikings: [NAryNode]):
    match vikings:
        case []:
            return None

        case [kid]:
            return BinaryNode(-1, to_binary(kid))

        case [*brothers, left, right]:
            node = BinaryNode(-2, to_binary(left), to_binary(right))
            while brothers:
                node = BinaryNode(node.val - 1, to_binary(brothers.pop()), node)
            return node


def to_binary(node: Optional[NAryNode]):
    match node and (node.children or [None]):
        case [firstborn, *vikings]:
            return BinaryNode(node.val, to_binary(firstborn), go_a_viking(vikings))


def to_nary(node: Optional[BinaryNode]):
    if not node:
        return

    def gen():
        ship = node
        while ship:
            yield ship.left
            ship = ship.right
            if not ship:
                return
            if ship.val >= -2:
                assert -ship.val + (not ship.right) == 2
            if ship.val == -2:
                yield ship.left
                yield ship.right
                return

    return NAryNode(node.val, node.left and list(map(to_nary, gen())))


example = tuple_to_nary([1, [3, 5, 6], 2, 4])


def debug_out(nary):
    binary = to_binary(nary)
    nary2 = to_nary(binary)
    print("✅" if nary == nary2 else "❌", end="   ")
    print(nary, binary, nary2, sep=" → ", end="   ")
    print("{", len(nary), "→", len(binary), "binary nodes", "}")


class MyTestCase(unittest.TestCase):
    def test_empty(_):
        assert to_binary(None) is None
        assert to_nary(None) is None

    def test_leaf(_):
        assert to_nary(BinaryNode(5)) == NAryNode(5)
        assert to_binary(NAryNode(10)) == BinaryNode(10)

    def test_simple(_):
        for n in range(10):
            simple = NAryNode(n**3, [NAryNode(i**2 + 5) for i in range(n)])
            try:
                assert to_nary(to_binary(simple)) == simple
            except AssertionError:
                debug_out(simple)
                raise

    def test_example(_):
        assert to_nary(to_binary(example)) == example

    def test_negatives(_):
        for i in (-1, -2):
            negative = tuple_to_nary([i, [i, [i], [i]], [i], [i]])
            assert to_nary(to_binary(negative)) == negative


if __name__ == "__main__":
    debug_out(example)
    unittest.main()
