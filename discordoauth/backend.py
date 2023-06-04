import os
import threading
import time

import requests

from coolbox_backend.settings import DEBUG


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
        oauth.access_token = response.json()["access_token"]
        oauth.expires = time.time() + response.json()["expires_in"] - 600
        oauth.refresh_token = response.json()["refresh_token"]
        oauth.save()
        return True
    return False


def set_missing_ids():
    from discordoauth.models import DiscordOAuth

    for discordoauth in DiscordOAuth.objects.all():
        if not discordoauth.discord_id:
            print("Setting missing ID for " + str(discordoauth.user))
            discord_user = get_discord_user(discordoauth.user)
            if discord_user:
                discordoauth.discord_id = discord_user["id"]
                discordoauth.save()
            time.sleep(1)

        update_roles()


def update_roles_async():
    thread = threading.Thread(target=update_roles)
    thread.setDaemon(True)
    thread.start()


def update_roles():
    if not DEBUG:
        url = os.environ.get("DISCORD_BOT_URL") + "update_roles"
        requests.get(url)
    else:
        print("Skipping role update in debug mode...")


def refresh_tokens():
    from discordoauth.models import DiscordOAuth

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
