"""315. Count of Smaller Numbers After Self

You are given an integer array nums and you have to return a new counts array. The counts array has the property where counts[i] is the number of smaller elements to the right of nums[i].

---

Writing: 25 minutes
Debugging: 3 minutes
Writing score: 😕😢😢

(without asserts)
Runtime: 7220 ms, faster than 7.12% of Python3 online submissions for Count of Smaller Numbers After Self.
Memory Usage: 45.2 MB, less than 13.66% of Python3 online submissions for Count of Smaller Numbers After Self.
"""


from typing import List


class Node:
    def __init__(self, vals):
        # 😢 Typo when writing an assertion
        assert vals == sorted(vals)
        n = len(vals)
        m = n // 2
        self.val = vals[m]
        self.left = Node(vals[:m]) if m > 0 else None
        self.right = Node(vals[m + 1 :]) if m < n - 1 else None
        self.count = 1
        self.size = n
        self.test()

    # 😢 Forgot self in the method when writing a test
    def test(self):
        assert self.lsize + self.rsize + self.count == self.size

    def __bool__(self):
        return self.size != 0

    @property
    def lsize(self):
        return self.left.size if self.left else 0

    @property
    def rsize(self):
        return self.right.size if self.right else 0

    def less_than(self, val):
        if val <= self.val:
            return self.left.less_than(val) if self.left else 0
        else:
            return (
                self.lsize
                + self.count
                + (self.right.less_than(val) if self.right else 0)
            )

    def pop(self, val):
        if self.left and self.val >= val and self.left.pop(val):
            self.size -= 1
            return True
        if self.val == val and self.count:
            self.count -= 1
            self.size -= 1
            return True
        if self.right and self.val <= val and self.right.pop(val):
            self.size -= 1
            return True
        return False


# 😕 This test name was shadowed in two inner scopes
t = Node([1, 2, 6, 6, 10])
assert [t.less_than(i) for i in range(12)] == [0, 0, 1, 2, 2, 2, 2, 4, 4, 4, 4, 5]
t.pop(10)
assert [t.less_than(i) for i in range(12)] == [0, 0, 1, 2, 2, 2, 2, 4, 4, 4, 4, 4]


class Solution:
    def countSmaller(self, nums: List[int]) -> List[int]:
        root = Node(sorted(nums))
        print(root)

        def gen():
            for n in nums:
                yield root.less_than(n)
                assert root.pop(n)
                root.test()
            assert not root

        return list(gen())
