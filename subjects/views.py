from django.shortcuts import render
from django.utils.decorators import method_decorator
from rest_framework import status
from rest_framework.views import APIView, Response

from schoolboxauth.backend import token_auth
from subjects.models import Subject
from subjects.serializers import ListSubjectSerializer, RetrieveSubjectSerializer


# Create your views here.


class SubjectView(APIView):
    @method_decorator(token_auth)
    def get(self, request):
        serializer = ListSubjectSerializer(data=request.data, many=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        subject_objects = [
            Subject.objects.get(name=subject["name"]) for subject in request.data
        ]

        serializer = RetrieveSubjectSerializer(subject_objects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @method_decorator(token_auth)
    def post(self, request):
        # serialize all data, add if it doesn't exist
        serializer = ListSubjectSerializer(data=request.data, many=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        for subject in request.data:
            serializer = ListSubjectSerializer(data=subject)
            if serializer.is_valid():
                if not Subject.objects.filter(name=subject["name"]).exists():
                    serializer.save()

        return Response(status=status.HTTP_200_OK)
