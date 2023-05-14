import os
import threading

from django.apps import AppConfig


class AuthConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "schoolboxauth"

    def ready(self):
        from schoolboxauth.backend import delete_old_tokens
        from schoolboxauth.models import Token

        if os.environ.get("RUN_MAIN"):
            thread = threading.Thread(target=delete_old_tokens)
            thread.setDaemon(True)
            thread.start()
