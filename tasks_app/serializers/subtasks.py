from rest_framework import serializers
from tasks_app.models import SubTask


#class SubTaskListSerializer(APIView):
class SubTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTask
        fields = '__all__'
        read_only_fields = ['created_at']

class SubTaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTask
        fields = (
            'title',
            'description',
            'status',
            'deadline',
            'task',
            'id'
        )
        read_only_fields = ['created_at']


class SubTaskDetailSerializer(serializers.ModelSerializer):
    task_title = serializers.CharField(source='task.title', read_only=True)

    class Meta:
        model = SubTask
        fields = ['id', 'title', 'description', 'status', 'deadline', 'task', 'task_title', 'created_at']
        read_only_fields = ['id', 'created_at', 'task_title']

