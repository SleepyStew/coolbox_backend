from django.db import models

# Create your models here.
class Reminder(models.Model):
    title = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey('schoolboxauth.User', on_delete=models.CASCADE)
    method = models.CharField(max_length=16)
    assessment = models.IntegerField(null=True)
    due = models.IntegerField()
