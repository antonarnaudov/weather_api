import django_filters
from django_filters.rest_framework import DjangoFilterBackend
from datetime import datetime, timedelta
from rest_framework.filters import OrderingFilter
from rest_framework.viewsets import ReadOnlyModelViewSet

from city_weather.models import CityWeather
from city_weather.serializers import CityWeatherSerializer

from core.utils.open_weather_map_api import get_openweathermap_city_weather


class CityWeatherFilter(django_filters.FilterSet):
    city = django_filters.CharFilter(method='city_filter')

    @staticmethod
    def city_filter(qs, name, value):
        filtered = qs.filter(weather__name__icontains=value)  # Filters JSONField by city case-insensitive

        if not filtered:  # If city not in db
            request, data = get_openweathermap_city_weather(value)  # Fetch data from openweathermap

            CityWeather.objects.create(weather=data)  # Store data in db
            filtered = qs.filter(weather__name__icontains=value)  # Refresh qs to get the new city weather

        elif filtered[0].updated_at.replace(tzinfo=None) <= datetime.now() - timedelta(hours=4):  # If info outdated
            request, data = get_openweathermap_city_weather(value)  # Fetch data from openweathermap
            filtered[0].weather = data  # Updates weather data
            filtered[0].save()  # Saves updated data

        return filtered

    class Meta:
        model = CityWeather
        fields = []


class CityWeatherViewSet(ReadOnlyModelViewSet):
    queryset = CityWeather.objects.all()
    serializer_class = CityWeatherSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = CityWeatherFilter
