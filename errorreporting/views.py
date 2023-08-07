from django.utils.decorators import method_decorator
from rest_framework import status
from rest_framework.views import APIView, Response

from errorreporting.serializer import ErrorReportSerializer
from schoolboxauth.backend import token_auth


# Create your views here.
class ErrorReportView(APIView):
    @method_decorator(token_auth)
    def post(self, request):
        serializer = ErrorReportSerializer(data=request.data, many=True)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save(author=request.user)

        return Response(serializer.data, status=status.HTTP_200_OK)
