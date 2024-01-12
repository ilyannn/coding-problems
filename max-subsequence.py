from functools import cache


def max_subsequence(seqN, seqM):
    @cache
    def answer(i, j):
        if not i or not j:
            return 0, ()

        if (v := seqN[i - 1]) == seqM[j - 1]:
            blen, bpath = answer(i - 1, j - 1)
            return blen + 1, (bpath, v)

        return max(answer(i - 1, j), answer(i, j - 1))

    def gen_path(path):
        while path:
            path, head = path
            yield head

    return reversed(list(gen_path(answer(len(seqN), len(seqM))[1])))


def main():
    (n,), seqN, (m,), seqM = ([int(v) for v in input().split()] for _ in range(4))
    assert n == len(seqN)
    assert m == len(seqM)

    print(*max_subsequence(seqN, seqM))


if __name__ == "__main__":
    main()
