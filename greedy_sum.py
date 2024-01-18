from heapq import heapify, heappop, heappush


def main(numbers):
    def gen():
        heap = numbers.copy()
        heapify(heap)
        while len(heap) > 1:
            total = heappop(heap) + heappop(heap)
            yield total
            heappush(heap, total)

    return f"{sum(gen())/20:.2f}"


if __name__ == "__main__":
    _ = input()
    print(main([int(s) for s in input().split()]))
