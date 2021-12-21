import sys
import q
import itertools as it
import math
from typing import List, Tuple
from dataclasses import dataclass
from collections import defaultdict


lines = [l.strip().split() for l in sys.stdin]
i_p1 = int(lines[0][-1])
i_p2 = int(lines[1][-1])
p1 = i_p1
p2 = i_p2
dice = 0
s1 = 0
s2 = 0

t1 = True
while s1 < 1000 and s2 < 1000:
    if t1:
        for _ in range(3):
            dice += 1
            roll = (dice % 100)
            if roll == 0: roll = 100
            p1 += roll
        p1 %= 10
        if p1 == 0:
            p1 = 10
        s1 += p1
    else:
        for _ in range(3):
            dice += 1
            roll = (dice % 100)
            if roll == 0: roll = 100
            p2 += roll
        p2 %= 10
        if p2 == 0:
            p2 = 10
        s2 += p2
    t1 = not t1


ans1 = min(s1, s2)*dice

# Part 2
s = defaultdict(lambda: 0)
# turn, s1, s2, p1, p2
s[(0,0,0,i_p1,i_p2)] = 1
w1 = 0
w2 = 0

while s:
    k = next(iter(s))
    v = s[k]
    del s[k]
    t, s1, s2, p1, p2 = k
    if t % 2 == 0:
        for dice in it.product([1,2,3],repeat=3):
            p1p = p1 + sum(dice)
            p1p %= 10
            if p1p == 0:
                p1p = 10
            if s1 + p1p >= 21:
                w1 += v
            else:
                s[(t+1,s1+p1p,s2,p1p,p2)] += v
    else:
        for dice in it.product([1,2,3],repeat=3):
            p2p = p2 + sum(dice)
            p2p %= 10
            if p2p == 0:
                p2p = 10
            if s2 + p2p >= 21:
                w2 += v
            else:
                s[(t+1,s1,s2+p2p,p1,p2p)] += v


ans2 = max(w1,w2)

print("1:", ans1)
print("2:", ans2)
