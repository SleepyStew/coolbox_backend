import os

from django.apps import AppConfig

from coolbox_backend.backend import scheduler


class StatsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "stats"

    def ready(self):
        print("PRESTART")
        if os.environ.get("RUN_MAIN", None) != "true":
            print("STARTED")
            scheduler.start()
