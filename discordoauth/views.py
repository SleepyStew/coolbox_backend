import os
import time

import requests
from django.shortcuts import redirect

# Create your views here.
from django.utils.decorators import method_decorator
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

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
            "scope": "identify",
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

        return redirect("https://schoolbox.donvale.vic.edu.au/")

    @method_decorator(token_auth)
    def delete(self, request):
        discordoauth = DiscordOAuth.objects.filter(user=request.user).first()
        if discordoauth:
            discordoauth.delete()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)
