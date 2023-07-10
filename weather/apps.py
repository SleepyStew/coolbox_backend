import os
import threading

from django.apps import AppConfig

from weather.backend import forecast_loop


class WeatherConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "weather"

    def ready(self):
        if os.environ.get("RUN_MAIN", None) != "true":
            thread = threading.Thread(target=forecast_loop)
            thread.setDaemon(True)
            thread.start()
