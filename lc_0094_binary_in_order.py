""" 94. Binary Tree Inorder Traversal

Given the root of a binary tree, return the inorder traversal of its nodes' values.

---

Writing: 15 minutes
Debugging: 1 minute
Writing score: 😀

Runtime: 32 ms, faster than 66.33% of Python3 online submissions for Binary Tree Inorder Traversal.
Memory Usage: 14.4 MB, less than 14.09% of Python3 online submissions for Binary Tree Inorder Traversal.
"""

# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right

from typing import List, Optional


class Solution:
    def inorderTraversal(self, root: Optional[TreeNode]) -> List[int]:

        def take_left(node):
            while node:
                yield node
                node = node.left

        def gen():
            stack = list(take_left(root))  # Next node as well as its parents
            while stack:
                node = stack[-1]
                yield node.val
                if node.right:
                    stack.extend(take_left(node.right))
                else:
                    node = stack.pop()
                    while stack and stack[-1].right is node:
                        node = stack.pop()

        return list(gen())