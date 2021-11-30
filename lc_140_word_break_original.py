"""140. Word Break II

Given a string s and a dictionary of strings wordDict, add spaces in s to construct a sentence where each word is a valid dictionary word. Return all such possible sentences in any order.

Note that the same word in the dictionary may be reused multiple times in the segmentation.

---

Writing: 30 minutes
Debugging: 5 minutes
Writing score: 😕😕😕😕😕😕😢🤬🤬

Runtime: 32 ms, faster than 65.92% of Python3 online submissions for Word Break II.
Memory Usage: 14.7 MB, less than 9.42% of Python3 online submissions for Word Break II.
"""

from collections import defaultdict
from functools import lru_cache
# 😕 The order of imports was not alphabetic
from typing import List

memoize = lru_cache(None)


# 😕 This should have been two empty lines according to PEP 8
def factory():
    return defaultdict(factory)


# 😕 This should have been two empty lines according to PEP 8
class Trie:
    def __init__(self, word_list=None):
        self.data = factory()
        if word_list:
            for w in word_list:
                self.add(w)

    def find_prefix(self, prefix, create=False):
        d = self.data
        for c in prefix:
            if c in d or create:
                d = d[c]
            else:
                return None
        return d

    def add(self, word):
        self.find_prefix(word, create=True)[None] = True

    def __contains__(self, word):
        if not isinstance(word, str):
            return False
        d = self.find_prefix(word)
        return (None in d) if d else False

    def has_prefix(self, prefix):
        return self.find_prefix(prefix) is not None

    def walk(self, s, from_index):
        """Yields all values of index for which s[from_index:index] is in the trie"""
        d = self.data
        for i in range(from_index, len(s)):
            if None in d:
                yield i
            c = s[i]
            if c not in d:
                return
            d = d[c]
        if None in d:
            yield len(s)


t = Trie(["ab", "abc"])
t.add("abba")
assert "ab" in t
assert "abba" in t
assert "a" not in t
assert t.has_prefix("a")
assert t.has_prefix("abba")
assert list(t.walk("jabba", 1)) == [3, 5]


# 😕 This should have been two empty lines according to PEP 8
# 😢 The function + assertion together had an off-by-one bug
def add_spaces(s, a):
    # ✅ This is fine -- I've decided to change the precondition
    assert a[-1] == len(s)
    return " ".join(s[p:c] for c, p in zip(a, [0] + a))


# 😕 This should have been two empty lines according to PEP 8
assert add_spaces("catsanddogs", [4, 7, 11]) == "cats and dogs"


class Solution:
    def wordBreak(self, s: str, wordDict: List[str]) -> List[str]:
        words = Trie(wordDict)

        @memoize
        def answer(from_ix):
            if from_ix == len(s):
                # 🤬 This was a bug, we meant "there is one choice"
                return [[]]

            # 😕 This should have been an empty line
            def gen():
                for ix in words.walk(s, from_ix):
                    for right in answer(ix):
                        yield [ix] + right
            return list(gen())

        # 🤬 This was a bug, the line as written made no sense
        return [add_spaces(s, a) for a in answer(0)]
