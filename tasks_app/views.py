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


# @api_view(['GET', ])
# def get_all_tasks(request: Request) -> Response:
#     tasks = Task.objects.all()
#     tasks_dto = TaskListSerializer(tasks, many=True)
#     return Response(
#         data=tasks_dto.data,
#         status=status.HTTP_200_OK
#     )
#
#
# @api_view(['GET'])
# def get_task_by_id(request: Request, task_id: int):
#     try:
#         task = Task.objects.get(pk=task_id)
#     except Task.DoesNotExist:
#         return Response(
#             data={"error": f"Задача с id={task_id} не найдена"},
#             status=status.HTTP_404_NOT_FOUND
#         )
#     task_dto = TaskDetailedSerializer(task)
#     return Response(
#         data=task_dto.data,
#         status=status.HTTP_200_OK
#     )
#
#
# @api_view(['POST', ])
# def create_new_task(request: Request) -> Response:
#     task_dto = TaskCreateSerializer(data=request.data)
#     if not task_dto.is_valid():
#         return Response(
#             data=task_dto.errors,
#             status=status.HTTP_400_BAD_REQUEST
#         )
#     try:
#         task = task_dto.save()
#     except Exception as err:
#         return Response(
#             data={"error": f"Ошибка сохранения {str(err)}"},
#             status=status.HTTP_500_INTERNAL_SERVER_ERROR
#         )
#     return Response(
#         data=task_dto.data,
#         status=status.HTTP_201_CREATED
#     )


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
    def get_filtered_queryset(self, query_params):
        # queryset = SubTask.objects.all()
        queryset = SubTask.objects.all().order_by("-deadline")

        task_name = query_params.get('parent_name')
        status_filter = query_params.get('status')

        if task_name:
            queryset = queryset.filter(task__title__icontains=task_name)

        if status_filter:
            queryset = queryset.filter(status=status_filter)

        return queryset

    def get(self, request):
        lim_num = 6
        queryset = SubTask.objects.all().order_by("-deadline")[:lim_num]
        if request.query_params:
            queryset = self.get_filtered_queryset(request.query_params)

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

######## task

class TaskListCreateView(APIView):
    #получение списка всех задач по дню недели
    def get_filtered_queryset(self, query_params):
        queryset = Task.objects.all()

        weekday = query_params.get('weekday')
        weekday_name = query_params.get('weekday_name')
        limit = query_params.get('limit')   # пагинацию

        # Фильтрация по числовому дню недели
        if weekday:
            try:
                weekday_num = int(weekday)
                django_weekday = weekday_num + 2
                queryset = queryset.filter(deadline__week_day=django_weekday)
            except (ValueError, TypeError):
                pass

        elif weekday_name:
            weekday_mapping = {
                'понедельник': 1, 'вторник': 2, 'среда': 3,
                'четверг': 4, 'пятница': 5, 'суббота': 6, 'воскресенье': 7,
                'monday': 1, 'tuesday': 2, 'wednesday': 3,
                'thursday': 2, 'friday': 5, 'saturday': 6, 'sunday': 7
            }

            normalized_name = weekday_name.lower().strip()
            if normalized_name in weekday_mapping:
                queryset = queryset.filter(
                    deadline__week_day=weekday_mapping[normalized_name]
                )

        if limit:
            try:
                limit_num = int(limit)
                queryset = queryset.order_by('-deadline')
                queryset = queryset[:limit_num]
            except (ValueError, TypeError):
                pass

        return queryset

    def get(self, request):
        # queryset = Task.objects.all()
        queryset = self.get_filtered_queryset(request.query_params)
        task_dto = TaskCreateSerializer(queryset, many=True)
        return Response(data=task_dto.data, status=status.HTTP_200_OK)

    def post(self, request):
        task_dto = TaskCreateSerializer(data=request.data)
        if task_dto.is_valid():
            task_dto.save()
            return Response(task_dto.data, status=status.HTTP_201_CREATED)
        return Response(task_dto.errors, status.HTTP_400_BAD_REQUEST)

class TaskDetailUpdateDeleteView(APIView):
    def get_object(self, pk):
        try:
            return Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            return None

    def get(self, request, pk):
        task = self.get_object(pk)
        if not task:
            return Response(
                {"error": "Task not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = TaskCreateSerializer(task)
        return Response(serializer.data)

    def put(self, request, pk):
        task = self.get_object(pk)
        if not task:
            return Response(
                {"error": "Task not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = TaskCreateSerializer(instance=task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        task = self.get_object(pk)
        if not task:
            return Response(
                {"error": "Task not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
