import os
import threading

from django.apps import AppConfig

from roomchanges.backend import feed_loop


class RoomchangesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "roomchanges"

    def ready(self):
        if os.environ.get("RUN_MAIN"):
            thread = threading.Thread(target=feed_loop)
            thread.setDaemon(True)
            thread.start()
