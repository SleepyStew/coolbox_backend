import os

import uptime
from django.utils import timezone
from django.utils.decorators import method_decorator
from django_ratelimit.decorators import ratelimit
from rest_framework import status
from rest_framework.views import APIView, Response

from coolbox_backend.settings import BASE_DIR
from schoolboxauth.backend import token_auth
from schoolboxauth.models import User


# Create your views here.


class RunningView(APIView):
    @method_decorator(ratelimit(key="ip", rate="5/3s"))
    def get(self, request):
        return Response(
            {"uptime": uptime.uptime()},
            status=status.HTTP_200_OK,
        )


class UserCountView(APIView):
    @method_decorator(ratelimit(key="ip", rate="5/3s"))
    def get(self, request):
        user_count = User.objects.count()
        # last_login within 5 days
        active_user_count = User.objects.filter(
            last_login__gte=timezone.now() - timezone.timedelta(days=5)
        ).count()

        return Response(
            {"count": user_count, "active": active_user_count},
            status=status.HTTP_200_OK,
        )


class MessageView(APIView):
    @method_decorator(token_auth)
    def get(self, request):
        # "message" to be deprecated
        status_types = ["info", "critical", "message"]
        status_lookup = {}
        for status_type in status_types:
            with open(
                os.path.join(BASE_DIR, f"status_{status_type}"), "r"
            ) as status_file:
                content = status_file.read().strip()
                status_lookup[status_type] = content if content else None
        return Response(status_lookup, status=status.HTTP_200_OK)
