from rest_framework import status
from rest_framework.test import APITestCase

from coolbox_backend.tests import authenticated_test_client


class UserViewTestCase(APITestCase):
    def setUp(self):
        self.client = authenticated_test_client()

    def test_user_view(self):
        response = self.client.get("/user")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(type(response.data["discord"]["linked"]), bool)


# TODO: Add more tests for authenticated
