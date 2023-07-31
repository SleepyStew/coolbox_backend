# Create your views here.
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from django.shortcuts import redirect

from reminders.views import RemindersView
from roomchanges.views import RoomChangesView
from schoolboxauth.backend import token_auth
from schoolboxauth.views import UserView
from rest_framework.response import Response

from stats.views import MessageView
from weather.views import WeatherView


# Create your views here.
class IndexView(APIView):
    def get(self, request):
        return redirect("https://github.com/SleepyStew/coolbox_backend")


class StartView(APIView):
    @method_decorator(token_auth)
    def get(self, request):
        requests = {
            "user": UserView.as_view()(request._request),
            "status": MessageView.as_view()(request._request),
            "reminders": RemindersView.as_view()(request._request),
            "weather": WeatherView.as_view()(request._request),
            "room_changes": RoomChangesView.as_view()(request._request),
        }
        return Response(
            {
                "status_codes": {
                    request: requests[request].status_code for request in requests
                },
                **{request: requests[request].data for request in requests},
            }
        )
