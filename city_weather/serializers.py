from rest_framework import serializers

from city_weather.models import CityWeather


class CityWeatherSerializer(serializers.ModelSerializer):
    class Meta:
        model = CityWeather
        fields = '__all__'
