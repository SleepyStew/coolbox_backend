import os
import time

import feedparser
import pandas as pd

from coolbox_backend.backend import scheduler


def get_key(dictionary, search_key):
    for key in dictionary:
        if key.lower().startswith(search_key):
            return key
    return None


@scheduler.scheduled_job("interval", minutes=10)
def get_feed():
    from .models import RoomChange

    rss_url = os.environ.get("FEED_URL")
    news_feed = feedparser.parse(rss_url, sanitize_html=True)

    RoomChange.objects.all().delete()

    for news in news_feed.entries:
        if news["title"].lower().startswith("room change"):
            data = []
            df_list = pd.read_html(news["summary"], header=0)[0]

            classes = df_list.get(get_key(df_list, "class"))
            timetabled_rooms = df_list.get(get_key(df_list, "timetabled"))
            assigned_rooms = df_list.get(get_key(df_list, "assigned"))

            for class_, timetabled_room, assigned_room in zip(
                classes, timetabled_rooms, assigned_rooms
            ):
                # Create a new RoomChange object for each item
                RoomChange.objects.create(
                    class_name=class_,
                    timetabled_room=timetabled_room,
                    assigned_room=assigned_room,
                )
                data.append(
                    {
                        "class": class_,
                        "timetabled_room": timetabled_room,
                        "assigned_room": assigned_room,
                    }
                )
            break


def feed_loop():
    while True:
        try:
            get_feed()
        except Exception as e:
            print(e)
        time.sleep(3600)
