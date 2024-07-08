from django.db import models


# Create your models here.
class AssessmentNote(models.Model):
    assessment = models.IntegerField()
    author = models.ForeignKey("schoolboxauth.User", on_delete=models.CASCADE)
    content = models.TextField()
