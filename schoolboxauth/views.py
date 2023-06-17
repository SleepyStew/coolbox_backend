from django.utils.decorators import method_decorator
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from discordoauth.backend import get_discord_user
from schoolboxauth.backend import token_auth
from schoolboxauth.serializers import UserSerializer


class UserView(APIView):
    @method_decorator(token_auth)
    def get(self, request):
        serializer = UserSerializer(request.user)

        return Response(
            {
                **serializer.data,
                "discord": {
                    "linked": request.user.discordoauth_set.all().first() is not None,
                    "info": get_discord_user(request.user),
                },
            },
            status=status.HTTP_200_OK,
        )
