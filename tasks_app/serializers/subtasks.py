from rest_framework import serializers
from tasks_app.models import SubTask


class SubTaskListSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTask
        fields = '__all__'


class SubTaskDetailedSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTask
        fields = '__all__'