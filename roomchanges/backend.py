import os
import time

import pandas as pd
import feedparser
from datetime import datetime


data = []
last_updated = None


def get_feed():
    global data, last_updated
    rss_url = os.environ.get("FEED_URL")
    news_feed = feedparser.parse(rss_url, sanitize_html=True)

    for news in news_feed.entries:
        if news["title"].startswith("Room Changes"):
            data = []
            df_list = pd.read_html(news["summary"])[0][1:]
            for class_, timetabled_room, assigned_room in zip(
                df_list[2], df_list[4], df_list[5]
            ):
                data.append(
                    {
                        "class": class_,
                        "timetabled_room": timetabled_room,
                        "assigned_room": assigned_room,
                    }
                )
            last_updated = day()
            break


def feed_loop():
    while True:
        try:
            get_feed()
        except Exception as e:
            print(e)
        time.sleep(3600)


def day():
    return datetime.now().day
