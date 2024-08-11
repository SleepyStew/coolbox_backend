from django.db import models


# Create your models here.
class TodoList(models.Model):
    title = models.CharField(max_length=128)
    author = models.ForeignKey("schoolboxauth.User", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class TodoItem(models.Model):
    content = models.TextField(blank=True)
    list = models.ForeignKey(TodoList, on_delete=models.CASCADE)
    colour = models.CharField(max_length=7, null=True)
    display_id = models.IntegerField()
