# 2 - > [2]
# 3 - > [3]
# 4 - > [2, 2]
# 12 - [2,2,3]
#
# 32 - [2,2,2,2,2]
from xmlrpc.client import Fault

import pytest


def prime_numbers(n):
    lst = []
    divider = 2
    while n > 1:
        while n % divider == 0:
            lst.append(divider)
            n = n // divider
        divider += 1
    return lst


@pytest.mark.parametrize("n, lst", (
        (1, []),
        (2, [2]),
        (3, [3]),
        (4, [2, 2]),
        (5, [5]),
        (6, [2, 3]),
        (7, [7]),
        (8, [2, 2, 2]),
        (9, [3, 3]),
        (2 * 2 * 2 * 2 * 3 * 3 * 11 * 13 * 17, [2, 2, 2, 2, 3, 3, 11, 13, 17]),
))
def test_tdd_prime_number(n, lst):
    assert prime_numbers(n) == lst


def check_password(password):
    special = "!@#$%^&*()_+}{\":?><';/.,]["
    return (any(x for x in password if x.isupper()) and
            any(x for x in password if x.islower()) and
            any(x for x in password if x.isdigit()) and
            any(x for x in password if x in special) and
            len(password) >= 8)


@pytest.mark.parametrize("password, result", [
    ('aaaa', False),
    ('Aaaa', False),
    ('AAAA', False),
    ('1aAA', False),
    ('1aAA0000', False),
    ('1aAA00;0', True)
])
def test_check_password(password, result):
    assert check_password(password) == result