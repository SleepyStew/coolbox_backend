from django.test import TestCase

# Create your tests here.
import requests
from rest_framework.test import APITestCase


class DailyVerseAPITestCase(APITestCase):
    def test_daily_verse_api(self):
        response = requests.get(
            "https://www.biblegateway.com/votd/get/?format=json&version=NIV"
        )
        self.assertEqual(response.status_code, 200)
