import sys
from itertools import pairwise

it = pairwise(int(line) for line in sys.stdin)
print(sum(c < p for c, p in it))
