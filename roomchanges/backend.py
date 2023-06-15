import os
from pprint import pprint

import feedparser
from dotenv import load_dotenv


def get_feed():
    rss_url = os.environ.get('FEED_URL')
    news_feed = feedparser.parse(rss_url)

    pprint(news_feed.entries[0])


if __name__ == '__main__':
    load_dotenv()
    get_feed()
