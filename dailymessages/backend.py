import html
from datetime import datetime

import requests

from coolbox_backend.backend import scheduler


@scheduler.scheduled_job("interval", hours=6, next_run_time=datetime.now())
def get_daily_verse():
    from .models import DailyVerse

    daily_verse_request = requests.get(
        "https://www.biblegateway.com/votd/get/?format=json&version=NLT"
    )

    if daily_verse_request.status_code != 200:
        return

    daily_verse = daily_verse_request.json()["votd"]
    DailyVerse.objects.all().delete()
    DailyVerse.objects.create(
        content=html.unescape(daily_verse["content"]),
        reference=daily_verse["reference"],
        link=daily_verse["permalink"],
    )
