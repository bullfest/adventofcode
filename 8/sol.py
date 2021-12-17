import sys
import q
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
    return sections


def get_grid(lines, f=None, sep=None):
    f = f or (lambda x: x)
    return transpose([list(map(f, l if sep is None else l.split(sep))) for l in lines])


def print_grid(g):
    for l in transpose(g):
        # print(l)
        print("".join(map(lambda n: "X" if n > 10 else str(n % 10), l)))
    print()


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


lines = [l.strip() for l in sys.stdin]

ans1 = 0
ans2 = 0

for l in lines:
    digs, displ = l.split("|")
    digs = list(map(lambda s: frozenset(sorted(s)), digs.strip().split()))
    displ = list(map(lambda s: frozenset(sorted(s)), displ.strip().split()))
    for d in displ:
        if len(d) in [2, 3, 4, 7]:
            ans1 += 1

    key = {}
    for d in digs:
        if len(d) == 2:
            key[1] = d
        if len(d) == 3:
            key[7] = d
        if len(d) == 4:
            key[4] = d
        if len(d) == 7:
            key[8] = d
    for d in digs:
        if len(d) == 5:  # 2 3 5
            if len(d - key[1]) == 3:
                key[3] = d
            elif len(d - key[4]) == 3:
                key[2] = d
            elif len(d - key[4]) == 2:
                key[5] = d
            else:
                print("BORK")
        if len(d) == 6:  # 0 6 9
            if len(d - key[1]) == 5:
                key[6] = d
            elif len(d - key[4]) == 2:
                key[9] = d
            elif len(d - key[4]) == 3:
                key[0] = d
            else:
                print("BORK")

    rev_key = {v: k for k, v in key.items()}
    num = 0
    for d in displ:
        num *= 10
        num += rev_key[d]
    ans2 += num


print("1:", ans1)
print("2:", ans2)
