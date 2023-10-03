import os

import requests
from discord_webhook import DiscordWebhook, DiscordEmbed
from django.utils.decorators import method_decorator
from django_ratelimit.decorators import ratelimit
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from feedback.serializers import FeedbackSerializer
from schoolboxauth.backend import token_auth
from urllib.parse import quote


# Create your views here.
class FeedbackView(APIView):
    @method_decorator(token_auth)
    @method_decorator(ratelimit(key="user", rate="6/h"))
    def post(self, request):
        serializer = FeedbackSerializer(data=request.data)

        if serializer.is_valid():
            # To prevent abuse, feedback must be logged to some extent
            print(f"Feedback: {request.user.name} - {serializer.data['content']}")

            if request.user.feedback_disabled:
                return Response(
                    {"detail": "You are not allowed to submit feedback."},
                    status=status.HTTP_403_FORBIDDEN,
                )

            embed = DiscordEmbed(title="CoolBox Feedback")

            filter_request = requests.get(
                "https://www.purgomalum.com/service/json?text="
                + quote(serializer.data["content"])
                + "&fill_char=*"
            )

            if filter_request.status_code != 200 or not filter_request.json().get(
                "result"
            ):
                return Response(
                    {"detail": "Failed to filter text."},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

            embed.add_embed_field(
                name="Content",
                value=filter_request.json()["result"].replace("*", "\\*"),
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
