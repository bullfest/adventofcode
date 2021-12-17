import time
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


edges = [l.strip().split("-") for l in sys.stdin]

edgelist = defaultdict(set)
for n1, n2 in edges:
    edgelist[n1].add(n2)
    edgelist[n2].add(n1)


def dfs1(node, visited):
    if node == "end":
        return 1
    s = 0
    for neigh in edgelist[node]:
        vis = visited | {node}
        if neigh.islower() and neigh in visited:
            continue
        s += dfs1(neigh, vis)
    return s


def dfs2(node, visited, smalltwice, path, logs):
    # time.sleep(1)
    path = path + [node]
    if node == "end":
        print("\n".join(logs))
        print()
        # print(path)
        return 1
    s = 0
    for neigh in edgelist[node]:
        vis = visited | {node}
        if neigh.islower() and neigh in visited:
            # print(neigh, smalltwice, visited, path)
            if neigh == "start" or smalltwice:
                continue
            s += dfs2(neigh, vis, True, path, logs + [f"Visiting {neigh} again"])
            continue
        # print("Vis", node, neigh, smalltwice)
        s += dfs2(
            neigh, vis, smalltwice, path, logs + [f"{node}->{neigh} {smalltwice}"]
        )
    return s


ans1 = dfs1("start", frozenset("start"))
ans2 = dfs2("start", frozenset("start"), False, [], [])
print("1:", ans1)
print("2:", ans2)
