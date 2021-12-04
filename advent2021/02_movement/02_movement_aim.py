import operator
import sys
from functools import reduce

commands = {
    "forward": lambda x: lambda p: (p[0] + p[2] * x, p[1] + x, p[2]),
    "down": lambda x: lambda p: (p[0], p[1], p[2] + x),
    "up": lambda x: lambda p: (p[0], p[1], p[2] - x)
}


def parse(it):
    for line in it:
        if line.strip():
            s = line.split()
            yield s[0], int(s[1])


def program():
    for w, x in parse(sys.stdin):
        yield commands[w](x)


final = reduce(lambda s, f: f(s), program(), (0, 0, 0))
print(final[0] * final[1])
