# from django.contrib import admin
# from tasks_app.models import Task, SubTask, Category

# admin.site.register(Task)
# admin.site.register(SubTask)
# admin.site.register(Category)

from django.contrib import admin, messages
from .models import Task, SubTask, Category


class SubTaskInline(admin.TabularInline):
    model = SubTask
    extra = 1  # Количество пустых форм для подзадач
    fields = ['title', 'description', 'status', 'deadline']
    list_display = ['title', 'status', 'deadline']


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['short_title', 'status', 'deadline', 'description']
    list_filter = ['deadline']
    inlines = [SubTaskInline]

    @admin.display()
    def short_title(self, obj: Task):
        if len(obj.title) > 10:
            return f"{obj.title[10:]}..."
        return obj.title

    fields = ['title', 'status', 'deadline', 'description']


@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'task', 'status']

    actions = ["mark_as_done", ]

    @admin.action(description="Изменить статус на Done")
    def mark_as_done(self, request, qs):
        updated = qs.update(
            status='DONE'
        )
        self.message_user(
            request,
            f"Успешно изменен статус на 'DONE' для {updated} подзадач",
            messages.SUCCESS
        )


@admin.register(Category)
class TaskCategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
