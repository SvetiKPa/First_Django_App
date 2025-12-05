from django.urls import path, include
from rest_framework.routers import DefaultRouter, SimpleRouter
from tasks_app.views import CategoryViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


# router = SimpleRouter()
router = DefaultRouter()
router.register('category', CategoryViewSet)  #viewset

urlpatterns = [
    path('tasks/', include('tasks_app.urls.tasks')),
    path('subtasks/', include('tasks_app.urls.subtasks')),
    path('jwt-auth/', TokenObtainPairView.as_view()),
    path('jwt-refresh/', TokenRefreshView.as_view()),

] + router.urls