from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from coolbox_backend.tests import authenticated_test_client
from schoolboxauth.models import User
from stats.views import status_types


class RunningViewTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()

    def test_running_view(self):
        response = self.client.get("/stats/running")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("uptime", response.data)


class UserCountViewTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()

    def test_user_count_view(self):
        response = self.client.get("/stats/user_count")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], User.objects.count())


class MessageViewTestCase(APITestCase):
    def setUp(self):
        self.client = authenticated_test_client()

    def test_message_view(self):
        response = self.client.get("/stats/message")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for status_type in status_types:
            self.assertIn(status_type, response.data)
