from rest_framework import status
from rest_framework.test import APITestCase

from coolbox_backend.tests import authenticated_test_client


class TaskViewTestCase(APITestCase):
    def setUp(self):
        self.client = authenticated_test_client()

    def test_subject_view(self):
        tasks_endpoint = "/tasks"

        response = self.client.get(tasks_endpoint)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

        task = {
            "title": "Test Task",
            "due": "2013-01-29T12:34:56.000000Z",
            "type": "assessment",
        }

        response = self.client.post(tasks_endpoint, task, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], task["title"])
        # Date format changes when saved to the database
        # self.assertEqual(response.data["due"], task["due"])
        self.assertEqual(response.data["type"], task["type"])

        response = self.client.get(tasks_endpoint)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        task_id = response.data[0]["id"]

        task_edit = {
            "id": task_id,
            "title": "Test Reminder",
            "due": "2013-01-29T12:34:56.000000Z",
            "type": "homework",
            "subject": "Test Subject",
        }

        response = self.client.patch(tasks_endpoint, task_edit, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["type"], task_edit["type"])
        self.assertEqual(response.data["subject"], task_edit["subject"])

        task_delete = {
            "id": task_id,
        }

        response = self.client.delete(tasks_endpoint, task_delete, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get(tasks_endpoint)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)
