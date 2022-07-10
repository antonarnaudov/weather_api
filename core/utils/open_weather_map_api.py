import requests
from rest_framework import status
from django.conf import settings
from django.http import Http404


def get_openweathermap_city_weather(city):
    request = requests.get(
        f'{settings.OWM_API_URL}?q={city}&appid={settings.OWM_API_KEY}&units={settings.OWM_DEFAULT_UNITS}')

    if request.status_code == status.HTTP_404_NOT_FOUND:
        raise Http404()

    return request, request.json()
