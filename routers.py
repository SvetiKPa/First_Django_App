from django.urls import path, include
from rest_framework.routers import DefaultRouter, SimpleRouter
from tasks_app.views import CategoryViewSet


# router = SimpleRouter()
router = DefaultRouter()
router.register('category', CategoryViewSet)

urlpatterns = [
    path('tasks/', include('tasks_app.urls.tasks')),
    path('subtasks/', include('tasks_app.urls.subtasks')),
    # path('categories/', include('tasks_app.urls.categories')),
] + router.urls