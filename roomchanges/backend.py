import os
import time

import feedparser
import pandas as pd


def get_feed():
    from .models import RoomChange

    rss_url = os.environ.get("FEED_URL")
    news_feed = feedparser.parse(rss_url, sanitize_html=True)

    RoomChange.objects.all().delete()

    for news in news_feed.entries:
        if news["title"].startswith("Room Changes"):
            data = []
            df_list = pd.read_html(news["summary"], header=0)[0]
            for class_, timetabled_room, assigned_room in zip(
                df_list["Class"], df_list["Timetabled Room"], df_list["Assigned Room"]
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
