"""460. LFU Cache

https://leetcode.com/problems/lfu-cache/

---

Runtime: 1680 ms, faster than 9.98% of Python3 online submissions for LFU Cache.
Memory Usage: 77.7 MB, less than 98.42% of Python3 online submissions for LFU Cache.
"""

from collections import defaultdict
import unittest


def debug(*_):
    pass


class Node:
    def __init__(self, key=None):
        self.key = key
        self.freq = 0
        self.bind_self()

    def bind_self(self):
        self.prev_ = self
        self.next_ = self

    def __repr__(self):
        return f"<{self.key}: {self.value} ({self.freq})>"


class LinkedList:
    def __init__(self):
        self.root = Node()
        self.length = 0

    def append(self, node):
        self.length += 1
        p = self.root.prev_
        p.next_ = node
        self.root.prev_ = node
        node.next_ = self.root
        node.prev_ = p

    def popleft(self) -> Node:
        self.length -= 1
        n = self.root.next_
        self.root.next_ = n.next_
        n.next_.prev_ = self.root
        n.bind_self()
        return n

    def pop(self, node):
        self.length -= 1
        node.next_.prev_, node.prev_.next_ = node.prev_, node.next_
        node.next_ = node.prev_ = node

    def __len__(self):
        return self.length

    def __bool__(self):
        return len(self) != 0

    def walk(self):
        node = self.root.next_
        while node != self.root:
            yield node
            node = node.next_

    def __repr__(self):
        return str(list(self.walk()))


class Levels:
    def __init__(self, factory):
        self.data = defaultdict(factory)
        self._min_level = 0

    def get(self, level):
        self._min_level = min(self._min_level, level)
        return self.data[level]

    def get_min(self):
        while not (l := self.data[self._min_level]):
            self._min_level += 1
        return l

    def __str__(self):
        d = sorted((i, l) for i, l in self.data.items() if l)
        return str({i: l for i, l in d})


class LFUCache:
    def __init__(self, capacity: int):
        self.use = Levels(LinkedList)
        self.nodes = {}
        self.capacity = capacity
        self.min_use = 0

    def _fetch(self, key):
        node = self.nodes.get(key, None)
        if node:
            self.use.get(node.freq).pop(node)
        return node

    def _emplace(self, node):
        node.freq += 1
        self.use.get(node.freq).append(node)

    def _reuse_node(self):
        assert self.capacity > 0
        if len(self.nodes) > self.capacity - 1:
            node = self.use.get_min().popleft()
            assert self.nodes[node.key] is node
            del self.nodes[node.key]
            return node

    def get(self, key: int) -> int:
        if not (node := self._fetch(key)):
            debug(f"get {key} (missing)")
            return -1
        try:
            return node.value
        finally:
            self._emplace(node)
            debug(f"get {key} →", len(self.nodes), self.use)

    def put(self, key: int, value: int) -> None:
        if not self.capacity:
            return
        if not (node := self._fetch(key)):
            if node := self._reuse_node():
                node.freq = 0
                node.key = key
            else:
                node = Node(key)
            self.nodes[key] = node
        node.value = value
        self._emplace(node)
        debug(f"put {key} →", len(self.nodes), self.use)


class MyTestCase(unittest.TestCase):
    def test_example(self):
        """Example from the problem description.
        ["LFUCache", "put", "put", "get", "put", "get", "get", "put", "get", "get", "get"]
        [[2], [1, 1], [2, 2], [1], [3, 3], [2], [3], [4, 4], [1], [3], [4]]
        Output
        [null, null, null, 1, null, -1, 3, null, -1, 3, 4]
        """
        c = LFUCache(2)
        c.put(1, 1)
        c.put(2, 2)
        assert c.get(1) == 1
        c.put(3, 3)
        assert c.get(2) == -1
        assert c.get(3) == 3
        c.put(4, 4)
        assert c.get(1) == -1
        assert c.get(3) == 3
        assert c.get(4) == 4

    def test_empty(self):
        """That's an actual test from the test suite"""
        c = LFUCache(0)
        c.put(1, 1)
        assert c.get(1) == -1


if __name__ == "__main__":
    unittest.main()
