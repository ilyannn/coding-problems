"""212. Word Search II

https://leetcode.com/problems/word-search-ii/

---

Submitted three times:
> Runtime: 40 ms, faster than 99.95% of Python3 online submissions for Word Search II.
> Runtime: 44 ms, faster than 99.86% of Python3 online submissions for Word Search II.
> Runtime: 44 ms, faster than 99.86% of Python3 online submissions for Word Search II.
> Memory Usage: 15.1 MB, less than 96.19% of Python3 online submissions for Word Search II.

We use two heuristics before the actual DFS. Overall there are following steps:

1. Only consider the words that can be composed using this multiset of letters.
2. Perform a naive BFS first to solve a simpler problem where the letters can be reused.
3. Check that the solution works for our problem by the DFS from the end of the word.

As additional optimizations we use the following tricks:

1. Board positions are saved as small integers.
2. The BFS is performed by iteratively walking a trie.
"""

from collections import Counter, defaultdict
from functools import cache
from itertools import chain
from typing import List
from unittest import TestCase, main


class Trie:
    def __init__(self, parent=None):
        def trie_factory():
            return defaultdict(lambda: Trie(parent=self))

        self.parent = parent
        self.root = trie_factory()
        self.empty_value = None

    def subtrie(self, ch, create=False):
        return self.root[ch] if ch in self.root or create else None

    def findtrie(self, prefix, create=False):
        trie = self
        for c in prefix:
            trie = trie.subtrie(c, create)
            if trie is None:
                break
        return trie

    def add(self, word, value=None):
        self.findtrie(word, create=True).empty_value = word if value is None else value

    def query(self, word):
        trie = self.findtrie(word)
        return trie and trie.empty_value

    def items(self):
        return (
            self.root.items()
            if self.empty_value is None
            else chain((("", self.empty_value),), self.root.items())
        )

    def __str__(self):
        parts = [f"{ch}: {str(subtrie)}" for ch, subtrie in self.root.items()]
        if self.empty_value is not None:
            parts = [self.empty_value] + parts
        return "<" + ", ".join(parts) + ">"

    def __len__(self):
        return (self.empty_value is not None) + sum(
            len(sub) for sub in self.root.values()
        )

    def __bool__(self):
        return len(self) != 0


def group_by_value(it, into=set, op=set.add):
    answer = defaultdict(into)
    for k, v in it:
        op(answer[v], k)  # PyCharm is not smart enough and displays a warning here.
    return answer


# noinspection PyMethodMayBeStatic
class Solution:
    def findWords(self, board: List[List[str]], words: List[str]) -> List[str]:
        m, n = len(board), len(board[0])
        B = max(64, n + 2)

        def g_enumerate():
            """Encode board positions into small numbers"""
            for y, row in enumerate(board):
                for x, val in enumerate(row):
                    yield B * y + x, val

        @cache
        def neighbors(p):
            """List of neighboring cells"""
            return p + 1, p - 1, p + B, p - B

        grid = dict(g_enumerate())
        grid_by_ch = group_by_value(grid.items())

        word_trie = Trie()
        for w in words:
            # Only keep words that are possible
            if len(w) <= m * n and all(
                v <= len(grid_by_ch[ch]) for ch, v in Counter(w).items()
            ):
                word_trie.add(w, w)

        def naive_bfs(trie=word_trie, cur=None):
            cur_n = {q for p in cur for q in neighbors(p)} if cur else set(grid)

            for ch, value in trie.items():
                if not ch:
                    yield cur, value
                elif next_ := cur_n & grid_by_ch[ch]:
                    yield from naive_bfs(value, next_)

        def check_word(choices, word):
            def dfs(p, pos, taken):
                return any(
                    not pos or dfs(q, pos - 1, taken | {p})
                    for q in grid_by_ch[word[pos]].intersection(neighbors(p)) - taken
                )

            return any(dfs(p, len(word) - 2, set()) for p in choices)

        #        for choices, word in naive_bfs():
        #            print(choices, word, check_word(choices, word))

        return [
            word
            for choices, word in naive_bfs()
            if len(word) == 1 or check_word(choices, word)
        ]


# noinspection PyMethodMayBeStatic
class AuxiliaryTestCase(TestCase):
    def test_trie(self):
        t = Trie()
        assert not t
        assert not t.findtrie("wo", create=False)
        t.add("wow", "wow")
        t.add("won", "won")
        assert t
        assert len(t) == 2
        assert len(t.findtrie("wo", create=False)) == 2
        assert len(t.findtrie("won", create=False)) == 1
        assert t.query("won") == "won"
        assert t.query("wow") == "wow"
        assert not t.query("wo") and not t.query("wont")
        assert [("w", t.findtrie("w"))] == list(t.items())
        assert [("", "won")] == list(t.findtrie("won").items())

    def test_group(self):
        assert group_by_value([("a", 1), ("b", 2), ("c", 1)]) == {
            1: {"a", "c"},
            2: {"b"},
        }


class SolutionTestCase(TestCase):
    def setUp(self) -> None:
        self.f = Solution().findWords

    def test_simple(self):
        """Check some simple cases"""
        assert self.f([["X"]], ["X"]) == ["X"]
        assert self.f([["X"]], ["Y"]) == []

    def test_examples(self):
        """From the problem description"""
        assert set(
            self.f(
                [
                    ["o", "a", "a", "n"],
                    ["e", "t", "a", "e"],
                    ["i", "h", "k", "r"],
                    ["i", "f", "l", "v"],
                ],
                words=["oath", "pea", "eat", "rain"],
            )
        ) == {"eat", "oath"}

        assert self.f([["a", "b"], ["c", "d"]], words=["abcb"]) == []

    def test_crosses(self):
        """Here the word can only be found on board if we take the letter 'a' twice."""
        assert (
            self.f(
                [
                    ["o", "b", "a", "n"],
                    ["e", "t", "a", "e"],
                    ["i", "h", "k", "r"],
                    ["i", "f", "l", "v"],
                ],
                words=["kata"],
            )
            == []
        )


if __name__ == "__main__":
    main()
