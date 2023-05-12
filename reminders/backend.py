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
            if reminder.due / 1000 < datetime.now().timestamp():
                if (
                    reminder.method in ["discord", "both"]
                    and not reminder.discord_fulfilled
                ):
                    discord_user = get_discord_user(reminder.author)
                    if discord_user:
                        url = (
                            os.environ.get("DISCORD_BOT_URL")
                            + "?id="
                            + discord_user["id"]
                            + "&name="
                            + reminder.author.name.split(" ")[0]
                            + "&title="
                            + reminder.title
                            + "&user="
                            + reminder.author.id
                            + "&due="
                            + str(reminder.due)
                        )
                        if reminder.assessment:
                            url += "&assessment=" + str(reminder.assessment)
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
