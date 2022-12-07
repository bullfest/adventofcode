import sys
import q
import itertools as it
import math
import copy
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



if __name__ == "__main__":
    lines = [l.strip().split(",") for l in sys.stdin]
    visited = [dict(), dict()]
    
    for c in range(2):
        xp, yp = 0, 0
        steps = 0
        for instr in lines[c]:
            match [instr[0], int(instr[1:])]:
                case ['D', i]:
                    for y in range(yp+1,yp+i+1):
                        steps += 1
                        visited[c][(xp,y)] = steps
                    yp += i
                case ['R', i]:
                    for x in range(xp+1,xp+i+1):
                        steps += 1
                        visited[c][(x,yp)] = steps
                    xp += i
                case ['L', i]:
                    for x in range(xp-1,xp-i-1, -1):
                        steps += 1
                        visited[c][(x,yp)] = steps
                    xp -= i
                case ['U', i]:
                    for y in range(yp-1,yp-i-1, -1):
                        steps += 1
                        visited[c][(xp,y)] = steps
                    yp -= i
    pairs = visited[0].keys() & visited[1].keys()

    print([(p, visited[0][p], visited[1][p]) for p in pairs])
    ans1 = min(map(lambda p: abs(p[0])+abs(p[1]), pairs))
    ans2 = min(map(lambda p: visited[0][p]+visited[1][p], pairs))

    print("1:", ans1)
    print("2:", ans2)
