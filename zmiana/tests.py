import pytest
from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse

from zmiana.forms import ChangeShiftForm
from zmiana.models import Shift, ChangeShiftProposal


@pytest.mark.django_db
def test_index_view():
    client = Client()
    url = reverse('home')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_my_duty_not_login():
    client = Client()  # tworze przegladarke
    url = reverse('my_duty')  # pobieram z url'a adres na który bede chciał wejść
    response = client.get(url)  # używam przeglądarki by wejść na zadany adres
    assert response.status_code == 302  # sprawdzam czy status odpwiedzi jest oczekiwanym statusem
    assert response.url.startswith(reverse('login'))


@pytest.mark.django_db
def test_my_duty_login(user, shifts):
    client = Client()
    client.force_login(user)
    url = reverse('my_duty')  # pobieram z url'a adres na który bede chciał wejść
    response = client.get(url)  # używam przeglądarki by wejść na zadany adres
    assert response.status_code == 200
    user_shift = response.context['shifts']
    assert user_shift.count() == len(shifts[user.id])
    for my_shift in shifts[user.id]:
        assert my_shift in user_shift


@pytest.mark.django_db
def test_my_duty_login_active(user, shifts_2):
    client = Client()
    client.force_login(user)
    url = reverse('my_duty')  # pobieram z url'a adres na który bede chciał wejść
    response = client.get(url)  # używam przeglądarki by wejść na zadany adres
    assert response.status_code == 200
    user_shift = response.context['shifts']
    assert user_shift.count() == len(shifts_2[True])
    for my_shift in shifts_2[True]:
        assert my_shift in user_shift


@pytest.mark.django_db
def test_add_new_shift_get(user):
    client = Client()
    client.force_login(user)
    url = reverse('add_new_shift')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_add_new_shift_post(user):
    client = Client()
    client.force_login(user)
    url = reverse('add_new_shift')
    dane = {
        'date':'1999-09-09',
    }
    response = client.post(url, dane)
    assert response.status_code == 302
    assert response.url.startswith(reverse('add_new_shift'))
    assert Shift.objects.count()==1

@pytest.mark.django_db
def test_change_shift_proposal_get(user, user2,shift, shift2):
    client = Client()
    client.force_login(user)
    url = reverse('change_shift_proposal')
    response = client.get(url)
    assert response.status_code == 200
    assert isinstance(response.context['form'], ChangeShiftForm)

@pytest.mark.django_db
def test_change_shift_proposal_post(user, user2,shift, shift2):
    client = Client()
    client.force_login(user)
    url = reverse('change_shift_proposal')
    dane = {
        'from_shift':shift.id,
        'to_shift':shift2.id,
    }
    response = client.post(url, dane)
    assert response.status_code == 302
    assert response.url.startswith(reverse('home'))
    shift.refresh_from_db()
    assert ChangeShiftProposal.objects.first()



