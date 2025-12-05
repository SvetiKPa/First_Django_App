from django.urls import path

from tasks_app.views import SubTaskListCreateAPIView, SubTaskRetrieveUpdateDestroyAPIView

urlpatterns = [
    path('', SubTaskListCreateAPIView.as_view()),
    path('<int:pk>/', SubTaskRetrieveUpdateDestroyAPIView.as_view()),
]