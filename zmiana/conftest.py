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