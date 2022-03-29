""" 155. Min Stack
Design a stack that supports push, pop, top, and retrieving the minimum element in constant time.

Implement the MinStack class:

- MinStack() initializes the stack object.
- void push(int val) pushes the element val onto the stack.
- void pop() removes the element on the top of the stack.
- int top() gets the top element of the stack.
- int getMin() retrieves the minimum element in the stack.
"""

import unittest


class MinStack:
    """Single stack solution

    Runtime: 40 ms, faster than 99.99% of Python3 online submissions for Min Stack.
    Memory Usage: 17.9 MB, less than 93.47% of Python3 online submissions for Min Stack.
    """

    def __init__(self):
        self.deltas = []
        self.min = None

    def push(self, val: int) -> None:
        if not self.deltas:
            self.min = val
        d = val - self.min
        self.deltas.append(d)
        if d < 0:
            self.min += d

    def pop(self) -> None:
        d = self.deltas.pop()
        if d < 0:
            self.min -= d
        return self.min + d

    def top(self) -> int:
        return self.min + max(0, self.deltas[-1])

    def getMin(self) -> int:
        return self.min


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.solution = MinStack()

    def test_1(self):
        self.solution.push(-2)
        self.solution.push(3)
        self.assertEqual(self.solution.top(), 3)
        self.assertEqual(self.solution.getMin(), -2)
        self.assertEqual(self.solution.pop(), 3)
        self.assertEqual(self.solution.pop(), -2)
        self.solution.push(5)
        self.solution.push(-1)
        self.assertEqual(self.solution.top(), -1)
        self.assertEqual(self.solution.getMin(), -1)
