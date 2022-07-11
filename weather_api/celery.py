from __future__ import absolute_import, unicode_literals
import os

from celery import Celery

# Set the default Django settings module for the 'celery' program.

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'weather_api.settings')

app = Celery('weather_api', include=['city_weather.celery'])

# Dict with Scheduled Celery tasks - extend only with Scheduled tasks
app.conf.beat_schedule = {
    "update_city_weather_data_per_day": {
        "task": "city_weather.celery.update_city_weather_data",
        # "schedule": 60.0  # every minute
        "schedule": 86400.0  # every day
    }
}

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

# celery -A weather_api worker -l info --pool=solo
# celery -A weather_api beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler
