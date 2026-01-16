"""Task model for the Todo App.

This module defines the Task dataclass and TaskStatus enum used to represent
tasks in the in-memory storage.
"""

from dataclasses import dataclass
from enum import Enum


class TaskStatus(Enum):
    """Enumeration of possible task completion states.

    Attributes:
        PENDING: Task has not been completed yet.
        COMPLETE: Task has been marked as completed.
    """

    PENDING = "pending"
    COMPLETE = "complete"


@dataclass
class Task:
    """Represents a task in the todo application.

    Attributes:
        id: Unique integer identifier for the task (auto-generated).
        title: Brief description of the task (required, non-empty).
        description: Detailed information about the task (optional).
        status: Current completion state of the task (defaults to PENDING).
    """

    id: int
    title: str
    description: str = ""
    status: TaskStatus = TaskStatus.PENDING
