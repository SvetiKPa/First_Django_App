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

class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = (
            'title',
            'description',
            'status',
            'deadline'
        )

# class TaskUpdateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Task
#         fields = (
#             'title',
#             'description',
#             'status',
#             'deadline'
#         )
