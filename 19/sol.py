import sys
import q
import itertools as it
import math
from typing import List, Tuple, Set
import dataclasses
from dataclasses import dataclass
from collections import defaultdict


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



@dataclass
class Scanner:
    n: int
    pos: Tuple[int,int,int] = None
    beacons: Set[Tuple[int,int, int]] = dataclasses.field(default_factory=set)
    abs_beacons = None

lines = [l.strip() for l in sys.stdin]
sections = get_sections(lines)
scanners = []
for s in sections:
    scanners.append(Scanner(len(scanners)))
    for b in s[1:]:
        scanners[-1].beacons.add(tuple(map(int, b.split(","))))
scanners[0].pos = (0,0,0)
scanners[0].abs_beacons = scanners[0].beacons

orientations = [
    {
        0: a,
        1: b,
        2: c,
    }
    for a,b,c in it.permutations(it.product(("+", "-"), (0,1,2)), 3)
    if a[1] not in [b[1], c[1]] and b[1] != c[1]
]

def reorient(b, o):
    p = [0,0,0]
    if o[0][0] == "+":
        p[0] += b[o[0][1]]
    if o[0][0] == "-":
        p[0] -= b[o[0][1]]

    if o[1][0] == "+":
        p[1] += b[o[1][1]]
    if o[1][0] == "-":
        p[1] -= b[o[1][1]]

    if o[2][0] == "+":
        p[2] += b[o[2][1]]
    if o[2][0] == "-":
        p[2] -= b[o[2][1]]
    return tuple(p)

def try_pos(gs, ts, pos, o):
    """Assume that ts is in pos, how many matches do we find?"""
    g_beacons = set(tuple(gs.pos[i]+b[i] for i in range(3)) for b in gs.beacons)
    beacons = set()
    for b in ts.beacons:
        beacons.add(reorient(b,o))
    t_beacons = set(tuple(pos[i]+b[i] for i in range(3)) for b in beacons)
    if len(t_beacons & g_beacons) >= 12:
        ts.pos = pos
        ts.beacons = beacons
        ts.abs_beacons = t_beacons
        return True
    return False

def find_pos(gs, ts):
    assert gs.pos is not None
    for bg, bt in it.product(gs.abs_beacons, ts.beacons):
        for o in orientations:
            b = reorient(bt, o)
            pos = tuple(bg[i] - b[i] for i in range(3)) 
            if try_pos(gs, ts, pos, o):
                return True
    return False

known_s = scanners[:1]
unknown_s = scanners[1:]
for ks in known_s:
    print("Next known", len(unknown_s))
    i = 0
    while i < len(unknown_s):
        us = unknown_s[i]
        if find_pos(ks, us):
            known_s.append(us)
            unknown_s.remove(us)
            print("Removed", len(unknown_s))
        else:
            i += 1

all_beacons = set()
for s in scanners:
    all_beacons |= s.abs_beacons

ans1 = len(all_beacons)

def manhattan(s1, s2):
    return sum(abs(s1.pos[i]-s2.pos[i]) for i in range(3))
ans2 = 0
for s1, s2 in it.combinations(scanners, 2):
    ans2 = max(ans2, manhattan(s1,s2))

for s in scanners:
    print(s.n, s.pos)

print("1:", ans1)
print("2:", ans2)
