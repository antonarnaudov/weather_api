from django.db import models


class CityWeather(models.Model):
    weather = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
