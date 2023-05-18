from rest_framework import serializers

from subjects.models import Subject


class ListSubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ["name"]


class RetrieveSubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ["name", "pretty"]
