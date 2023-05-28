from rest_framework import status
from rest_framework.test import APITestCase

from coolbox_backend.tests import authenticated_test_client
from discordoauth.models import DiscordOAuth


class DiscordViewTestCase(APITestCase):
    def setUp(self):
        self.client = authenticated_test_client()

    def test_discord_view(self):

        response = self.client.delete("/discord")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        response = self.client.get("/discord")

        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

        discordoauth_object = DiscordOAuth(
            user=self.client.user,
            access_token="test_access_token",
            refresh_token="test_refresh_token",
            expires=0,
        )
        discordoauth_object.save()

        response = self.client.delete("/discord")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
