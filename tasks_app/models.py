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

    title = models.CharField(max_length=255, verbose_name="Наименование задачи")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='NEW')
    deadline = models.DateTimeField(verbose_name="Дедлайн")
    created_date = models.DateField(auto_now_add=True, verbose_name="Дата создания")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

    def clean(self):
        """Валидация дедлайна"""
        if self.deadline and self.deadline < timezone.now():
            raise ValidationError({'deadline': 'Дедлайн не может быть в прошлом'})


class Task(BaseTask):
    categories = models.ManyToManyField(
        "Category",
        related_name="tasks",
        blank=True,                 # позволяет иметь задачи без категорий
        verbose_name="Категории",
        help_text="Выберите категории для этой задачи"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'created_date'],
                name='unique_title_per_date'
            )
        ]
        indexes = [
            models.Index(fields=['title', 'created_date']),
        ]
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} ({self.deadline.strftime('%d.%m.%Y %H:%M')})"


class SubTask(BaseTask):
    task =models.ForeignKey("Task",
                            on_delete=models.CASCADE, #подзадачи удаляются с основной задачей
                            related_name="subtasks"
                            )

    class Meta:
        verbose_name = "Подзадача"
        verbose_name_plural = "Подзадачи"
        ordering = ['-created_at']

    def __str__(self):
        return f" {self.deadline} - {self.description}"

class Category(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Название категории"
    )

