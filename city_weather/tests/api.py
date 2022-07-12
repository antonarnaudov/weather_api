from rest_framework import status
from rest_framework.reverse import reverse

from core.tests.base import BaseApiTests
from city_weather.tests.factory import CityWeatherFactory


class CityWeatherApiTests(BaseApiTests):
    """City Weather API tests, including filters"""

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.city_weather = CityWeatherFactory()  # Adds Sofia to db

    def test_fetch_cities(self):
        url = reverse('cityweather-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_filter_cities(self):
        # Checks if Sofia is already in db
        url = reverse('cityweather-list')
        response = self.client.get(url, {'city': 'sofia'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['weather']['name'], 'Sofia')

        # Checks if Plovdiv is in the db, it is not so api should add it
        url = reverse('cityweather-list')
        response = self.client.get(url, {'city': 'plovdiv'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['weather']['name'], 'Plovdiv')

        # Checks if Plovdiv gets added only once and sofia is not repeated
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
