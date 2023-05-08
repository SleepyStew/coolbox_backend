from django.utils.decorators import method_decorator
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from discordoauth.backend import get_discord_user
from schoolboxauth.backend import token_auth
from schoolboxauth.models import User
from schoolboxauth.serializers import UserSerializer


class UserView(APIView):
    @method_decorator(token_auth)
    def get(self, request):
        return Response(
            {
                "name": request.user.name,
                "id": request.user.id,
                "discord": {
                    "linked": request.user.discordoauth_set.all().first() is not None,
                    "info": get_discord_user(request.user),
                },
            },
            status=status.HTTP_200_OK,
        )


class UsersView(APIView):
    @method_decorator(token_auth)
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(
            {"count": users.count(), "details": serializer.data},
            status=status.HTTP_200_OK,
        )
