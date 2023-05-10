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
                if (
                    reminder.method in ["discord", "both"]
                    and not reminder.discord_fulfilled
                ):
                    discord_user = get_discord_user(reminder.author)
                    if discord_user:
                        url = (
                            os.environ.get("DISCORD_BOT_URL")
                            + "?user="
                            + discord_user["id"]
                            + "&name="
                            + reminder.author.name.split(" ")[0]
                            + "&title="
                            + reminder.title
                            + "&description=No Description"
                        )
                        requests.get(url)
                        reminder.discord_fulfilled = True
                        reminder.save()
                        print(
                            "Discord Reminder: "
                            + reminder.title
                            + " has been fulfilled."
                        )

                if reminder.method == "discord":
                    reminder.delete()
