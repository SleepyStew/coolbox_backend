from rest_framework import status
from rest_framework.test import APITestCase

from coolbox_backend.tests import authenticated_test_client


class ErrorReportViewTestCase(APITestCase):
    def setUp(self):
        self.client = authenticated_test_client()

    def test_subject_view(self):
        error_report_endpoint = "/error-report"

        errors = [
            {
                "error": "Test",
                "detail": "Detail",
            },
            {
                "error": "Test2",
                "detail": "Detail2",
            },
        ]

        response = self.client.post(error_report_endpoint, errors, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["error"], errors[0]["error"])
        self.assertEqual(response.data[1]["detail"], errors[1]["detail"])
