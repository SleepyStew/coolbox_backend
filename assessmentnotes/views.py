from django.utils.decorators import method_decorator
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from assessmentnotes.models import AssessmentNote
from assessmentnotes.serializers import AssessmentNoteSerializer
from schoolboxauth.backend import token_auth


# Create your views here.
class AssessmentNotesView(APIView):
    @method_decorator(token_auth)
    def get(self, request):
        assessment_notes = AssessmentNote.objects.filter(author=request.user)
        serializer = AssessmentNoteSerializer(assessment_notes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @method_decorator(token_auth)
    def post(self, request):
        serializer = AssessmentNoteSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save(author=request.user)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @method_decorator(token_auth)
    def delete(self, request):
        if not request.data.get("id"):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        assessment_note = AssessmentNote.objects.filter(id=request.data.get("id")).first()
        if assessment_note:
            if assessment_note.author != request.user:
                return Response(status=status.HTTP_401_UNAUTHORIZED)

            assessment_note.delete()
            return Response(status=status.HTTP_200_OK)

        return Response(status=status.HTTP_404_NOT_FOUND)

    @method_decorator(token_auth)
    def patch(self, request):
        if not request.data.get("id"):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        assessment_note = AssessmentNote.objects.filter(id=request.data.get("id")).first()
        if assessment_note:
            if assessment_note.author != request.user:
                return Response(status=status.HTTP_401_UNAUTHORIZED)

            serializer = AssessmentNoteSerializer(
                assessment_note, data=request.data, partial=True
            )
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_404_NOT_FOUND)
