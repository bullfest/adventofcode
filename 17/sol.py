import sys
import q
from typing import List, Tuple
from dataclasses import dataclass
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
        print(l)
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

x_min, x_max, y_min, y_max = map(int, lines[0].split())


def test_trajectory(dx, dy):
    x, y = 0, 0
    maxi_y = 0
    while True:
        x += dx
        y += dy
        # print(x,y, dx, dy)
        if dx > 0:
            dx -= 1
        dy -= 1
        maxi_y = max(y, maxi_y)
        # print("maxis", x_min, x , x_max, y_min, y, y_max,
        #      x_min <= x <= x_max and y_max <= y <= y_min)
        if x_min <= x <= x_max and y_min <= y <= y_max:
            return maxi_y
        if y < y_min or x > x_max:
            return None


# assert 3 == test_trajectory(7,2)
# assert 6 == test_trajectory(6,3)
# assert 0 == test_trajectory(9,0)
# assert test_trajectory(17,-4) is None
# assert 45 == test_trajectory(6,9)

if len(sections) > 1:
    for l in sections[1]:
        for p in l.split():
            dx, dy = map(int, p.split(","))
            if (dx, dy) in [(7, -1)]:
                continue
            assert test_trajectory(dx, dy) is not None, f"{dx}, {dy} is None"
            print()

# 0 0
# 6 0
# 5 -1
# 9 -3
# 12 -6
# 14 -10


ans1 = 0
ans2 = 0

solutions = []
for dx in range(0, 150):
    for dy in range(-200, 200):
        if (ans := test_trajectory(dx, dy)) is not None:
            if dx == 0:
                print("???", dy)
            # print(dx,dy,ans)
            solutions.append((dx, dy))
            ans1 = max(ans1, ans)

ans2 = len(solutions)


print("1:", ans1)
print("2:", ans2)

# 3281
