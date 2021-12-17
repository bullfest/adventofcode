import sys
from collections import defaultdict

lines = [l.strip() for l in sys.stdin]
fishes = list(map(int, lines[0].split(",")))

buckets = defaultdict(lambda: 0)
for f in fishes:
    buckets[f] += 1
print(buckets)
for n in range(1, 257):
    new_bucket = defaultdict(lambda: 0)
    new_bucket[6] = buckets[0]
    new_bucket[8] = buckets[0]
    for i in range(1, 9):
        new_bucket[i - 1] += buckets[i]
    buckets = new_bucket
    print(buckets)

print("1:", sum(buckets.values()))
