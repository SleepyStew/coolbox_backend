from django.utils.decorators import method_decorator
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from quicknotes.models import QuickNote
from quicknotes.serializers import QuickNoteSerializer
from schoolboxauth.backend import token_auth
from schoolboxauth.models import User


# Create your views here.
class QuickNotesView(APIView):
    @method_decorator(token_auth)
    def get(self, request):
        user = User.from_token(request)
        if user:
            quick_notes = QuickNote.objects.filter(author=user).order_by("display_id")
            serializer = QuickNoteSerializer(quick_notes, many=True)
            for index, quick_note in enumerate(serializer.data):
                quick_note["id"] = index
            return Response(serializer.data, status=status.HTTP_200_OK)

    @method_decorator(token_auth)
    def post(self, request):
        user = User.from_token(request)
        if user:
            quick_notes = request.data.get("quick_notes")
            serializer = QuickNoteSerializer(data=quick_notes, many=True)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            current_notes = QuickNote.objects.filter(author=user)

            try:
                for quick_note in QuickNote.objects.filter(author=user):
                    quick_note.delete()

                for index, quick_note in enumerate(quick_notes):
                    serializer = QuickNoteSerializer(data=quick_note)
                    if serializer.is_valid():
                        serializer.save(author=user, display_id=index)
            except:
                # If there is an error, restore the previous notes
                for quick_note in current_notes:
                    quick_note.save()
                return Response({}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response({}, status=status.HTTP_200_OK)
