import cgi

form = cgi.FieldStorage()
user_input = form.getvalue("userInput")


def int_to_roman(number: int):
    vals = {'M': 1000, 'CM': 900, 'D': 500, 'CD': 400, 'C': 100, 'XC': 90,
            'L': 50, 'XL': 40, 'X': 10, 'IX': 9, 'V': 5, 'IV': 4, 'I': 1}
    curr = ""
    for val in vals:
        while number - vals[val] >= 0:
            curr += val
            number -= vals[val]
    return curr


print(int_to_roman(int(user_input)))
