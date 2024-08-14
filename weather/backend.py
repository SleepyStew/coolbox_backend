import os
from datetime import datetime

import humanize
import requests

from coolbox_backend.backend import scheduler
from weather.constants import weathercodes


@scheduler.scheduled_job("interval", minutes=60)
def get_forecast():
    from .models import Forecast

    response = requests.get(
        os.environ.get("WEATHER_API_URL"),
    )
    forecast = {}
    if response.status_code == 200:
        response = response.json()
        days = len(response["daily"]["time"])
        for i in range(days):
            time_real = datetime.fromtimestamp(response["daily"]["time"][i])
            forecast[i] = {
                "time": (
                    humanize.naturalday(time_real).title()
                    if i < 2
                    else time_real.strftime("%A")
                ),
                "time_real": str(time_real),
                "weathercode": weathercodes[response["daily"]["weathercode"][i]],
                "temperature_2m_max": response["daily"]["temperature_2m_max"][i],
                "temperature_2m_min": response["daily"]["temperature_2m_min"][i],
                "uv_index_max": response["daily"]["uv_index_max"][i],
                "precipitation_probability_mean": response["daily"][
                    "precipitation_probability_mean"
                ][i],
            }

        Forecast.objects.all().delete()
        Forecast.objects.create(forecast=forecast)
