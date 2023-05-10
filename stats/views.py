import uptime
from rest_framework import status
from rest_framework.views import APIView, Response


# Create your views here.


class RunningView(APIView):
    def get(self, request):
        return Response(
            {"uptime": uptime.uptime()},
            status=status.HTTP_200_OK,
        )
