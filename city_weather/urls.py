from django.urls import path, include
from rest_framework.routers import DefaultRouter

from city_weather.viewsets import CityWeatherViewSet

router = DefaultRouter()
router.register(r'cityweather', CityWeatherViewSet, basename='cityweather')

urlpatterns = [
    path('', include(router.urls)),
]
