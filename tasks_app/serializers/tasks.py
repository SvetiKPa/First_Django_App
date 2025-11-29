from rest_framework import serializers
from tasks_app.models import Task
from django.utils import timezone

from tasks_app.serializers.subtasks import SubTaskSerializer


class TaskListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'


class TaskDetailedSerializer(serializers.ModelSerializer):
    subtasks = SubTaskSerializer(many=True, read_only=True) #вложенный сериализатор
    class Meta:
        model = Task
        fields = [
            'id',
            'title',
            'description',
            'status',
            'deadline',
            'categories',
            'subtasks'
        ]

class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = (
            'title',
            'description',
            'status',
            'deadline'
        )

    def validate_deadline(self, value):
        time_data = timezone.make_aware(value, timezone.get_current_timezone())  # сырая дата - > форматир дата с учетом зоны
        today = timezone.now()
        if time_data < today:
            raise serializers.ValidationError(f"Deadline < {today}")
        return time_data


class TaskUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = (
            'title',
            'description',
            'status',
            'deadline'
        )
