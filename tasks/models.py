from django.db import models

# Create your models here.


class Task(models.Model):
    title = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey("schoolboxauth.User", on_delete=models.CASCADE)
    content = models.TextField(null=True)
    type = models.CharField(max_length=128)
    due = models.DateTimeField()
