import sys
from collections import defaultdict

lines = [l.strip() for l in sys.stdin]
ans1 = 0
ans2scores = []
points = {")": 3, "]": 57, "}": 1197, ">": 25137}
points2 = {"(": 1, "[": 2, "{": 3, "<": 4}
pairs = {
    "(": ")",
    "[": "]",
    "{": "}",
    "<": ">",
}
for l in lines:
    s = []
    for c in l:
        if c in pairs.keys():
            s.append(c)
        else:
            if c == pairs[s[-1]]:
                s.pop()
            else:
                ans1 += points[c]
                break
    else:
        if s != []:
            score = 0
            for c in reversed(s):
                score *= 5
                score += points2[c]
            ans2scores.append(score)

print("ans1", ans1)

ans2scores.sort()
print("ans2", ans2scores[(len(ans2scores) // 2)])
