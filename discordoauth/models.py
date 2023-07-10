from django.db import models


# Create your models here.
class DiscordOAuth(models.Model):
    user = models.ForeignKey("schoolboxauth.User", on_delete=models.CASCADE)
    access_token = models.CharField(max_length=64)
    refresh_token = models.CharField(max_length=64)
    discord_id = models.BigIntegerField(null=True)
    expires = models.BigIntegerField()

    def __str__(self):
        return self.user.name

    def __repr__(self):
        return self.user.name
