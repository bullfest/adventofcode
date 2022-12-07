import sys
from collections import defaultdict

lines = [l.strip() for l in sys.stdin]
positions = list(map(int, lines[0].split(",")))

min_pos = min(positions)
max_pos = max(positions)
min_fuel = 100000000000000000
for m in range(min_pos, max_pos):
    s = 0
    for p in positions:
        d = abs(m - p)
        s += (d * (1 + d)) / 2
    min_fuel = min(s, min_fuel)
    print(m, s)
print(min_fuel)
