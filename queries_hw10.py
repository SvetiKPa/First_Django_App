import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from tasks_app.models import Task, SubTask, Category
from django.utils.timezone import now, timedelta
from django.db.models import Q

# new_categ=Category.objects.create(name="Category F")
# print(new_categ.id) # name- unique

# new_task=Task.objects.create(
#     title="Prepare presentation",
#     description="Prepare materials and slides for the presentation",
#     status="NEW",
#     deadline="2025-11-18"
#    )
#
# print(new_task.id)
# new_subtask1 = SubTask.objects.create(
#     title="Gather information",
#     description="Find necessary information for the presentation",
#     status="NEW",
#     deadline="2025-11-17",
#     task=new_task
# )
# new_subtask2=SubTask.objects.create(
#     title="Create slides",
#     description="Create presentation slides",
#     status="NEW",
#     deadline="2025-11-16",
#     task=new_task
#     )
# print(f"Created subtasks  {new_subtask1.id, new_subtask2.id} with TASK_ID: {new_task.id}")

print('='*10, "NEW")
status_new = Task.objects.filter(status='NEW')
if status_new.exists():
    for qs in status_new:
        print(f"{qs.title} - {qs.deadline}")
else:
    print("Нет задач со статусом NEW")

print('='*10, "DONE")
today = now()
status_done = SubTask.objects.filter(Q(status='DONE') &
                                     Q(deadline__lte=today))
if status_done.exists():
    for qs in status_done:
        print(f"{qs.title} - {qs.deadline}")
else:
    print("Нет выполненных подзадач с истекшим дедлайном")

print('='*10, "UPDATE")
# Изменение записей:
# Измените статус "Prepare presentation" на "In progress".
prepare_pr = Task.objects.filter(title__contains='Prepare') #+Subtask
if prepare_pr.exists():
    for task in prepare_pr:
        Task.objects.filter(id=task.id).update(status='IN_PROGRESS')
        print(f"Статус задачи '{task.title}' изменен на IN_PROGRESS")
        for subtask in task.subtasks.all():
            subtask.status = 'IN_PROGRESS'
            subtask.save()
            print(f"  - Подзадача '{subtask.title}' также обновлена")
else:
    print("Задачи с 'Prepare' в названии не найдены")

# Измените срок выполнения для "Gather information" на два дня назад.
date_update = SubTask.objects.filter(title__contains='Gather').first()
if date_update:
    print(f"Текущий дедлайн: {date_update.deadline}")
    new_deadline = now() - timedelta(days=2)
    date_update.deadline = new_deadline
    date_update.save()
    print(f"Новый дедлайн: {date_update.deadline}")
else:
    print("Подзадача с 'Gather' в названии не найдена")

# updated_date = SubTask.objects.filter(title__contains='Gather').update(
#     deadline=now() - timedelta(days=2)
# )

# Измените описание для "Create slides" на "Create and format presentation slides".
updated_descr = SubTask.objects.filter(title__contains='Create slides').update(
    description='Create and format presentation slides'
)
# Удаление записей:
print('='*10, "DELETE")
# Удалите задачу "Prepare presentation" и все ее подзадачи.
prepare_pr = Task.objects.filter(title__contains='Prepare')
prepare_pr.delete()


# Показать все поля модели
# print("Task fields:", [f.name for f in Task._meta.get_fields()])
# print("SubTask fields:", [f.name for f in SubTask._meta.get_fields()])





