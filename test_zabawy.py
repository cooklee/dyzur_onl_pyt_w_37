from datetime import datetime

import pytest

from funk import div, analyze_pesel

def test_div_by_zero():
    with pytest.raises(ZeroDivisionError):
        div(12, 0)

@pytest.mark.parametrize("pesel", [
    "52081578994",
    "96081326355",
    "55101045498",
    "81071158555"
])
def test_analyze_pesel(pesel):
    result = analyze_pesel(pesel)
    assert result['pesel'] == pesel

@pytest.mark.parametrize("pesel", [
    "52081578994",
    "96081326355",
    "55101045498",
    "81071158555"
])
def test_analyze_pesel_valid(pesel):
    result = analyze_pesel(pesel)
    assert result['valid']

@pytest.mark.parametrize("pesel", [
    "52081578993",
    "96081326353",
    "55101045493",
    "81071158553"
])
def test_analyze_pesel_not_valid(pesel):
    result = analyze_pesel(pesel)
    assert not result['valid']


@pytest.mark.parametrize("pesel, gender", [
    ("52081578994",'male'),
    ("96081326355",'male'),
    ("55101045498",'male'),
    ("81071158555",'male'),
    ("83040993666",'female'),
    ("54011417544",'female'),
    ("86090116863",'female'),
    ("97030879443",'female'),
])
def test_analyze_pesel_gender(pesel, gender):
    result = analyze_pesel(pesel)
    assert result['gender'] == gender


@pytest.mark.parametrize("pesel, birth_date", [
    ("52081578994",datetime(1952,8,15)),
    ("96081326355",datetime(1996,8,13)),
    ("55101045498",datetime(1955,10,10)),
    ("83040993666",datetime(1983,4,9)),
    ("54011417544",datetime(1954, 1, 14)),
    ("53270871236", datetime(2053, 7, 8)),



])
def test_analyze_pesel_gender(pesel, birth_date):
    result = analyze_pesel(pesel)
    assert result['birth_date'] == birth_date


