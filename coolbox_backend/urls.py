"""
URL configuration for coolbox_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView
from django_ratelimit.exceptions import Ratelimited
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler

from coolbox_backend.views import IndexView, StartView
from discordoauth.views import (
    DiscordOAuthView,
    DiscordOAuthRedirectView,
    DiscordOAuthUsersView,
)
from feedback.views import FeedbackView
from quicknotes.views import QuickNotesView
from reminders.views import RemindersView, RemindersRescheduleView
from roomchanges.views import RoomChangesView
from schoolboxauth.views import UserView
from stats.views import RunningView, UserCountView, MessageView
from subjects.views import SubjectView
from weather.views import WeatherView

urlpatterns = [
    path("cba", admin.site.urls),
    path("", IndexView.as_view(), name="index"),
    path("quick-notes", QuickNotesView.as_view(), name="quick_notes"),
    path("reminders", RemindersView.as_view(), name="reminders"),
    path(
        "reminders/reschedule",
        RemindersRescheduleView.as_view(),
        name="reminders_reschedule",
    ),
    path("discord", DiscordOAuthView.as_view(), name="discord"),
    path("discord/users", DiscordOAuthUsersView.as_view(), name="discord_users"),
    path(
        "discord/redirect", DiscordOAuthRedirectView.as_view(), name="discord_redirect"
    ),
    path("user", UserView.as_view(), name="user"),
    path("stats/running", RunningView.as_view(), name="running"),
    path("stats/user_count", UserCountView.as_view(), name="user_count"),
    path("stats/message", MessageView.as_view(), name="status_message"),
    path("subjects", SubjectView.as_view(), name="subjects"),
    path("feedback", FeedbackView.as_view(), name="feedback"),
    path("room-changes", RoomChangesView.as_view(), name="room-changes"),
    path("weather", WeatherView.as_view(), name="weather"),
    path("start", StartView.as_view(), name="start"),
    path(
        "robots.txt",
        TemplateView.as_view(template_name="robots.txt", content_type="text/plain"),
        name="robots",
    ),
]


def ratelimit_error_handler(exc, context):
    response = exception_handler(exc, context)

    if isinstance(exc, Ratelimited):
        return Response(
            {"detail": "You are being rate-limited. Please try again later."},
            status=status.HTTP_429_TOO_MANY_REQUESTS,
        )

    return response
