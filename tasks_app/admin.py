# from django.contrib import admin
# from tasks_app.models import Task, SubTask, Category

# admin.site.register(Task)
# admin.site.register(SubTask)
# admin.site.register(Category)

from django.contrib import admin
from .models import Task, SubTask, Category as TaskCategory

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'deadline']
    list_filter = ['deadline']

@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'task', 'status']

@admin.register(TaskCategory)
class TaskCategoryAdmin(admin.ModelAdmin):
    list_display = ['name']