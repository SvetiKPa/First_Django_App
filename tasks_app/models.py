from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError

# Create your models here.
class BaseTask(models.Model):
    STATUS_CHOICES = [
        ('NEW', 'New'),  # 1 - в базу, 2 клиенту
        ('IN_PROGRESS', 'In progress'),
        ('PENDING', 'Pending'),
        ('BLOCKED', 'Blocked'),
        ('DONE', 'Done'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True, verbose_name="Описание")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='NEW')
    deadline = models.DateTimeField(verbose_name="Дедлайн")
    created_date = models.DateField(auto_now_add=True, verbose_name="Дата создания")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'created_date'],
                name='unique_title_per_date'
            )
        ]
        ordering = ['-created_at']
        abstract = True

    # def clean(self):
    #     """Валидация дедлайна"""
    #     if self.deadline and self.deadline < timezone.now():
    #         raise ValidationError({'deadline': 'Дедлайн не может быть в прошлом'})

    def __str__(self):
        return f"{self.deadline} - {self.title}"

class Task(BaseTask):
    categories = models.ManyToManyField(
        "Category",
        related_name="tasks",
        blank=True,                 # позволяет иметь задачи без категорий
        verbose_name="Категории",
        help_text="Выберите категории для этой задачи"
    )

    class Meta:
        db_table = "task_manager_task"
        verbose_name = "Task"


class SubTask(BaseTask):
    task =models.ForeignKey("Task",
                            on_delete=models.CASCADE, #подзадачи удаляются с основной задачей
                            related_name="subtasks"
                            )

    class Meta:
        db_table = "task_manager_subtask"
        verbose_name = "Subtask"


class Category(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True
    )

    class Meta:
        db_table = "task_manager_category"
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return f"{self.name}"


