import uptime
from rest_framework import status
from rest_framework.views import APIView, Response

from schoolboxauth.models import User


# Create your views here.


class RunningView(APIView):
    def get(self, request):
        return Response(
            {"uptime": uptime.uptime()},
            status=status.HTTP_200_OK,
        )


class UserCountView(APIView):
    def get(self, request):
        user_count = User.objects.count()
        return Response({"count": user_count}, status=status.HTTP_200_OK)
