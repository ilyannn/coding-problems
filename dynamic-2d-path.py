from functools import cache
from typing import Tuple


def main():
    n, m = (int(v) for v in input().split())
    table = [[int(v) for v in input().split()] for _ in range(n)]
    assert all(len(row) == m for row in table)

    def neighbors(x, y):
        if y < n:
            yield "D", (x, y + 1)
        if x < m:
            yield "R", (x + 1, y)

    def value_at(x, y):
        return table[y - 1][x - 1]

    initial = 1, 1
    final = m, n

    @cache
    def answer(p) -> Tuple[int, list]:
        def choices():
            #  Ascend
            if p == final:
                yield value_at(*p), []

            #  Go D or R
            for dir, np in neighbors(*p):
                pvalue, path = answer(np)
                yield value_at(*p) + pvalue, (dir, path)

        return max(choices())

    def gen_path(path):
        while path:
            dir, path = path
            yield dir

    best_value, best_path = answer(initial)

    print(best_value)
    print(*gen_path(best_path))


if __name__ == "__main__":
    main()
