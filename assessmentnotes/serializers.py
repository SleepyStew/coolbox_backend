from rest_framework import serializers

from assessmentnotes.models import AssessmentNote


class AssessmentNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssessmentNote
        fields = ("id", "assessment", "content")
