import sys

lines = [l.strip() for l in sys.stdin]
nums = list(map(int, lines[0].split(",")))
boards = []

board = []
for l in lines[1:]:
    if l == "":
        if board != []:
            boards.append(board)
        board = []
        continue
    board.append(list(map(int, l.split())))
boards.append(board)

marks = [[[False] * len(l) for l in b] for b in boards]


def mark(n):
    for i, board in enumerate(boards):
        for j, line in enumerate(board):
            if n in line:
                marks[i][j][line.index(n)] = True


def scoref(board, marks):
    s = 0
    for i in range(len(marks)):
        for j in range(len(marks[i])):
            if not marks[i][j]:
                s += board[i][j]
    return s


def won():
    for i, marks_b in enumerate(marks):
        # lines
        for j, line in enumerate(marks_b):
            print(line)
            if all(line):
                print("won", i)
                return i

        # columns
        for j, line in enumerate(list(zip(*marks_b))):
            print("col", line)
            if all(line):
                print("won", i)
                return i
    return None


i = 0
ans = None
for num in nums:
    mark(num)
    print(len(boards), num)
    while (i := won()) is not None:
        print("wwwon", i)
        if len(boards) == 1:
            score = scoref(boards[i], marks[i])
            ans = score * num
            break
        print("winning", len(boards), i, num)
        del boards[i]
        del marks[i]
    if ans is not None:
        break

for b in marks:
    print("\n".join(map(str, b)))
    print()

print("1:", ans)
