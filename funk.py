from datetime import datetime
from random import randint

def div(a,b):
    return a / b


def analyze_pesel(pesel):
    weights = [1,3,7,9,
    1, 3, 7, 9, 1, 3]
    weight_index=0
    digits_sum= 0
    for digit in pesel[ : -1 ]:
        digits_sum +=int(digit)*weights[weight_index]
        weight_index+=1
    pesel_modulo = digits_sum % 10
    validate = 10-pesel_modulo
    if validate == 10:
        validate = 0
    gender = "male" if int(pesel[-2]) % 2==1 else "female"
    m = int(pesel[2:4])
    dodatkowe_dwudziestki = m//20
    m = m % 20
    lst = ['19', '20','21','22', '18']
    year = int(lst[dodatkowe_dwudziestki] + pesel[0: 2])
    d = int(pesel[4 :6])
    print(year, m, d)
    birth_date = datetime(year, m ,d)
    result = {
        "pesel":pesel,
        "valid":validate == int(pesel[-1]),
        "gender":gender,
        "birth_date": birth_date
            }
    return result