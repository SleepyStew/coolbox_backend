from django.shortcuts import render
from django.utils.decorators import method_decorator
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from dailymessages.models import DailyVerse
from dailymessages.serializers import DailyVerseSerializer
from schoolboxauth.backend import token_auth


# Create your views here.
class DailyVerseView(APIView):
    @method_decorator(token_auth)
    def get(self, request):
        daily_verse = DailyVerse.objects.filter().first()
        if not daily_verse:
            return Response(
                {"error": "No daily verse found"}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = DailyVerseSerializer(daily_verse)
        return Response(serializer.data, status=status.HTTP_200_OK)
