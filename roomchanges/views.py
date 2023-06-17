from django.utils.decorators import method_decorator
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from roomchanges import backend
from schoolboxauth.backend import token_auth


# Create your views here.
class RoomChangesView(APIView):
    @method_decorator(token_auth)
    def get(self, request):
        # For debugging production environment
        print(backend.day(), backend.last_updated)
        return Response(
            {
                "room_changes": backend.data
                if backend.day() == backend.last_updated
                else []
            },
            status=status.HTTP_200_OK,
        )
