from django.urls import path

from tasks_app.views import TaskListCreateAPIView, TaskRetrieveUpdateDestroyAPIView

urlpatterns = [
    path('', TaskListCreateAPIView.as_view()),
    path('<int:pk>/', TaskRetrieveUpdateDestroyAPIView.as_view()),
]