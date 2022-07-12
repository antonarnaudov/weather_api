from unittest import TestCase

from city_weather.models import CityWeather
from city_weather.tests.factory import CityWeatherFactory


class CityWeatherModelTests(TestCase):
    """Model tests for CityWeather"""
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.city_weather = CityWeatherFactory()

    def test_has_model(self):
        city_weather = CityWeather(weather={'weather': 'test'})
        self.assertIsInstance(city_weather, CityWeather)

    def test_can_create(self):
        city_weather = CityWeatherFactory()
        self.assertIsInstance(city_weather, CityWeather)
        self.assertEqual(city_weather.weather, CityWeatherFactory.weather)
