import copy

from django.utils.decorators import method_decorator
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from schoolboxauth.backend import token_auth
from todos.models import TodoList, TodoItem
from todos.serializers import TodoListSerializer, TodoItemSerializer


# Create your views here.
class TodoListView(APIView):
    @method_decorator(token_auth)
    def get(self, request):
        todos = TodoList.objects.filter(author=request.user)
        serializer = TodoListSerializer(todos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @method_decorator(token_auth)
    def post(self, request):
        serializer = TodoListSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save(author=request.user)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @method_decorator(token_auth)
    def delete(self, request):
        if not request.data.get("id"):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        todo = TodoList.objects.filter(id=request.data.get("id")).first()
        if todo:
            if todo.author != request.user:
                return Response(status=status.HTTP_401_UNAUTHORIZED)

            todo.delete()
            return Response(status=status.HTTP_200_OK)

        return Response(status=status.HTTP_404_NOT_FOUND)

    @method_decorator(token_auth)
    def patch(self, request):
        if not request.data.get("id"):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        todo = TodoList.objects.filter(id=request.data.get("id")).first()
        if todo:
            if todo.author != request.user:
                return Response(status=status.HTTP_401_UNAUTHORIZED)

            serializer = TodoListSerializer(todo, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_404_NOT_FOUND)

    @method_decorator(token_auth)
    def put(self, request):
        if not request.data.get("id"):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        todo = TodoList.objects.filter(id=request.data.get("id")).first()

        if todo:
            if todo.author != request.user:
                return Response(status=status.HTTP_401_UNAUTHORIZED)

            current_items = list(TodoItem.objects.filter(list=todo).all())
            TodoItem.objects.filter(list=todo).delete()

            try:
                for index, item in enumerate(request.data.get("items")):
                    serializer = TodoItemSerializer(data=item)
                    if serializer.is_valid():
                        serializer.save(list=todo, display_id=index)
                    else:
                        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            except Exception as e:
                for item in current_items:
                    print("saving")
                    item.save()

                print(e)

                return Response(
                    {"restored": True}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

            todo = TodoList.objects.filter(id=request.data.get("id")).first()
            serializer = TodoListSerializer(todo)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(status=status.HTTP_404_NOT_FOUND)
