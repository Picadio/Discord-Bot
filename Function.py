def in_2(x):
    n = []
    while x != 0:
        tmp = x % 2
        n.append(str(tmp))
        x //= 2
    n.reverse()
    q = ""
    for s in n:
        q += s
    return q


def in_8(x):
    n = []
    while x != 0:
        tmp = x % 8
        n.append(str(tmp))
        x //= 8
    n.reverse()
    q = ""
    for s in n:
        q += s
    return q


def in_16(x):
    n = []
    while x != 0:
        tmp = x % 16
        if tmp == 10:
            temp = "A"
        elif tmp == 11:
            temp = "B"
        elif tmp == 12:
            temp = "C"
        elif tmp == 13:
            temp = "D"
        elif tmp == 14:
            temp = "E"
        elif tmp == 15:
            temp = "F"
        else:
            temp = str(tmp)
        n.append(temp)
        x //= 16
    n.reverse()
    q = ""
    for s in n:
        q += s
    return q


def det(n, arr):
    print(arr)
    if n == 2:
        return arr[0][0] * arr[1][1] - arr[0][1] * arr[1][0]

    ans = 0
    for i in range(n):
        arrcp = []
        for i1 in range(1, n):
            arrcp.append([arr[i1][j] for j in range(n) if (j != i)])
        ans += arr[0][i] * pow(-1, i + 1 + 1) * det(n - 1, arrcp)
        print("ANSWER")
        print(ans)
    return ans