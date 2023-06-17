import os
from pprint import pprint

from django.apps import AppConfig


class StatsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "stats"

    def ready(self):
        print("PRESTART")
        if os.environ.get("RUN_MAIN", None) != "true":
            print("STARTED")
