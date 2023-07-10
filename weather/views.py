from django.utils.decorators import method_decorator
from requests import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from schoolboxauth.backend import token_auth
from weather.models import Forecast


# Create your views here.
class WeatherView(APIView):
    @method_decorator(token_auth)
    def get(self, request):
        forecast = Forecast.objects.filter().order_by("-last_updated").first()
        if not forecast:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(
            {
                "last_updated": forecast.last_updated,
                **forecast.forecast,
            },
            status=status.HTTP_200_OK,
        )
