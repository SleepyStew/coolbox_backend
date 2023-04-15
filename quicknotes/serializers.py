from rest_framework import serializers

from quicknotes.models import QuickNote


class QuickNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuickNote
        fields = (
            "title",
            "content",
        )
