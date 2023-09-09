import os

from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()
if os.environ.get("RUN_MAIN", None) != "true":
    scheduler.start()
