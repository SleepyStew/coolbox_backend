from django.db import models


# Create your models here.
class QuickNote(models.Model):
    title = models.CharField(max_length=255, blank=True)
    content = models.TextField(blank=True)
    display_id = models.IntegerField()
    author = models.ForeignKey("schoolboxauth.User", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def __repr__(self):
        return self.title
