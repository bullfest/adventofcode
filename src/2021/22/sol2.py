import sys
import functools as ft
from typing import List, Tuple, Set
from dataclasses import dataclass


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
    sign: int

    @ft.cached_property
    def size(this):
        a = 1
        for i in range(3):
            a *= this.p1[i] - this.p0[i] + 1
        return a * this.sign

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

        return Cube(p0, p1, -c1.sign)


def from_op(op):
    x = op.x
    y = op.y
    z = op.z
    p0 = (x[0], y[0], z[0])
    p1 = (x[1], y[1], z[1])
    return Cube(p0, p1, 1 if op.op == "on" else -1)


cubes = set()

# Negacubes https://www.reddit.com/r/adventofcode/comments/rlxhmg/comment/hplbfaz/?utm_source=reddit&utm_medium=web2x&context=3
for op in inst:
    cube = from_op(op)
    for c in set(cubes):  # copy to iterate
        if o := c.overlap(cube):
            cubes.add(o)
    if op.op == "on":
        cubes.add(cube)

ans2 = 0
for c in cubes:
    ans2 += c.size

print("2:", ans2)
