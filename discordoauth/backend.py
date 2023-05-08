import os
import threading
import time

import requests

from discordoauth.models import DiscordOAuth


def get_discord_user(user):
    discordoauth = user.discordoauth_set.first()
    if not discordoauth:
        return None
    discord_user = requests.get(
        "https://discordapp.com/api/users/@me",
        headers={"Authorization": "Bearer " + discordoauth.access_token},
    )
    if discord_user.status_code == 200:
        return discord_user.json()
    return None


def refresh_token(oauth):
    data = {
        "client_id": "999205944133177365",
        "client_secret": os.environ.get("CLIENT_SECRET"),
        "grant_type": "refresh_token",
        "refresh_token": oauth.refresh_token,
        "scope": "identify",
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post(
        "https://discordapp.com/api/oauth2/token", data=data, headers=headers
    )
    if response.status_code == 200:
        print(response.json())
        oauth.access_token = response.json()["access_token"]
        oauth.expires = time.time() + response.json()["expires_in"] - 600
        oauth.refresh_token = response.json()["refresh_token"]
        oauth.save()
        return True
    return False


def refresh_tokens():
    while True:
        time.sleep(60)
        for discordoauth in DiscordOAuth.objects.all():
            if time.time() > discordoauth.expires:
                if refresh_token(discordoauth):
                    print(
                        "Refreshed token for "
                        + get_discord_user(discordoauth.user)["username"]
                        + "#"
                        + get_discord_user(discordoauth.user)["discriminator"]
                    )
                else:
                    print("Failed to refresh token for " + str(discordoauth.user))
                    discordoauth.delete()


thread = threading.Thread(target=refresh_tokens)
thread.setDaemon(True)
thread.start()
