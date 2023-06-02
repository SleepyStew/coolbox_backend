from rest_framework import serializers

from discordoauth.models import DiscordOAuth


class DiscordOAuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiscordOAuth
        fields = ["discord_id"]
