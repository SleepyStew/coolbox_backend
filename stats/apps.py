import os

from django.apps import AppConfig

from coolbox_backend.backend import scheduler


class StatsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "stats"

    def ready(self):
        print("PRESTART")
        import sys
        if os.environ.get("RUN_MAIN", None) != "true" and not ('manage.py' in sys.argv and 'runserver' not in sys.argv):
            print("STARTED")
            scheduler.start()
