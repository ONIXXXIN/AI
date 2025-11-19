
x = [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0]
if 1 in x:
    n = x.index(1)
    if n < len(x) - 1:
        x[n] = 0
        x[n+1] = 1
    print(x)

