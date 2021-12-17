import sys
import q
from collections import defaultdict


def transpose(m):
    return list(map(list, zip(*m)))


def get_sections(lines):
    sections = []
    section = []
    for l in lines:
        if l == "":
            if section != []:
                sections.append(section)
                section = []
        else:
            section.append(l)
    sections.append(section)
    return sections


def get_grid(lines, f=None, sep=None):
    f = f or (lambda x: x)
    return transpose([list(map(f, l if sep is None else l.split(sep))) for l in lines])


def print_grid(g):
    for l in transpose(g):
        print("".join(map(str, l)))
        # print("".join(map(lambda n: "X" if n > 10 else str(n % 10), l)))
    print()


def zero_index_points(points):
    return [(x - 1, y - 1) for x, y in points]


def points_to_grid(points, default_value=False, point_value=True):
    max_x = 0
    max_y = 0
    for x, y in points:
        max_x = max(x, max_x)
        max_y = max(y, max_y)

    grid = [[default_value] * (max_y + 1) for _ in range(max_x + 1)]
    for x, y in points:
        grid[x][y] = point_value
    return grid


def neighbours(x, y, diagonal=False):
    l = []
    if x > 0:
        l.append((x - 1, y))
        if y > 0 and diagonal:
            l.append((x - 1, y - 1))
        if y + 1 < max_y and diagonal:
            l.append((x - 1, y + 1))
    if y > 0:
        l.append((x, y - 1))

    if x + 1 < max_x:
        l.append((x + 1, y))
        if y > 0 and diagonal:
            l.append((x + 1, y - 1))
        if y + 1 < max_y and diagonal:
            l.append((x + 1, y + 1))
    if y + 1 < max_y:
        l.append((x, y + 1))
    return l


lines = [l.strip() for l in sys.stdin]
sections = get_sections(lines)

ans1 = 0
ans2 = 0

grid = get_grid(sections[0], int)
# big_grid = get_grid(sections[1], int)

x_h = len(grid)
y_h = len(grid[0])
new_grid = [[0] * len(grid[0]) * 5 for _ in range(len(grid) * 5)]


def next_v(n):
    n += 1
    n %= 10
    if n == 0:
        n = 1
    return n


for x in range(len(new_grid)):
    for y in range(len(new_grid[0])):
        if x - x_h < 0:
            if y - y_h < 0:
                new_grid[x][y] = grid[x][y]
            else:
                new_grid[x][y] = next_v(new_grid[x][y - y_h])
        else:
            new_grid[x][y] = next_v(new_grid[x - x_h][y])


dp = [[None] * len(grid[0]) * 5 for _ in range(len(grid) * 5)]

# print_grid(grid)
# print_grid(new_grid)
dp[-1][-1] = new_grid[-1][-1]

for _ in range(5):
    for x in reversed(range(len(dp))):
        for y in reversed(range(len(dp[0]))):
            s = None
            # g_val = grid[x%len(grid)][y%len(grid[0])] + (x // len(grid)) + (y // len(grid[0]))
            # if g_val > 10:
            #    g_val += 1
            # g_val %= 10
            # if g_val == 0:
            #    g_val = 1
            # print(x,y,g_val)
            g_val = new_grid[x][y]

            if x + 1 < len(dp):
                s = dp[x + 1][y] + g_val
            if y + 1 < len(dp[0]):
                if s is None:
                    s = dp[x][y + 1] + g_val
                else:
                    s = min(s, dp[x][y + 1] + g_val)
            if x - 1 > 0:
                if dp[x - 1][y] is not None:
                    if s is None:
                        s = dp[x - 1][y] + g_val
                    else:
                        s = min(s, dp[x - 1][y] + g_val)
            if y - 1 > 0:
                if dp[x][y - 1] is not None:
                    if s is None:
                        s = dp[x][y - 1] + g_val
                    else:
                        s = min(s, dp[x][y - 1] + g_val)

            if s is not None:
                dp[x][y] = s

ans1 = min(dp[0][1], dp[1][0])

assert next_v(1) == 2
assert next_v(2) == 3
assert next_v(3) == 4
assert next_v(4) == 5
assert next_v(5) == 6
assert next_v(6) == 7
assert next_v(7) == 8
assert next_v(8) == 9
assert next_v(9) == 1


print("1:", ans1)
print("2:", ans2)
