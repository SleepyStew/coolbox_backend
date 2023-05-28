from rest_framework import status
from rest_framework.test import APITestCase

from coolbox_backend.tests import authenticated_test_client


class ReminderViewTestCase(APITestCase):
    def setUp(self):
        self.client = authenticated_test_client()

    def test_subject_view(self):
        response = self.client.get("/reminders")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

        reminder = {
            "title": "Test Reminder",
            "due": 0,
            "method": "both",
        }

        response = self.client.post("/reminders", reminder, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], reminder["title"])
        self.assertEqual(response.data["due"], reminder["due"])
        self.assertEqual(response.data["method"], reminder["method"])

        response = self.client.get("/reminders")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        reminder_id = response.data[0]["id"]

        reminder_edit = {
            "id": reminder_id,
            "title": "Test Reminder",
            "due": 0,
            "method": "both",
        }

        response = self.client.patch("/reminders", reminder_edit, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], reminder_edit["title"])

        reminder_delete = {
            "id": reminder_id,
        }

        response = self.client.delete("/reminders", reminder_delete, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get("/reminders")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)
