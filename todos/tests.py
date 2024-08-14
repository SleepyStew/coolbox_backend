from rest_framework import status
from rest_framework.test import APITestCase

from coolbox_backend.tests import authenticated_test_client


class TodoViewTestCase(APITestCase):
    def setUp(self):
        self.client = authenticated_test_client()

    def test_todo_view(self):
        todos_endpoint = "/todos"

        response = self.client.get(todos_endpoint)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

        todo = {"title": "Test Todo"}

        response = self.client.post(todos_endpoint, todo, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Test Todo")
        self.assertEqual(len(response.data["items"]), 0)

        todo_change = {"id": response.data["id"], "title": "Test Todo Changed"}

        response = self.client.patch(todos_endpoint, todo_change, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Test Todo Changed")

        todo_items = {
            "id": response.data["id"],
            "items": [{"content": "Test Item"}, {"content": "Test Item 2"}],
        }

        response = self.client.put(todos_endpoint, todo_items, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["items"]), 2)
        self.assertEqual(response.data["items"][0]["content"], "Test Item")
        self.assertEqual(response.data["items"][1]["content"], "Test Item 2")

        delete_todo = {"id": response.data["id"]}

        response = self.client.delete(todos_endpoint, delete_todo, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get(todos_endpoint)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)
