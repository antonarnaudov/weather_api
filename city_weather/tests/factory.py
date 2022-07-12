from factory.django import DjangoModelFactory

from city_weather.models import CityWeather
from core.utils.open_weather_map_api import get_openweathermap_city_weather


class CityWeatherFactory(DjangoModelFactory):
    class Meta:
        model = CityWeather

    _, weather = get_openweathermap_city_weather('sofia')  # Adds data for sofia in weather field
