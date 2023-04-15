import json

import requests
from django.utils.decorators import method_decorator
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken
from django_ratelimit.decorators import ratelimit

from .backend import token_auth
from .models import User
from .serializers import UserSerializer


class TestView(APIView):
    @method_decorator(token_auth)
    def get(self, request):
        return Response({"detail": "Hello world."}, status=status.HTTP_200_OK)


class CustomLoginView(APIView):
    @method_decorator(ratelimit(key="header:User-Agent", rate="3/m"))
    def post(self, request, format=None):
        username = request.data.get("username")
        password = request.data.get("password")

        request_data = {"username": username.replace(" ", "."), "password": password}

        login_request = requests.post(
            "https://schoolbox.donvale.vic.edu.au/api/session",
            data=request_data,
        )

        if login_request.status_code == 400 or login_request.status_code == 401:
            return Response(
                {"detail": "Incorrect username or password."},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        elif login_request.status_code == 200:
            id = login_request.text.split('= {"id":')[1].split('"')[0][:-1]
            name = login_request.text.split(',"fullName":"')[1].split('"')[0]

            user = User.objects.filter(id=id).first()
            if user:
                user.cookie = str(login_request.cookies.get("PHPSESSID"))
                user.username = username
                user.save()
            else:
                user = User(
                    id=id, cookie=str(login_request.cookies.get("PHPSESSID")), name=name
                )
                user.save()

            access = AccessToken.for_user(user)
            print(access)

            serializer = UserSerializer(user)

            response_data = {
                "user": dict(serializer.data),
                "access": str(access),
            }

            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response(
                {"detail": "Login failed."}, status=status.HTTP_400_BAD_REQUEST
            )
