import sys
import q
import itertools as it
import functools as ft
import math
from typing import List, Tuple, Set
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
inst = []


@dataclass
class Op:
    op: str
    x: Tuple[int, int]
    y: Tuple[int, int]
    z: Tuple[int, int]

    def coords(this):
        return (this.x, this.y, this.z)

    def outside(this):
        for c in this.coords():
            if (not -50 <= c[0] <= 50) or (not -50 <= c[1] <= 50):
                return True
        return False

    def xrange(this):
        return range(this.x[0] + 50, this.x[1] + 51)

    def yrange(this):
        return range(this.y[0] + 50, this.y[1] + 51)

    def zrange(this):
        return range(this.z[0] + 50, this.z[1] + 51)


for l in lines:
    op, arg = l.split()
    x, y, z = map(lambda s: s.split("=")[1], arg.split(","))
    x = tuple(map(int, x.split("..")))
    y = tuple(map(int, y.split("..")))
    z = tuple(map(int, z.split("..")))
    inst.append(Op(op, x, y, z))

cubs = [[[False] * 101 for _ in range(101)] for _ in range(101)]

for i in inst:
    if i.outside():
        continue
    for x in i.xrange():
        for y in i.yrange():
            for z in i.zrange():
                if i.op == "on":
                    cubs[x][y][z] = True
                else:
                    cubs[x][y][z] = False


ans1 = 0
for x in cubs:
    for y in x:
        for cub in y:
            if cub:
                ans1 += 1
print("1:", ans1)


@dataclass(frozen=True)
class Cube:
    p0: Tuple[int, int, int]
    p1: Tuple[int, int, int]

    @ft.cached_property
    def size(this):
        a = 1
        for i in range(3):
            a *= this.p1[i] - this.p0[i] + 1
        return a

    @property
    def x(this):
        x0 = this.p0[0]
        x1 = this.p1[0]
        return (x0, x1)

    @property
    def y(this):
        y0 = this.p0[1]
        y1 = this.p1[1]
        return (y0, y1)

    @property
    def z(this):
        z0 = this.p0[2]
        z1 = this.p1[2]
        return (z0, z1)

    def overlap(c1, c2):
        if any(c1.p0[i] > c2.p1[i] or c1.p1[i] < c2.p0[i] for i in range(3)):
            return None
        p0 = tuple(max(c1.p0[i], c2.p0[i]) for i in range(3))
        p1 = tuple(min(c1.p1[i], c2.p1[i]) for i in range(3))

        return Cube(p0, p1)

    def subtract(c1, c2):
        o = c1.overlap(c2)
        if not o:
            return False
        cubes = set()
        cubes.add(from_coords(c1.x, c1.y, (c1.z[0], o.z[0] - 1)))
        cubes.add(from_coords(c1.x, c1.y, (o.z[1] + 1, c1.z[1])))
        cubes.add(from_coords((c1.x[0], o.x[0] - 1), c1.y, o.z))
        cubes.add(from_coords((o.x[1] + 1, c1.x[1]), c1.y, o.z))
        cubes.add(from_coords(o.x, (c1.y[0], o.y[0] - 1), o.z))
        cubes.add(from_coords(o.x, (o.y[1] + 1, c1.y[1]), o.z))
        return (
            cubes  # set(c for c in cubes if all(c.p0[i] <= c.p1[i] for i in range(3)))
        )


def from_coords(x, y, z):
    p0 = (x[0], y[0], z[0])
    p1 = (x[1], y[1], z[1])
    return Cube(p0, p1)


def from_op(op):
    x = op.x
    y = op.y
    z = op.z
    p0 = (x[0], y[0], z[0])
    p1 = (x[1], y[1], z[1])
    return Cube(p0, p1)


cubes = set()


for op in inst:
    cube = from_op(op)
    new_cubes = set()
    for c in cubes:
        if s := c.subtract(cube):
            new_cubes |= s
        else:
            new_cubes.add(c)
    if op.op == "on":
        new_cubes.add(cube)
    cubes = new_cubes

ans2 = 0
for c in cubes:
    ans2 += c.size

print("2:", ans2)
