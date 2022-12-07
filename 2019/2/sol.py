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

def run_program(prog):
    prog = copy.deepcopy(prog)
    i = 0
    while i < len(prog):
        v = prog[i]
        match v:
            case 1:
                v1 = prog[prog[i+1]]
                v2 = prog[prog[i+2]]
                prog[prog[i+3]] = v1 + v2
                i += 4
            case 2:
                v1 = prog[prog[i+1]]
                v2 = prog[prog[i+2]]
                prog[prog[i+3]] = v1 * v2
                i += 4
            case 99:
                break
    return prog

def test_run():
    assert run_program([]) == []
    assert run_program([1,9,10,3,2,3,11,0,99,30,40,50]) == [3500,9,10,70,2,3,11,0,99,30,40,50]
    assert run_program([1,0,0,0,99]) == [2,0,0,0,99]
    assert run_program([2,3,0,3,99]) == [2,3,0,6,99]
    assert run_program([2,4,4,5,99,0]) == [2,4,4,5,99,9801]
    assert run_program([1,1,1,4,99,5,6,0,99]) == [30,1,1,4,2,5,6,0,99]

if __name__ == "__main__":
    lines = [l.strip() for l in sys.stdin]
    prog = list(map(int, lines[0].split(",")))
    prog[1] = 12
    prog[2] = 2
    ans1 = run_program(prog)[0]
    for n in range(100):
        for v in range(100):
            prog[1] = n
            prog[2] = v
            res = run_program(prog)[0]
            if res == 19690720:
                ans2 = n*100 + v
                break
        else:
            continue
        break

    print("1:", ans1)
    print("2:", ans2)
