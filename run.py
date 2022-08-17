str = "PAYPALISHIRING"
# str = "ABCDE"


def convert(input, rows_num):
    if rows_num == 1 or len(input) <= 1:
        return input
    result = []
    step = (rows_num - 1) * 2
    for line_num in range(rows_num):
        for i in range(0, len(input) - 1, step):
            left_candidate = i + line_num
            if left_candidate < len(input) and left_candidate not in result:
                result.append(left_candidate)
            right_candidate = i + step - line_num
            if right_candidate < len(input) and right_candidate not in result:
                result.append(right_candidate)
    return "".join([input[i] for i in result])


print(convert(str, 3))
# print(convert(str, 4))
# print(convert(str, 5))
