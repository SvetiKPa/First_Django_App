from django.utils import timezone

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from django.http import HttpResponse
from django.db.models import Count

from tasks_app.models import Task, SubTask
from tasks_app.serializers import (TaskListSerializer,
                                   TaskDetailedSerializer,
                                   TaskCreateSerializer,
                                   TaskUpdateSerializer,
                                   SubTaskCreateSerializer,
                                   )


def hello_world(request, user_name):
    return HttpResponse(f"<h1>Hello, {user_name} in TASKS_APP! </h1>")


@api_view(['GET', ])
def get_all_tasks(request: Request) -> Response:
    tasks = Task.objects.all()
    tasks_dto = TaskListSerializer(tasks, many=True)
    return Response(
        data=tasks_dto.data,
        status=status.HTTP_200_OK
    )


@api_view(['GET'])
def get_task_by_id(request: Request, task_id: int):
    try:
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        return Response(
            data={"error": f"Задача с id={task_id} не найдена"},
            status=status.HTTP_404_NOT_FOUND
        )
    task_dto = TaskDetailedSerializer(task)
    return Response(
        data=task_dto.data,
        status=status.HTTP_200_OK
    )


@api_view(['POST', ])
def create_new_task(request: Request) -> Response:
    task_dto = TaskCreateSerializer(data=request.data)
    if not task_dto.is_valid():
        return Response(
            data=task_dto.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    try:
        task = task_dto.save()
    except Exception as err:
        return Response(
            data={"error": f"Ошибка сохранения {str(err)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    return Response(
        data=task_dto.data,
        status=status.HTTP_201_CREATED
    )


# statistic
# таких как общее количество задач,
# количество задач по каждому статусу и количество просроченных задач.
@api_view(['GET', ])
def tasks_statistic(request):
    total_tasks = Task.objects.count()
    task_by_status = Task.objects.values("status").annotate(count=Count("status"))
    not_done = Task.objects.filter(
        deadline__lt=timezone.now()
    ).exclude(status='Done').count()

    return Response(
        data={"total_task": total_tasks,
              "task_by_status": task_by_status,
              "not_done": not_done},
        status=status.HTTP_200_OK
    )
#########################################################################
from rest_framework.views import APIView

class SubTaskListCreateView(APIView):
    def get(self, request):
        queryset = SubTask.objects.all()
        subtask_dto = SubTaskCreateSerializer(queryset, many=True)
        return Response(data=subtask_dto.data, status=status.HTTP_200_OK)

    def post(self, request):
        subtask_dto = SubTaskCreateSerializer(data=request.data)
        if subtask_dto.is_valid():
            subtask_dto.save()
            return Response(subtask_dto.data, status=status.HTTP_201_CREATED)
        return Response(subtask_dto.errors, status.HTTP_400_BAD_REQUEST)

class SubTaskDetailUpdateDeleteView(APIView):
    def get_object(self, pk):
        try:
            return SubTask.objects.get(pk=pk)
        except SubTask.DoesNotExist:
            return None

    def get(self, request, pk):
        subtask = self.get_object(pk)
        if not subtask:
            return Response(
                {"error": "SubTask not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = SubTaskCreateSerializer(subtask)
        return Response(serializer.data)

    def put(self, request, pk):
        subtask = self.get_object(pk)
        if not subtask:
            return Response(
                {"error": "SubTask not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = SubTaskCreateSerializer(instance=subtask, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        subtask = self.get_object(pk)
        if not subtask:
            return Response(
                {"error": "SubTask not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        subtask.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
