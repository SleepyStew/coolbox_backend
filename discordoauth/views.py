import os
import time

import requests
from django.shortcuts import redirect

# Create your views here.
from django.utils.decorators import method_decorator
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from coolbox_backend.settings import DEBUG
from discordoauth.backend import get_discord_user
from discordoauth.models import DiscordOAuth
from schoolboxauth.backend import token_auth


# Create your views here.
class DiscordOAuthView(APIView):
    @method_decorator(token_auth)
    def get(self, request):
        code = request.GET.get("code")
        if not code:
            return redirect("https://schoolbox.donvale.vic.edu.au/")

        data = {
            "client_id": "999205944133177365",
            "client_secret": os.environ.get("CLIENT_SECRET"),
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": os.environ.get("APP_URL") + "/discord",
            "scope": "identify guilds.join",
        }
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        response = requests.post(
            "https://discordapp.com/api/oauth2/token", data=data, headers=headers
        )

        if response.status_code == 200:
            existing_discordoauth = DiscordOAuth.objects.filter(
                user=request.user
            ).first()
            if existing_discordoauth:
                existing_discordoauth.delete()

            discordoauth = DiscordOAuth(
                user=request.user,
                access_token=response.json()["access_token"],
                refresh_token=response.json()["refresh_token"],
                expires=time.time() + response.json()["expires_in"] - 600,
            )
            discordoauth.save()

            discord_user = get_discord_user(request.user)

            if discord_user["id"]:
                data = {"access_token": discordoauth.access_token}
                headers = {
                    "authorization": f"Bot {os.environ.get('BOT_TOKEN')}",
                }
                url = f"https://discord.com/api/guilds/999205764117835796/members/{discord_user['id']}"
                response = requests.put(url, json=data, headers=headers)

        return redirect("https://schoolbox.donvale.vic.edu.au/")

    @method_decorator(token_auth)
    def delete(self, request):
        discordoauth = DiscordOAuth.objects.filter(user=request.user).first()
        if discordoauth:
            discordoauth.delete()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)


class DiscordOAuthRedirectView(APIView):
    @method_decorator(token_auth)
    def get(self, request):
        client_id = "999205944133177365"
        scope = "identify%20guilds.join"

        if DEBUG:
            redirect_uri = "http%3A%2F%2Flocalhost%3A8000%2Fdiscord"
        else:
            redirect_uri = "https%3A%2F%2Fapi.coolbox.lol%2Fdiscord"

        return redirect(
            f"https://discord.com/oauth2/authorize?"
            f"client_id={client_id}"
            f"&redirect_uri={redirect_uri}"
            f"&response_type=code"
            f"&scope={scope}"
            f"&state={request.token}"
        )
