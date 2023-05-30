from rest_framework import serializers

from schoolboxauth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("name", "id", "year", "role", "is_active")
