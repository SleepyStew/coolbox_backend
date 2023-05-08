import os
import threading

from django.apps import AppConfig

from reminders.backend import reminder_check


class RemindersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "reminders"

    def ready(self):
        if os.environ.get('RUN_MAIN'):
            thread = threading.Thread(target=reminder_check)
            thread.setDaemon(True)
            thread.start()