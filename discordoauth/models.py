from django.db import models


# Create your models here.
class DiscordOAuth(models.Model):
    user = models.ForeignKey("schoolboxauth.User", on_delete=models.CASCADE)
    access_token = models.CharField(max_length=64)
    refresh_token = models.CharField(max_length=64)
    discord_id = models.IntegerField(null=True)
    expires = models.IntegerField()

    def __str__(self):
        return self.user

    def __repr__(self):
        return self.user
