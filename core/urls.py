"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
# from test_app.views import hello_world
from tasks_app.views import (hello_world,
                             # create_new_task,
                             # get_task_by_id,
                             # get_all_tasks,
                             tasks_statistic,
                             SubTaskListCreateView, SubTaskDetailUpdateDeleteView,
                             TaskListCreateView, TaskDetailUpdateDeleteView,
TaskListCreateAPIView, TaskRetrieveUpdateDestroyAPIView,
SubTaskListCreateAPIView, SubTaskRetrieveUpdateDestroyAPIView,
                             )

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/<str:user_name>', hello_world),

    # CRUD for Task

    # path('api/v1/tasks/', get_all_tasks),
    # path('api/v1/tasks/create/', create_new_task),
    # path('api/v1/tasks/<int:task_id>/', get_task_by_id),
    path('api/v1/tasks_statistic/', tasks_statistic),
    # path('api/v1/tasks/', TaskListCreateView.as_view()),
    # path('api/v1/tasks/create/', TaskListCreateView.as_view()),
    # path('api/v1/tasks/<int:task_id>/', TaskDetailUpdateDeleteView.as_view()),
    # path('api/v1/subtasks/', SubTaskListCreateView.as_view()),
    # path('api/v1/subtasks/create/', SubTaskListCreateView.as_view()),
    # path('api/v1/subtasks/<int:subtask_id>/', SubTaskDetailUpdateDeleteView.as_view()),
    path('api/v1/tasks/', TaskListCreateAPIView.as_view()),
    # path('api/v1/tasks/create/', TaskListCreateAPIView.as_view()),
    path('api/v1/tasks/<int:pk>/', TaskRetrieveUpdateDestroyAPIView.as_view()),
    path('api/v1/subtasks/', SubTaskListCreateAPIView.as_view()),
    # path('api/v1/subtasks/create/', SubTaskListCreateAPIView.as_view()),
    path('api/v1/subtasks/<int:pk>/', SubTaskRetrieveUpdateDestroyAPIView.as_view()),
]
