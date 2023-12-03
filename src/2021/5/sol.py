import sys

lines = [l.strip() for l in sys.stdin]
segments = []
max_x = -1
max_y = -1
for l in lines:
    parts = l.split(" ")
    print(parts)
    x1, y1 = map(int, parts[0].split(","))
    x2, y2 = map(int, parts[2].split(","))
    max_x = max(x1, x2, max_x)
    max_y = max(y1, y2, max_y)
    segments.append(list(sorted([(x1, y1), (x2, y2)])))


def sign(n1, n2):
    if n1 - n2 < 0:
        return -1
    else:
        return 1


max_y += 1
max_x += 1
field = [[0] * max_y for _ in range(max_x)]

for p1, p2 in segments:
    x1, y1 = p1
    x2, y2 = p2

    dx = x2 - x1
    dy = y2 - y1

    if 0 not in [dx, dy]:
        pass  # continue
    x = x1
    y = y1
    for n in range(max(abs(dx), abs(dy)) + 1):
        field[x][y] += 1
        if dx < 0:
            x -= 1
        if dx > 0:
            x += 1
        if dy < 0:
            y -= 1
        if dy > 0:
            y += 1


ans1 = 0

for row in field:
    for n in row:
        if n > 1:
            ans1 += 1


print("1:", ans1)
