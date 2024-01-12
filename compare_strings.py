"""Compare Strings with Counts
"""

import unittest
from itertools import zip_longest


def expand(s):
    """Generates expanded string (None means "any char")"""
    for ch in s:
        if ch.isdigit():
            yield from [None] * int(ch)
        else:
            yield ch


def compare_strings_with_counts(a, b):
    """Compare Strings with Counts

    :param a: The first input string to compare.
    :param b: The second input string to compare.
    :return: True if the strings match with counts, False otherwise.

    This method compares whether the two strings can be made equal, taking into account the possible expansion
    of digits into arbitrary characters in each string.
    The comparison is performed by expanding the strings into a list of characters, possibly including None,
    which functions as a wildcard.

    Example usage:
        >>> compare_strings_with_counts("a1b", "aaa")
        False
    """
    return all(
        not ca or not cb or ca == cb
        for ca, cb in zip_longest(expand(a), expand(b), fillvalue="FAIL")
    )


class TestCompareStrings(unittest.TestCase):
    def test_compare_strings_with_counts(self):
        self.assertTrue(compare_strings_with_counts("apple", "apple"))
        self.assertFalse(compare_strings_with_counts("opple", "apple"))
        self.assertFalse(compare_strings_with_counts("apple", "applo"))
        self.assertTrue(compare_strings_with_counts("a2le", "a3e"))
        self.assertTrue(compare_strings_with_counts("4e", "4e"))
        self.assertFalse(compare_strings_with_counts("4e", "4o"))


if __name__ == "__main__":
    unittest.main()
