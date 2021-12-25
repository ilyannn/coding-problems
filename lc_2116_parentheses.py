"""2116. Check if a Parentheses String Can Be Valid

https://leetcode.com/problems/check-if-a-parentheses-string-can-be-valid/
"""

import unittest


class Solution:
    def canBeValid(self, s: str, locked: str) -> bool:
        """Find out if the string can be made into a valid one.

        At each step of the algorithm, the range(minl, maxl + 1, 2])
        contains exactly the possible open bracket levels of valid strings
        across all possible arrangements of parentheses in s[:i].

        In other words, the values of L for which s[:i] + ')' * L is valid
        are exactly the values from minl to maxl inclusive (of correct parity).
        """
        minl, maxl = 0, 0
        for ch, lock in zip(s, locked):
            if lock == "0":
                #  Two possible choices – minl goes down, maxl goes up.
                minl += -1 if minl else 1  # Except we can't go lower than 0.
                maxl += 1
            elif ch == "(":
                #  Only one choice - shift our interval up.
                minl += 1
                maxl += 1
            elif maxl:  # ch == ")"
                #  Only one choice - shift our interval down.
                minl += -1 if minl else 1
                maxl -= 1
            else:
                #  Our interval became empty – no possible choices.
                return False

        #  Per invariant above we know some strings of the form s + ')' * L are
        #  valid, we just need to check that 0 is a valid value for L.
        return not minl


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.f = Solution().canBeValid

    def test_locked(self):
        assert self.f("(()())", "111111")
        assert not self.f("())())", "111111")

    def test_empty(self):
        assert self.f("", "")

    def test_unlocked(self):
        assert not self.f("())())", "011111")
        assert self.f("())())", "101111")
        assert not self.f("())())", "111000")
        assert self.f("())())", "101101")

    def text_examples(self):
        assert self.f("))()))", "010100")
        assert self.f("()()", "0000")
        assert not self.f(")", "0")


if __name__ == "__main__":
    unittest.main()