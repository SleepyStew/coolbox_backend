from rest_framework import serializers


class FeedbackSerializer(serializers.Serializer):
    content = serializers.CharField(max_length=2048, allow_blank=False)
    origin = serializers.CharField(max_length=64, allow_blank=False)
    anonymous = serializers.BooleanField(default=False)

    def validate_origin(self, value):
        # More origins soon
        if value not in ["schoolbox", "test"]:
            raise serializers.ValidationError("Invalid origin.")
        return value
