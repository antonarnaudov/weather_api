from rest_framework import serializers

from city_weather.models import CityWeather


class CityWeatherSerializer(serializers.ModelSerializer):
    """Serializer for CityWeather with all fields"""
    class Meta:
        model = CityWeather
        fields = '__all__'
