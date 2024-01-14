from functools import cache


def main():
    n, m = (int(v) for v in input().split())
    table = [[int(v) for v in input().split()] for _ in range(n)]
    assert len(table) == n and all(len(row) == m for row in table)

    def neighbours(x, y):
        yield x - 1, y
        yield x, y - 1

    @cache
    def answer(x, y):
        if x == 0 and y == 1:
            return 0
        if not (1 <= x <= m and 1 <= y <= n):
            return float("inf")
        return table[y - 1][x - 1] + min(answer(*n) for n in neighbours(x, y))

    print(answer(m, n))


if __name__ == "__main__":
    main()
