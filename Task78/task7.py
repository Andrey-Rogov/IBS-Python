answer = 0


def chain_sum(*args):
    global answer
    if args:
        answer += args[0]
        return chain_sum
    else:
        result = answer
        answer = 0
        return result


def int_to_roman(s):
    vals = {'M': 1000, 'CM': 900, 'D': 500, 'CD': 400, 'C': 100, 'XC': 90,
            'L': 50, 'XL': 40, 'X': 10, 'IX': 9, 'V': 5, 'IV': 4, 'I': 1}
    curr = ""
    for val in vals:
        while s - vals[val] >= 0:
            curr += val
            s -= vals[val]
    return curr
