from math import inf


def main(cities):
    def gen():
        stack = [(-inf, -1)]
        for i, v in enumerate(cities[::-1], -len(cities) + 1):
            while stack[-1][0] >= v:
                _ = stack.pop()
            yield stack[-1][1]
            stack.append((v, -i))

    return list(gen())[::-1]


if __name__ == "__main__":
    _ = input()
    print(*main([int(s) for s in input().split()]))
