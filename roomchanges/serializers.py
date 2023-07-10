from rest_framework import serializers

from roomchanges.models import RoomChange


class RoomChangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomChange
        fields = ("class_name", "timetabled_room", "assigned_room")
