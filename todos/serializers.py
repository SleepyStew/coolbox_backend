from rest_framework import serializers
from todos.models import TodoList, TodoItem


class TodoItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = TodoItem
        fields = ["content", "colour", "completed"]


class TodoListSerializer(serializers.ModelSerializer):
    items = TodoItemSerializer(many=True, read_only=True, source="todoitem_set")

    class Meta:
        model = TodoList
        fields = ["id", "title", "items", "display_id"]
