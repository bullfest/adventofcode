import itertools
import math

min_x = min_y = 0
max_x = None
max_y = None


def transpose(m):
    """[[1, 2], [3, 4]] -> [[1, 3], [2, 4]]"""
    return list(map(list, zip(*m)))


def get_sections(lines):
    """Split lines on empty lines"""
    sections = []
    section = []
    for l in lines:
        if l == "":
            if section != []:
                sections.append(section)
                section = []
        else:
            section.append(l)
    sections.append(section)
    return sections


def parse_ints(*l):
    return list(map(int, l))


def get_grid(lines, f=None, sep=None):
    """ """
    f = f or (lambda x: x)
    return transpose([list(map(f, l if sep is None else l.split(sep))) for l in lines])


def print_grid(g):
    for l in transpose(g):
        print("".join(l))
        # print("".join(map(lambda n: "X" if n > 10 else str(n % 10), l)))
    print()


def zero_index_points(points):
    return [(x - 1, y - 1) for x, y in points]


def points_to_grid(points, default_value=False, point_value=True):
    max_x = 0
    max_y = 0
    for x, y in points:
        max_x = max(x, max_x)
        max_y = max(y, max_y)

    grid = [[default_value] * (max_y + 1) for _ in range(max_x + 1)]
    for x, y in points:
        grid[x][y] = point_value
    return grid


def neighbours(x, y, diagonal=False):
    l = []
    if x > min_x:
        l.append((x - 1, y))
        if y > min_y and diagonal:
            l.append((x - 1, y - 1))
        if y + 1 < max_y and diagonal:
            l.append((x - 1, y + 1))
    if y > min_y:
        l.append((x, y - 1))

    if x + 1 < max_x:
        l.append((x + 1, y))
        if y > min_y and diagonal:
            l.append((x + 1, y - 1))
        if y + 1 < max_y and diagonal:
            l.append((x + 1, y + 1))
    if y + 1 < max_y:
        l.append((x, y + 1))
    return l


def polygon_area(points):
    border_len = 0
    area = 0
    # https://www.mathopenref.com/coordpolygonarea2.html
    for n1, n2 in itertools.pairwise(points + points[:1]):
        x1, y1 = n1
        x2, y2 = n2
        area += (x2 + x1) * (y2 - y1)
        border_len += math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    area = area / 2
    # For a shape like this the
    # right and bottom edges won't have their edges counted
    # x-----x
    # |     |
    # |     x----x
    # |          |
    # |  x---x   |
    # |  |   |   |
    # x--x   x---x
    #
    # Zoomed in (x are discrete coords), the #:s are counted but not the O:s
    #     x
    #  ###|OOO
    #  ###|OOO
    #  ###|OOO
    # x---x
    #  OOO OOO
    #  OOO OOO
    #  OOO OOO
    #
    # As exactly half of the edges are right/bottom edges we can add them.
    area += border_len / 2
    # The final +1 is for the bottom-right-most corner
    # Other bottom-right (_|) corners don't need to be added as there's always a corresponding
    # top-left inner corner (Γ) that's counted doubly (as it has both a right-edge and a bottom edge)
    area += 1
    return area
