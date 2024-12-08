from datetime import datetime

import pytest
from django.contrib.auth.models import User

from zmiana.models import Shift


@pytest.fixture
def user():
    u = User.objects.create_user(username='testuser')
    return u

@pytest.fixture
def user2():
    u = User.objects.create_user(username='testuser2')
    return u

@pytest.fixture
def shifts(user, user2):
    shifts = {}
    for u in [user, user2]:
        sh = []
        for x in range(5):
            s = Shift.objects.create(owner=u, active=True, date= datetime(1999,1,x+1).date())
            sh.append(s)
        shifts[u.id] = sh
    return shifts

@pytest.fixture
def shift(user):
    s = Shift.objects.create(owner=user, active=True, date= datetime(1999,1,2).date())
    return s

@pytest.fixture
def shift2(user2):
    s = Shift.objects.create(owner=user2, active=True, date= datetime(1999,1,1).date())
    return s


@pytest.fixture
def shifts_2(user):
    shifts = {}
    skip = 0
    for active in [True, False]:
        sh = []
        for x in range(5):
            s = Shift.objects.create(owner=user, active=active, date= datetime(1999,1,x+1+skip).date())
            sh.append(s)
        skip += 5
        shifts[active] = sh
    return shifts