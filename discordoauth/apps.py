import os
import threading
import time

from django.apps import AppConfig

from discordoauth.backend import refresh_tokens


class DiscordoauthConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "discordoauth"

    def ready(self):
        if os.environ.get("RUN_MAIN"):
            thread = threading.Thread(target=refresh_tokens)
            thread.setDaemon(True)
            thread.start()

            from discordoauth.backend import set_missing_ids

            thread = threading.Thread(target=set_missing_ids)
            thread.setDaemon(True)
            thread.start()
