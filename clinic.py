""" https://coderun.yandex.ru/problem/goblins-and-chess """


class Node:
    """Double-linked list node"""

    def __init__(self, value=None):
        self.value = value
        self.next = None
        self.prev = None

    def connect(self, next=None, prev=None):
        self.next = next
        self.prev = prev
        if next:
            next.prev = self
        if prev:
            prev.next = self

    def walk(self):
        node = self
        while node:
            yield str(node.value)
            node = node.next


class Pointer:
    """Pointer to the node together with its place in the queue"""

    def __init__(self, node: Node, index: int):
        self.node = node
        self.index = index

    def move(self, target: int):
        while target > self.index:
            self.node = self.node.next
            self.index += 1
        while target < self.index:
            self.node = self.node.prev
            self.index -= 1

    def correct(self, delta):
        self.index += delta

    def __str__(self):
        return f"[#{self.index}] " + "->".join(self.node.walk())


def main():
    """Solve the clinic problem with three pointers"""
    N = int(input())

    head = Pointer(Node(), 0)
    middle = Pointer(head.node, 0)
    tail = Pointer(Node(), 1)
    tail.node.connect(prev=head.node)

    # middle points to the center as defined by index len(tail) // 2
    # 0 elements: tail=1, middle=head=0
    # 1 element: tail=2, middle=1, head=0
    # 2 elements: tail=3, 2, middle=1, head=0
    # we always insert between tail and middle

    for _ in range(N):
        s = input()
        # print(head, middle, s, sep="  |  ")
        if s[0] == "-":
            del_node = head.node.next
            print(del_node.value)
            head.node.connect(next=del_node.next)
            if middle.index == 1:
                assert del_node == middle.node
                middle = Pointer(head.node.next, 1)
            else:
                assert del_node != middle.node
                middle.correct(-1)
            tail.correct(-1)
        else:
            new_node = Node(int(s.split()[1].strip()))
            if s[0] == "*":
                # insert after the middle
                new_node.connect(prev=middle.node, next=middle.node.next)
            else:
                assert s[0] == "+"
                # insert before the tail
                new_node.connect(prev=tail.node.prev, next=tail.node)
            tail.correct(+1)

        middle.move(tail.index // 2)


if __name__ == "__main__":
    main()
