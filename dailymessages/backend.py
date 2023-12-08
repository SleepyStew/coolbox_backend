import html

import requests

from coolbox_backend.backend import scheduler


@scheduler.scheduled_job("interval", hours=6)
def get_daily_verse():
    from .models import DailyVerse

    print("hey")
    daily_verse_request = requests.get(
        "https://www.biblegateway.com/votd/get/?format=json&version=NIV"
    )
    if daily_verse_request.status_code != 200:
        return

    daily_verse = daily_verse_request.json()["votd"]
    DailyVerse.objects.all().delete()
    DailyVerse.objects.create(
        content=html.unescape(daily_verse["content"]), reference=daily_verse["reference"], link=daily_verse["permalink"]
    )
