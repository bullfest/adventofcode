import sys
import q
import itertools as it
import math
import aocd
from typing import List, Tuple
from dataclasses import dataclass
from collections import defaultdict


def priority(c):
    i = ord(c)
    if "a" <= c <= "z":
        return i - ord("a") + 1
    else:
        return i - ord("A") + 27


filename = sys.argv[1]
with open(filename) as f:
    lines = [l.strip() for l in f]
ans1 = 0

for l in lines:
    part1 = l[: len(l) // 2]
    part2 = l[len(l) // 2 :]
    # print(part1, part2)
    for c in set(part1) & set(part2):
        ans1 += priority(c)

ans2 = 0

for i in range((len(lines) + 1) // 3):
    l1 = lines[3 * i]
    l2 = lines[3 * i + 1]
    l3 = lines[3 * i + 2]
    for c in set(l1) & set(l2) & set(l3):
        ans2 += priority(c)


print("1:", ans1)
print("2:", ans2)

if filename == "input":
    submit = input("submit?")
    if "y" in submit.lower():
        if ans1 != 0:
            aocd.submit(ans1, part="a")
        if ans2 != 0:
            aocd.submit(ans2, part="b")
