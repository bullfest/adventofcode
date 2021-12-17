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
        print("".join(l))
    print()


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
points_coords = [list(map(int, l.split(","))) for l in sections[0]]
folds = []
for l in sections[1]:
    _, _, info = l.split()
    axis, value = info.split("=")
    value = int(value)
    folds.append((axis, value))


def fold(axis, value, points):
    new_points = set()
    for x, y in points:
        if axis == "x":
            if x < value:
                new_points.add((x, y))
            else:
                new_points.add((2 * value - x, y))
        else:
            if y < value:
                new_points.add((x, y))
            else:
                new_points.add((x, 2 * value - y))
    return new_points


points = fold(folds[0][0], folds[0][1], points_coords)
print("1:", len(points))

ans1 = 0
for axis, value in folds[1:]:
    points = fold(axis, value, points)

max_x = 0
max_y = 0
for x, y in points:
    max_x = max(max_x, x)
    max_y = max(max_y, y)

max_x += 1
max_y += 1

m = [["."] * max_y for _ in range(max_x)]

for x, y in points:
    m[x][y] = "#"

print_grid(m)
