import operator
import sys
from itertools import accumulate, islice, pairwise, tee


def sum_k(i, k: int):
    i1, i2 = tee(accumulate(i, initial=0))
    return map(operator.sub, islice(i2, k, None), i1)


it = pairwise(sum_k((int(line) for line in sys.stdin), 3))
print(sum(c < p for c, p in it))
