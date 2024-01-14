from typing import List

class Solution:
    def findWords(self, board: List[List[str]], words: List[str]) -> List[str]:
        m, n = len(board), len(board[0])
        B = n + 2

        def g_enumerate():
            """Encode board positions into small numbers"""
            for y, row in enumerate(board):
                for x, v in enumerate(row):
                    yield B * y + x, v

        def neighbors(p):
            """List of neighboring cells"""
            return (p + 1, p - 1, p + R, p - R)

        grid = defaultdict(lambda: None) | dict(g_enumerate())
        chars = set(grid.values())

        begins = defaultdict(set)
        for w in words:
            # Only keep words that are possible
            if not set(w).difference(chars):
                begins[w[0]].add(w)
        print(begins)

        def bfs():
            q = deque()
            for p, v in grid:
                for w in begins[v]:
                    q.push((p, 0, w))
            while q:
                p, i, w = q.popleft()
                for p1 in neighbors(p):
                    if w[i] == grid[p1]:
                        if i == len(w) - 1:
                            yield p1, w
                        else:
                            q.push((p1, i + 1, w))

        found = list(bfs())
        print(found)

        answer = set()

        def dfs(p, w, check=-1, seen=set()):
            if check == -len(w):
                answer.add(w)
            if w in answer:
                return  # Don't repeat ourselves
            seen.add(p)
            try:
                for p1 in neighbors(p):
                    if p not in seen and grid[p1] == w[check]:
                        dfs(p1, w, check - 1, seen)
            finally:
                seen.remove(p)

        for f in found:
            dfs(*f)

        return list(answer)
