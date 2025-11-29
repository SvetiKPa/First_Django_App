__all__ = [
    "TaskListSerializer",
    "TaskDetailedSerializer",
    "TaskCreateSerializer",
    "TaskUpdateSerializer",
    "SubTaskSerializer",
    "SubTaskCreateSerializer",
    "SubTaskDetailSerializer",
]

from .tasks import (
    TaskListSerializer,
    TaskDetailedSerializer,
    TaskCreateSerializer,
    TaskUpdateSerializer,

)

from .subtasks import (
    SubTaskSerializer,
    SubTaskCreateSerializer,
    SubTaskDetailSerializer,
)