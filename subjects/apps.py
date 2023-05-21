import os
from threading import Thread

from django.apps import AppConfig

from subjects.backend import update_subjects
from subjects.subjects import subjects_pretty


class SubjectsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "subjects"

    def ready(self):
        if os.environ.get("RUN_MAIN"):
            thread = Thread(target=update_subjects)
            thread.setDaemon(True)
            thread.start()
