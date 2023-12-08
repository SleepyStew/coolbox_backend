from rest_framework import serializers

from dailymessages.models import DailyVerse


class DailyVerseSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyVerse
        fields = ["content", "reference", "link"]
