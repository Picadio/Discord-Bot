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


def add2(x1, x2):
    nxt = 0
    ans = ""
    num1 = x1[::-1]
    num2 = x2[::-1]

    if len(num1) > len(num2):
        for i in range(len(num1)-len(num2)):
            num2 += '0'
    if len(num1) < len(num2):
        for i in range(len(num2)-len(num1)):
            num1 += '0'
    for i in range(len(x1)):
        if num1[i] == '1' and num2[i] == '1':
            buf = '0'
            if nxt == 1:
                buf = '1'
            ans += buf
            nxt = 1
        elif (num1[i] == '1' and num2[i] == '0') or (num1[i] == '0' and num2[i] == '1'):
            buf = '1'
            if nxt == 1:
                buf = '0'
                nxt = 1
            ans += buf
        else:
            buf = '0'
            if nxt == 1:
                buf = '1'
                nxt = 0
            ans += buf
    if nxt == 1:
        ans += '1'
    print(ans[::-1])
    return ans[::-1]


def reform(x, input_type, output_type):
    if input_type == "2":
        step = 1
        sum = 0
        for i in x[::-1]:
            sum += int(i)*step
            step *= 2
        if output_type == "2":
            return x
        if output_type == "8":
            return in_8(sum)
        if output_type == "10":
            return sum
        if output_type == "16":
            return in_16(sum)
    if input_type == "8":
        step = 1
        sum = 0
        for i in x[::-1]:
            sum += int(i)*step
            step *= 8
        if output_type == "2":
            return in_2(sum)
        if output_type == "8":
            return x
        if output_type == "10":
            return sum
        if output_type == "16":
            return in_16(sum)
    if input_type == "10":
        if output_type == "2":
            return in_2(int(x))
        if output_type == "8":
            return in_8(int(x))
        if output_type == "10":
            return x
        if output_type == "16":
            return in_16(int(x))
    if input_type == "16":
        step = 1
        sum = 0
        for i in x[::-1]:

            if i.upper() == "A":
                num = 10
            elif i.upper() == "B":
                num = 11
            elif i.upper() == "C":
                num = 12
            elif i.upper() == "D":
                num = 13
            elif i.upper() == "E":
                num = 14
            elif i.upper() == "F":
                num = 15
            else:
                num = int(i)
            sum += num*step
            step *= 16
        if output_type == "2":
            return in_2(sum)
        if output_type == "8":
            return in_8(sum)
        if output_type == "10":
            return sum
        if output_type == "16":
            return x
