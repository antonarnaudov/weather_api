from weather_api.celery import app
from city_weather.models import CityWeather
from core.utils.open_weather_map_api import get_openweathermap_city_weather
from datetime import timedelta, datetime


@app.task
def update_city_weather_data():
    """Celery task that fetches the latest weather data per city in the db and updates it"""
    all_cities = CityWeather.objects.all()

    for city in all_cities:
        request, data = get_openweathermap_city_weather(city.weather['name'])  # Fetch data from openweathermap
        city.weather = data  # Updates weather data
        city.save()  # Saves updated data

    print(f'>>> CityWeather data updated at {datetime.strftime(datetime.utcnow(), "%m/%d/%Y %H:%M:%S")}')
    print(f'>>> Next Update scheduled for {datetime.strftime(datetime.utcnow() + timedelta(days=1), "%m/%d/%Y %H:%M:%S")}')
