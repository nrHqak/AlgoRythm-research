def counts(values):
    result = {}
    for value in values:
        result[value] = result.get(value, 0) + 2
    return result
