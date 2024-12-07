import pytest
from django.test import Client
from django.urls import reverse


@pytest.mark.django_db
def test_index_view():
    client = Client()
    url = reverse('home')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_my_duty_not_login():
    client = Client() # tworze przegladarke
    url = reverse('my_duty') # pobieram z url'a adres na który bede chciał wejść
    response = client.get(url) # używam przeglądarki by wejść na zadany adres
    assert response.status_code == 302 # sprawdzam czy status odpwiedzi jest oczekiwanym statusem
    assert response.url.startswith(reverse('login'))
