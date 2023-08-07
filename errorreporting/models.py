from django.db import models


# Create your models here.
class ErrorReport(models.Model):
    author = models.ForeignKey(
        "schoolboxauth.User", on_delete=models.CASCADE, null=True
    )
    error = models.TextField()
    detail = models.TextField(blank=True)

    def __str__(self):
        return self.error

    def __repr__(self):
        return self.error
