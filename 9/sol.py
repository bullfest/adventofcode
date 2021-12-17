import sys
from collections import defaultdict

lines = [l.strip() for l in sys.stdin]
grid = [list(map(int, l)) for l in lines]

bn = [[0] * len(grid[x]) for x in range(len(grid))]

ans1 = 0
for p in range(10):
    for x in range(len(grid)):
        for y in range(len(grid[x])):
            pairs = set()
            if x > 0:
                pairs.add((x - 1, y))
            if x + 1 < len(grid):
                pairs.add((x + 1, y))
            if y > 0:
                pairs.add((x, y - 1))
            if y + 1 < len(grid[x]):
                pairs.add((x, y + 1))
            if p == 0 and all(grid[x][y] < grid[px][py] for px, py in pairs):
                ans1 += grid[x][y] + 1
bs = []
next_i = 1
for x in range(len(grid)):
    for y in range(len(grid[x])):
        if bn[x][y] > 0 or grid[x][y] == 9:
            continue
        dfs = [(x, y)]
        c = 0
        # print("starting dfs",x,y)
        while len(dfs) > 0:
            # print(dfs)
            px, py = dfs.pop()
            # print(px,py, bn[px][py])
            if bn[px][py] > 0:
                continue
            pairs = set()
            if px > 0:
                pairs.add((px - 1, py))
            if px + 1 < len(grid):
                pairs.add((px + 1, py))
            if py > 0:
                pairs.add((px, py - 1))
            if py + 1 < len(grid[px]):
                pairs.add((px, py + 1))
            n = 0
            for ppx, ppy in pairs:
                if bn[ppx][ppy] > 0:
                    if n not in [0, bn[ppx][ppy]]:
                        print("WOT")
                    n = bn[ppx][ppy]
                else:
                    if grid[ppx][ppy] < 9:
                        dfs.append((ppx, ppy))
            c += 1
            if n == 0:
                n = next_i
                next_i += 1
            bn[px][py] = n
        bs.append(c)


print("ans1:", ans1)

for x in range(len(grid)):
    pass
    print("".join(map(lambda x: "▪" if x == 0 else " ", bn[x])))

bs.sort()
ans2 = bs[-1] * bs[-2] * bs[-3]
print("ans2:", ans2)
