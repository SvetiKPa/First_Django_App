from django.urls import path

from tasks_app.views import CategoryViewSet

urlpatterns = [
    path('', CategoryViewSet),
    # path('<int:pk>/', TaskRetrieveUpdateDestroyAPIView.as_view()),
]