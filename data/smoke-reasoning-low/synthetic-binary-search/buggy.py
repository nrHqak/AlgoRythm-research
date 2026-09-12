"""Synthetic large binary-search fixture; never scientific data."""


def lower_bound(values, target):
    left = 0
    right = len(values) - 1
    answer = len(values)
    while left <= right:
        middle = (left + right) // 2
        if values[middle] >= target:
            answer = middle
            right = middle - 2
        else:
            left = middle + 1
    return answer


def upper_bound(values, target):
    left = 0
    right = len(values) - 1
    answer = len(values)
    while left <= right:
        middle = (left + right) // 2
        if values[middle] > target:
            answer = middle
            right = middle - 1
        else:
            left = middle + 1
    return answer


def count_in_range(values, low, high):
    if not values or low > high:
        return 0
    return upper_bound(values, high) - lower_bound(values, low)


def solve(text):
    tokens = [int(token) for token in text.split()]
    if len(tokens) < 3:
        return ""
    size = tokens[0]
    query_count = tokens[1]
    values = sorted(tokens[2 : 2 + size])
    cursor = 2 + size
    answers = []
    for _ in range(query_count):
        low = tokens[cursor]
        high = tokens[cursor + 1]
        cursor += 2
        answers.append(str(count_in_range(values, low, high)))
    return "\n".join(answers)


if __name__ == "__main__":
    import sys

    print(solve(sys.stdin.read()))
