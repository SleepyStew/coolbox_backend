from rest_framework import serializers

from errorreporting.models import ErrorReport


class ErrorReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = ErrorReport
        fields = ("error", "detail")
