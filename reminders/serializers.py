from rest_framework import serializers

from reminders.models import Reminder


class ReminderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reminder
        fields = (
            "title",
            "method",
            "due",
            "assessment"
        )