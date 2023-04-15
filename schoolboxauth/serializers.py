from rest_framework import serializers

from schoolboxauth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "name",
            "date_joined",
            "last_login",
            "is_staff",
            "is_active",
        )
