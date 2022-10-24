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
        arr_copy = []
        for i1 in range(1, n):
            arr_copy.append([arr[i1][j] for j in range(n) if (j != i)])
        ans += arr[0][i] * pow(-1, i + 1 + 1) * det(n - 1, arr_copy)
        print("ANSWER")
        print(ans)
    return ans





def reform(x, input_type, output_type):
    if input_type == output_type:
        return x
    if input_type == "2" or input_type == "8" or input_type == "16":
        step = 1
        sum = 0
        for i in x[::-1]:
            if i == 'A':
                ii = 10
            elif i == 'B':
                ii = 11
            elif i == 'C':
                ii = 12
            elif i == 'D':
                ii = 13
            elif i == 'E':
                ii = 14
            elif i == 'F':
                ii = 15
            else:
                ii = int(i)
            sum += ii*step
            step *= int(input_type)
        x = sum
    elif input_type != "10":
        return "Ви вказали невірну систему числення"
    if output_type == "10":
        return x
    elif output_type == "2":
        return in_2(int(x))
    elif output_type == "8":
        return in_8(int(x))
    elif output_type == "16":
        return in_16(int(x))
    return "Ви вказали невірну систему числення"
