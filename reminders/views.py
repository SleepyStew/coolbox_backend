from django.utils.decorators import method_decorator
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from reminders.models import Reminder
from reminders.serializers import ReminderSerializer
from schoolboxauth.backend import token_auth, internal_auth
from schoolboxauth.models import User


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
            return Response(status=status.HTTP_400_BAD_REQUEST)
        reminder = Reminder.objects.filter(id=request.data.get("id")).first()
        if reminder:
            if reminder.author != request.user:
                return Response(status=status.HTTP_401_UNAUTHORIZED)

            reminder.delete()
            return Response(status=status.HTTP_200_OK)

        return Response(status=status.HTTP_404_NOT_FOUND)

    @method_decorator(token_auth)
    def patch(self, request):
        if not request.data.get("id"):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        reminder = Reminder.objects.filter(id=request.data.get("id")).first()
        if reminder:
            if reminder.author != request.user:
                return Response(status=status.HTTP_401_UNAUTHORIZED)

            serializer = ReminderSerializer(reminder, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_404_NOT_FOUND)


class RemindersRescheduleView(APIView):
    @method_decorator(internal_auth)
    def post(self, request):
        serializer = ReminderSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        if not request.data.get("user"):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(id=request.data.get("user")).first()

        if not user:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer.save(author=user)

        return Response(serializer.data, status=status.HTTP_200_OK)
