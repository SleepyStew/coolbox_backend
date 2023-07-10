from django.db import models


class Forecast(models.Model):
    forecast = models.JSONField()
    last_updated = models.DateTimeField(auto_now_add=True)
