from django.db import models


# Create your models here.
class DailyVerse(models.Model):
    content = models.TextField()
    reference = models.CharField(max_length=128)
    link = models.CharField(max_length=256)
    date = models.DateField(auto_now_add=True)
