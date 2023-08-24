import operator
import sys
from functools import reduce

commands = {
    "forward": lambda x: lambda p: (
        p[0],
        p[1] + x,
    ),  # increases the horizontal position by X units.
    "down": lambda x: lambda p: (p[0] + x, p[1]),  # increases the depth by X units.
    "up": lambda x: lambda p: (p[0] - x, p[1]),  # decreases the depth by X units.
}


def parse(it):
    for line in it:
        if line.strip():
            s = line.split()
            yield s[0], int(s[1])


def program():
    for w, x in parse(sys.stdin):
        yield commands[w](x)


final = reduce(lambda s, f: f(s), program(), (0, 0))
print(reduce(operator.mul, final, 1))
