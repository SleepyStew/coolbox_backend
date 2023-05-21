import os

from django.apps import AppConfig

from subjects.subjects import subjects_pretty


class SubjectsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "subjects"

    def ready(self):
        from subjects.models import Subject

        if os.environ.get("RUN_MAIN"):
            for subject in Subject.objects.all():
                name = subject.name
                for subject_pretty in subjects_pretty:
                    if subject_pretty[0] in name:
                        subject.pretty = subject_pretty[1]
                        subject.save()
                        break
