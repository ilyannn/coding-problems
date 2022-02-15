"""691. Stickers to Spell Word

Heuristics + search.

---
Runtime: 213 ms, faster than 92.46% of Python3 online submissions for Stickers to Spell Word.
Memory Usage: 15.3 MB, less than 28.82% of Python3 online submissions for Stickers to Spell Word.
"""

from collections import Counter
from functools import cache
from typing import List
import unittest


def subtract(a, b, n=1):
    return tuple(max(av - bv * n, 0) for av, bv in zip(a, b))


class Solution:
    def minStickers(self, stickers: List[str], target: str) -> int:
        def gen():
            sett = set(target)
            sets = {ch for s in stickers for ch in s}

            if sett - sets:
                return

            countt = Counter(target)
            listt = list(countt.items())

            def vector(c):
                return tuple(c[l] for l, _ in listt)

            countvs = {vector(Counter(s)) for s in stickers} - {(0,) * len(listt)}
            targetv = tuple(v for _, v in listt)

            in_words = [list() for _ in listt]
            for c in countvs:
                for i, v in enumerate(c):
                    if v:
                        in_words[i].append(c)

            for i, inw in enumerate(in_words):
                if len(inw) == 1:
                    yield (n := targetv[i])
                    targetv = subtract(targetv, inw[0], n)

            @cache
            def dfs(t):
                ix = next((i for i, v in enumerate(t) if v), None)
                if ix is None:
                    return 0
                return 1 + min(dfs(subtract(t, w)) for w in in_words[ix])

            yield dfs(targetv)

        return sum(gen()) or -1


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.f = Solution().minStickers

    def test_example(self):
        assert self.f(["with", "example", "science"], "thehat") == 3
        assert self.f(["notice", "possible"], "basicbasic") == -1

    def test_my(self):
        assert self.f(["bob", "bib"], "boy") == -1
        assert self.f(["bob", "bib"], "boi") == 2
        assert self.f(["bob", "bib"], "bobbibb") == 3
        assert self.f(["aeroplane", "meem", "highway", "destiny"], "yeet") == 2


if __name__ == "__main__":
    unittest.main()
