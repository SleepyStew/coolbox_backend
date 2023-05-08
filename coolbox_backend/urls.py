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

from coolbox_backend.views import IndexView
from discordoauth.views import DiscordOAuthView
from quicknotes.views import QuickNotesView
from reminders.views import RemindersView
from schoolboxauth.views import UserView, UsersView

urlpatterns = [
    path("admin", admin.site.urls),
    path("", IndexView.as_view(), name="index"),
    path("quick-notes", QuickNotesView.as_view(), name="quick_notes"),
    path("reminders", RemindersView.as_view(), name="reminders"),
    path("discord", DiscordOAuthView.as_view(), name="discord"),
    path("user", UserView.as_view(), name="user"),
    path("users", UsersView.as_view(), name="users"),
]
