import os
import threading

from django.apps import AppConfig

from stats.backend import debug_loop


class StatsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "stats"

    def ready(self):
        print("PRESTART")
        if os.environ.get("RUN_MAIN", None) != "true":
            print("STARTED")
            thread = threading.Thread(target=debug_loop)
            thread.setDaemon(True)
            thread.start()
