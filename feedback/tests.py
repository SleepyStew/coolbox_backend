from rest_framework import status
from rest_framework.test import APITestCase

from coolbox_backend.tests import authenticated_test_client


class FeedbackViewTestCase(APITestCase):
    def setUp(self):
        self.client = authenticated_test_client()

    def test_discord_view(self):
        discord_endpoint = "/feedback"

        data = {
            "content": "Test message.",
            "origin": "test",
        }

        response = self.client.post(discord_endpoint, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, data)
