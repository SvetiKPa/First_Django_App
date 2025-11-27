from rest_framework import serializers
from tasks_app.models import Task


class TaskListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'


class TaskDetailedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'