from rest_framework import permissions

from django.utils import timezone

from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from django.http import HttpResponse
from django.db.models import Count
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly

from tasks_app.models import Task, SubTask, Category
from tasks_app.serializers import (TaskListSerializer,
                                   TaskDetailedSerializer,
                                   TaskCreateSerializer,
                                   TaskUpdateSerializer,
                                   SubTaskCreateSerializer,
                                   SubTaskDetailSerializer,
                                   CategorySerializer,
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
    # получение списка всех задач по дню недели
    def get_filtered_queryset(self, query_params):
        queryset = Task.objects.all()

        weekday = query_params.get('weekday')
        weekday_name = query_params.get('weekday_name')
        limit = query_params.get('limit')  # пагинацию

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


###############################
# Реализуйте фильтрацию по полям status и deadline.
# Реализуйте поиск по полям title и description.
# Добавьте сортировку по полю created_at.
from rest_framework.generics import (ListCreateAPIView,
                                     RetrieveUpdateDestroyAPIView)
from rest_framework.filters import SearchFilter


class TaskListCreateAPIView(ListCreateAPIView):
    # queryset = Task.objects.all().order_by('-created_at')
    serializer_class = TaskListSerializer
    filter_backends = [SearchFilter]
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'deadline', 'status']
    ordering = ['-created_at']
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Task.objects.all()
        status_filter = self.request.query_params.get('status')
        deadline_filter = self.request.query_params.get('deadline')
        if status_filter:
            queryset = Task.objects.filter(status=status_filter)

        if deadline_filter and 'T' in deadline_filter:
            date_only = deadline_filter.split('T')[0]
            queryset = Task.objects.filter(deadline__date=date_only)
        elif deadline_filter:
            queryset = Task.objects.filter(deadline__date=deadline_filter)

        #     if deadline_filter:
        #         queryset = Task.objects.filter(deadline=deadline_filter)
        return queryset


class TaskRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskDetailedSerializer


class SubTaskListCreateAPIView(ListCreateAPIView):
    serializer_class = SubTaskCreateSerializer
    filter_backends = [SearchFilter]
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'deadline', 'status']
    ordering = ['-created_at']
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = SubTask.objects.all()
        status_filter = self.request.query_params.get('status')
        deadline_filter = self.request.query_params.get('deadline')
        if status_filter:
            queryset = SubTask.objects.filter(status=status_filter)
        if deadline_filter:
            queryset = SubTask.objects.filter(deadline=deadline_filter)
        return queryset


class SubTaskRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = SubTask.objects.all()
    serializer_class = SubTaskDetailSerializer

##########################
from rest_framework.viewsets import ModelViewSet

class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()  # используем SoftDeleteManager
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUser]

    @action(methods=['get',], detail=False, url_path='count_categories')
    def get_count_categories(self, request):
        count_categ = Category.objects.count()
        return Response(data=count_categ, status=status.HTTP_200_OK )