from rest_framework import status
from rest_framework.test import APITestCase

from coolbox_backend.tests import authenticated_test_client


class SubjectViewTestCase(APITestCase):
    def setUp(self):
        self.client = authenticated_test_client()

    def test_subject_view(self):
        self.subject_data = [
            {"name": "Math"},
            {"name": "Science"},
            {"name": "History"},
        ]

        response = self.client.post("/subjects", self.subject_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)
