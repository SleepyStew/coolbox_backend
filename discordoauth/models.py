from django.db import models

# Create your models here.
class DiscordOAuth(models.Model):
    user = models.ForeignKey('schoolboxauth.User', on_delete=models.CASCADE)
    access_token = models.CharField(max_length=64)
    refresh_token = models.CharField(max_length=64)
    expires = models.IntegerField()
