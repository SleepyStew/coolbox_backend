from rest_framework import status
from rest_framework.test import APITestCase

from coolbox_backend.tests import authenticated_test_client


class ErrorReportViewTestCase(APITestCase):
    def setUp(self):
        self.client = authenticated_test_client()

    def test_subject_view(self):
        error_report_endpoint = "/error-report"

        error = {
            "error": "Test",
            "detail": "Detail",
        }

        response = self.client.post(error_report_endpoint, error, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["error"], error["error"])
        self.assertEqual(response.data["detail"], error["detail"])
