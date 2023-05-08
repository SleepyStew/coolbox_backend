from django.shortcuts import render
from django.utils.decorators import method_decorator
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from reminders.models import Reminder
from schoolboxauth.backend import token_auth
from reminders.serializers import ReminderSerializer


# Create your views here.


class RemindersView(APIView):
    @method_decorator(token_auth)
    def get(self, request):
        reminders = Reminder.objects.filter(author=request.user)
        serializer = ReminderSerializer(reminders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @method_decorator(token_auth)
    def post(self, request):
        serializer = ReminderSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save(author=request.user)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @method_decorator(token_auth)
    def delete(self, request):
        if not request.data.get("id"):
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
        reminder = Reminder.objects.filter(id=request.data.get("id")).first()
        if reminder:
            if not reminder.author == request.user:
                return Response({}, status=status.HTTP_401_UNAUTHORIZED)

            reminder.delete()
            return Response({}, status=status.HTTP_200_OK)
        else:
            return Response({}, status=status.HTTP_404_NOT_FOUND)
