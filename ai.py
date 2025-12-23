x = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
]


def right():
    for i in range(len(x)):
        if 1 in x[i]:
            n = x[i].index(1)
            if n < len(x[i]) - 1:
                x[i][n] = 0
                x[i][n + 1] = 1
right()
def left():
    for i in range(len(x)):
        if 1 in x[i]:
            n = x[i].index(1)
            if n != 0:
                x[i][n] = 0
                x[i][n - 1] = 1
left()
def down():
    for col in range(len(x[0])):
        column = [row[col] for row in x]

        if 1 in column:
            n = column.index(1)

            if n < len(column) - 1:
                x[n][col] = 0
                x[n + 1][col] = 1

down()

for cell in x:
    print(cell)
