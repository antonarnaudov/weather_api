from django.db import models


class CityWeather(models.Model):
    weather = models.JSONField()  # Stores the JSON data from Open Weather Map API
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
