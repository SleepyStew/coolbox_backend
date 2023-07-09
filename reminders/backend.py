import os
import time
from datetime import datetime
from urllib.parse import quote

import requests


def reminder_check():
    from discordoauth.backend import get_discord_user
    from reminders.models import Reminder

    while True:
        time.sleep(10)
        for reminder in Reminder.objects.all():
            if reminder.due / 1000 > datetime.now().timestamp():
                continue

            reminder.delete()

            if reminder.method in ["discord", "both"]:
                discord_user = get_discord_user(reminder.author)

                if not discord_user:
                    continue

                url = (
                    os.environ.get("DISCORD_BOT_URL")
                    + "?id="
                    + discord_user["id"]
                    + "&name="
                    + reminder.author.name.split(" ")[0]
                    + "&title="
                    + quote(reminder.title)
                    + "&user="
                    + reminder.author.id
                    + "&due="
                    + str(reminder.due)
                )

                if reminder.assessment:
                    url += "&assessment=" + str(reminder.assessment)

                requests.get(url)

                print(f"Discord Reminder: {reminder.title} has been fulfilled.")
