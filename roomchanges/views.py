from django.utils.decorators import method_decorator
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from roomchanges import backend
from roomchanges.models import RoomChange
from roomchanges.serializers import RoomChangeSerializer
from schoolboxauth.backend import token_auth


# Create your views here.
class RoomChangesView(APIView):
    @method_decorator(token_auth)
    def get(self, request):
        room_changes = RoomChange.objects.all()
        serializer = RoomChangeSerializer(room_changes, many=True)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )
