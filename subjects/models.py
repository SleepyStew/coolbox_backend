from django.db import models


# Create your models here.
class Subject(models.Model):
    name = models.CharField(max_length=128)
    pretty = models.CharField(max_length=128, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
