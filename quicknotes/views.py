from django.utils.decorators import method_decorator
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from quicknotes.models import QuickNote
from quicknotes.serializers import QuickNoteSerializer
from schoolboxauth.backend import token_auth


# Create your views here.
class QuickNotesView(APIView):
    @method_decorator(token_auth)
    def get(self, request):
        quick_notes = QuickNote.objects.filter(author=request.user).order_by(
            "display_id"
        )
        serializer = QuickNoteSerializer(quick_notes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @method_decorator(token_auth)
    def put(self, request):
        serializer = QuickNoteSerializer(data=request.data, many=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        current_notes = list(QuickNote.objects.filter(author=request.user).all())
        QuickNote.objects.filter(author=request.user).delete()

        try:
            for index, quick_note in enumerate(request.data):
                serializer = QuickNoteSerializer(data=quick_note)
                if serializer.is_valid():
                    serializer.save(author=request.user, display_id=index)

        # If there is an error, restore the previous notes
        except:
            for quick_note in current_notes:
                quick_note.save()

            return Response(
                {"restored": True}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        new_notes = QuickNote.objects.filter(author=request.user)
        new_serializer = QuickNoteSerializer(new_notes, many=True)

        return Response(new_serializer.data, status=status.HTTP_200_OK)
