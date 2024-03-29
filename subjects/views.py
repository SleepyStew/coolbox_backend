from django.utils.decorators import method_decorator
from rest_framework import status
from rest_framework.views import APIView, Response

from schoolboxauth.backend import token_auth
from subjects.models import Subject
from subjects.serializers import ListSubjectSerializer, RetrieveSubjectSerializer


# Create your views here.


class SubjectView(APIView):
    @method_decorator(token_auth)
    def post(self, request):
        # serialize all data, add if it doesn't exist
        serializer_many = ListSubjectSerializer(data=request.data, many=True)
        if not serializer_many.is_valid():
            return Response(serializer_many.errors, status=status.HTTP_400_BAD_REQUEST)

        subject_objects = []

        for subject in request.data:
            serializer = ListSubjectSerializer(data=subject)
            subject_object = Subject.objects.filter(name=subject["name"]).first()
            if serializer.is_valid():
                if not subject_object:
                    serializer.save()
                    subject_objects.append(
                        Subject.objects.filter(name=subject["name"]).first()
                    )
                else:
                    subject_objects.append(subject_object)

        serializer = RetrieveSubjectSerializer(subject_objects, many=True)
        not_blank_subjects = [
            subject for subject in serializer.data if subject["pretty"] != ""
        ]
        return Response(not_blank_subjects, status=status.HTTP_200_OK)
