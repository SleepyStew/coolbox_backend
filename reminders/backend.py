import os
import time
from datetime import datetime

import requests


def reminder_check():
    from discordoauth.backend import get_discord_user
    from reminders.models import Reminder

    while True:
        time.sleep(10)
        for reminder in Reminder.objects.all():
            if reminder.due < datetime.now().timestamp():
                if reminder.method in ["discord", "both"]:
                    discord_user = get_discord_user(reminder.author)
                    print(discord_user)
                    if discord_user:
                        url = (os.environ.get("DISCORD_BOT_URL")
                               + "?user="
                               + discord_user["id"]
                               + "&name="
                               + reminder.author.name.split(" ")[0]
                               + "&title="
                               + reminder.title
                               + "&description=No Description")
                        requests.get(url)
                print("Reminder: " + reminder.title + " has been fulfilled.")
                reminder.delete()
