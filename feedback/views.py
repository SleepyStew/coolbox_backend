import os

from discord_webhook import DiscordWebhook, DiscordEmbed
from django.utils.decorators import method_decorator
from django_ratelimit.decorators import ratelimit
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from feedback.serializers import FeedbackSerializer
from schoolboxauth.backend import token_auth
from better_profanity import profanity


profanity.load_censor_words()


# Create your views here.
class FeedbackView(APIView):
    @method_decorator(token_auth)
    @method_decorator(ratelimit(key="user", rate="2/m"))
    def post(self, request):
        serializer = FeedbackSerializer(data=request.data)

        if serializer.is_valid():
            embed = DiscordEmbed(title="CoolBox Feedback")

            embed.add_embed_field(
                name="Content",
                value=profanity.censor(serializer.data["content"]).replace(
                    "****", "\\*\\*\\*\\*"
                ),
                inline=False,
            )

            if not serializer.data["anonymous"]:
                embed.add_embed_field(
                    name="Author", value=request.user.name, inline=False
                )

            embed.add_embed_field(
                name="Origin", value=serializer.data["origin"].title(), inline=False
            )

            if serializer.data["origin"] == "test":
                webhook = DiscordWebhook(
                    url=os.environ.get("TEST_WEBHOOK_URL"),
                )
            else:
                webhook = DiscordWebhook(
                    url=os.environ.get("WEBHOOK_URL"),
                )

            webhook.add_embed(embed)
            response = webhook.execute()

            if response.status_code == 200:
                return Response(serializer.data, status=status.HTTP_200_OK)

            return Response(
                {"detail": "Failed to send webhook."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
