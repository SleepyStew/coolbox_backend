from rest_framework import status
from rest_framework.test import APITestCase

from coolbox_backend.tests import authenticated_test_client


class QuickNoteViewTestCase(APITestCase):
    def setUp(self):
        self.client = authenticated_test_client()

    def test_quicknote_view(self):
        quick_notes_endpoint = "/quick-notes"

        response = self.client.get(quick_notes_endpoint)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

        self.quicknote_data = [
            {"title": "Test QuickNote 1", "content": "This is a test quicknote"},
            {"title": "Test QuickNote 2", "content": "This is a second test quicknote"},
        ]

        response = self.client.put(quick_notes_endpoint, self.quicknote_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), len(self.quicknote_data))

        response = self.client.get(quick_notes_endpoint)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
