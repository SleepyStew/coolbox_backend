from django.db import models


class RoomChange(models.Model):
    class_name = models.CharField(max_length=255)
    timetabled_room = models.CharField(max_length=255)
    assigned_room = models.CharField(max_length=255)
    last_updated = models.DateField(auto_now_add=True)
