import os
import threading

from django.apps import AppConfig

from discordoauth.backend import startup_logic, refresh_tokens


class DiscordoauthConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "discordoauth"

    def ready(self):
        if os.environ.get("RUN_MAIN", None) != "true":
            thread = threading.Thread(target=refresh_tokens)
            thread.setDaemon(True)
            thread.start()

            thread = threading.Thread(target=startup_logic)
            thread.setDaemon(True)
            thread.start()
