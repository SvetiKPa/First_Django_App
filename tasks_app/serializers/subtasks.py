from rest_framework import serializers
from tasks_app.models import SubTask


#class SubTaskListSerializer(APIView):
class SubTaskListSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTask
        fields = '__all__'
    def get(self):              #TODO
        ...
    def post(self):
        ...

class SubTaskDetailedSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTask
        fields = '__all__'

class SubTaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTask
        fields = (
            'title',
            'description',
            'status',
            'deadline'
        )
        read_only_fields = ['created_at']

class SubTaskUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTask
        fields = (
            'title',
            'description',
            'status',
            'deadline'
        )
