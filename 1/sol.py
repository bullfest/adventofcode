import sys

depths = [int(l) for l in sys.stdin]
windows = [sum(depths[i - 2 : i + 1]) for i in range(2, len(depths))]

ans1 = 0
ans2 = 0
for i in range(1, len(depths)):
    if depths[i - 1] < depths[i]:
        ans1 += 1
for i in range(1, len(windows)):
    if windows[i - 1] < windows[i]:
        ans2 += 1

print("1:", ans1)
print("2:", ans2)
