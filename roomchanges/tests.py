import os

import feedparser
from rest_framework.test import APITestCase


class RoomChangeFeedTestCase(APITestCase):
    def test_room_changes_feed(self):
        rss_url = os.environ.get("FEED_URL")
        news_feed = feedparser.parse(rss_url, sanitize_html=True)

        self.assertEqual(news_feed.status, 200)
