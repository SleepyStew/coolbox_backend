from rest_framework import status
from rest_framework.test import APITestCase

from coolbox_backend.tests import authenticated_test_client


class AssessmentNoteViewTestCase(APITestCase):
    def setUp(self):
        self.client = authenticated_test_client()

    def test_subject_view(self):
        assessment_notes_endpoint = "/assessment-notes"

        response = self.client.get(assessment_notes_endpoint)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

        assessment_note = {
            "content": "Test Assessment Note",
            "assessment": 12345678,
        }

        response = self.client.post(assessment_notes_endpoint, assessment_note, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["content"], assessment_note["content"])
        self.assertEqual(response.data["assessment"], assessment_note["assessment"])

        response = self.client.get(assessment_notes_endpoint)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        assessment_note_id = response.data[0]["id"]

        assessment_note_edit = {
            "id": assessment_note_id,
            "content": "Test Assessment Note Change"
        }

        response = self.client.patch(assessment_notes_endpoint, assessment_note_edit, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["content"], assessment_note_edit["content"])

        assessment_note_delete = {
            "id": assessment_note_id,
        }

        response = self.client.delete(
            assessment_notes_endpoint, assessment_note_delete, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get(assessment_notes_endpoint)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)
