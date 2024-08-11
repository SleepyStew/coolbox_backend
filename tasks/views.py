from django.utils.decorators import method_decorator
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from tasks.models import Task
from tasks.serializers import TaskSerializer
from schoolboxauth.backend import token_auth


# Create your views here.
class TasksView(APIView):
    @method_decorator(token_auth)
    def get(self, request):
        tasks = Task.objects.filter(author=request.user)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @method_decorator(token_auth)
    def post(self, request):
        serializer = TaskSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save(author=request.user)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @method_decorator(token_auth)
    def delete(self, request):
        if not request.data.get("id"):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        task = Task.objects.filter(id=request.data.get("id")).first()
        if task:
            if task.author != request.user:
                return Response(status=status.HTTP_401_UNAUTHORIZED)

            task.delete()
            return Response(status=status.HTTP_200_OK)

        return Response(status=status.HTTP_404_NOT_FOUND)

    @method_decorator(token_auth)
    def patch(self, request):
        if not request.data.get("id"):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        task = Task.objects.filter(id=request.data.get("id")).first()
        if task:
            if task.author != request.user:
                return Response(status=status.HTTP_401_UNAUTHORIZED)

            serializer = TaskSerializer(task, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_404_NOT_FOUND)
