from rest_framework import serializers
from todos.models import TodoList, TodoItem


class TodoItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = TodoItem
        fields = ['content', 'colour']


class TodoListSerializer(serializers.ModelSerializer):
    items = TodoItemSerializer(many=True, read_only=True, source='todoitem_set')

    class Meta:
        model = TodoList
        fields = ['id', 'title', 'items']
