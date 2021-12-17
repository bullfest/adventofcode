import sys
from collections import defaultdict

lines = [l.strip() for l in sys.stdin]
octi = [list(map(int, l)) for l in lines]


def neighbours(x, y):
    l = []
    if x > 0:
        l.append((x - 1, y))
        if y > 0:
            l.append((x - 1, y - 1))
        if y + 1 < len(octi[0]):
            l.append((x - 1, y + 1))
    if y > 0:
        l.append((x, y - 1))

    if x + 1 < len(octi):
        l.append((x + 1, y))
        if y > 0:
            l.append((x + 1, y - 1))
        if y + 1 < len(octi[0]):
            l.append((x + 1, y + 1))
    if y + 1 < len(octi[0]):
        l.append((x, y + 1))
    return l


def print_map():
    for l in octi:
        # print(l)
        print("".join(map(lambda n: "X" if n > 10 else str(n % 10), l)))
    print()


ans1 = 0

# print("start state")
# print_map()
for step in range(1000):
    if step == 100:
        print(ans1)
    for x in range(len(octi)):
        for y in range(len(octi[0])):
            octi[x][y] += 1

    # print("Doin step",step+1)
    # print_map()
    again = True

    while again:
        again = False
        for x in range(len(octi)):
            for y in range(len(octi[0])):
                if octi[x][y] == 10:
                    ans1 += 1
                    octi[x][y] += 1
                    again = True
                    for px, py in neighbours(x, y):
                        if octi[px][py] != 10:
                            octi[px][py] += 1
        # print_map()

    all_blink = True
    for x in range(len(octi)):
        for y in range(len(octi[0])):
            if octi[x][y] > 9:
                octi[x][y] = 0
            else:
                all_blink = False
    if all_blink:
        print(step + 1)
        break
