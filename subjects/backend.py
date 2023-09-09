from coolbox_backend.backend import scheduler


@scheduler.scheduled_job("interval", minutes=10)
def update_subjects():
    from subjects.models import Subject
    from subjects.subjects import subjects_pretty

    for subject in Subject.objects.all():
        name = subject.name
        for subject_pretty in subjects_pretty:
            if subject_pretty[0] in name:
                subject.pretty = subject_pretty[1]
                subject.save()
                break
