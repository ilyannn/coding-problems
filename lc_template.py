import bisect
from itertools import *
from string import *
from collections import *
import unittest


# noinspection PyMethodMayBeStatic
class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def test_passing(self):
        assert 2 + 2 == 4

    def test_failing1(self):
#        assert 2 + 2 == 5
        pass
    
    def test_failing2(self):
#        assert 2 + 2 == 5
        pass

if __name__ == "__main__":
    unittest.main()
