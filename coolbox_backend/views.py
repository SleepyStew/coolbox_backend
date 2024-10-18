# Create your views here.

from django.shortcuts import redirect
from rest_framework.response import Response
from rest_framework.views import APIView

from dailymessages.views import DailyVerseView
from reminders.views import RemindersView
from roomchanges.views import RoomChangesView
from schoolboxauth.views import UserView
from stats.views import MessageView
from tasks.views import TasksView
from weather.views import WeatherView


# Create your views here.
class IndexView(APIView):
    def get(self, request):
        return redirect("https://github.com/SleepyStew/coolbox_backend")


def create_requests(request_template, requests):
    return_requests = {}
    endpoint_request = request_template._request

    for endpoint, view in requests.items():
        endpoint_request.path = "/" + endpoint
        return_requests[endpoint] = view(endpoint_request)

    return return_requests


class StartView(APIView):
    def get(self, request):
        requests = create_requests(
            request,
            {
                "user": UserView.as_view(),
                "status": MessageView.as_view(),
                "reminders": RemindersView.as_view(),
                "weather": WeatherView.as_view(),
                "room_changes": RoomChangesView.as_view(),
                "daily_verse": DailyVerseView.as_view(),
                "tasks": TasksView.as_view(),
            },
        )
        return Response(
            {
                "status_codes": {
                    request: requests[request].status_code for request in requests
                },
                **{request: requests[request].data for request in requests},
            }
        )
