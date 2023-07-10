import os
import time

import requests


def get_forecast():
    from .models import Forecast

    response = requests.get(
        os.environ.get("WEATHER_API_URL"),
    )
    if response.status_code == 200:
        Forecast.objects.create(forecast=response.json())


def forecast_loop():
    while True:
        try:
            get_forecast()
        except Exception as e:
            print(e)
        time.sleep(3600)
