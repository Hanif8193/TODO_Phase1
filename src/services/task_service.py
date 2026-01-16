"""Task service for managing in-memory task storage and CRUD operations.

This module provides the TaskService class which handles all business logic
for creating, reading, updating, and deleting tasks.
"""

from src.models.task import Task, TaskStatus
from src.services.exceptions import TaskNotFoundError, ValidationError


class TaskService:
    """Service for managing in-memory task storage and CRUD operations.

    This class provides methods for creating, reading, updating, and deleting
    tasks stored in memory. Tasks are identified by unique auto-incrementing
    integer IDs.

    Attributes:
        _tasks: Internal dictionary storing tasks by ID.
        _next_id: Counter for generating unique task IDs.
    """

    def __init__(self) -> None:
        """Initialize TaskService with empty storage and ID counter."""
        self._tasks: dict[int, Task] = {}
        self._next_id: int = 1

    def create_task(self, title: str, description: str = "") -> Task:
        """Create a new task with auto-generated ID.

        Args:
            title: Task title (must be non-empty after stripping whitespace).
            description: Optional task description (defaults to empty string).

        Returns:
            The newly created Task with assigned ID and PENDING status.

        Raises:
            ValidationError: If title is empty or whitespace-only.
        """
        # Validate title
        if not title or not title.strip():
            raise ValidationError("Task title cannot be empty")

        # Create task with next available ID
        task = Task(
            id=self._next_id,
            title=title.strip(),
            description=description,
            status=TaskStatus.PENDING,
        )

        # Store task and increment ID counter
        self._tasks[self._next_id] = task
        self._next_id += 1

        return task

    def get_task(self, task_id: int) -> Task:
        """Retrieve a single task by ID.

        Args:
            task_id: ID of the task to retrieve.

        Returns:
            The requested Task.

        Raises:
            TaskNotFoundError: If no task exists with the given ID.
        """
        if task_id not in self._tasks:
            raise TaskNotFoundError(task_id)
        return self._tasks[task_id]

    def get_all_tasks(self) -> list[Task]:
        """Retrieve all tasks in creation order.

        Returns:
            List of all tasks, sorted by ID (creation order).
            Returns empty list if no tasks exist.
        """
        return sorted(self._tasks.values(), key=lambda t: t.id)

    def update_task(
        self,
        task_id: int,
        title: str | None = None,
        description: str | None = None,
    ) -> Task:
        """Update a task's title and/or description.

        Args:
            task_id: ID of the task to update.
            title: New title (if provided, must be non-empty).
            description: New description (if provided, can be empty).

        Returns:
            The updated Task.

        Raises:
            TaskNotFoundError: If no task exists with the given ID.
            ValidationError: If new title is empty or whitespace-only.
        """
        task = self.get_task(task_id)

        if title is not None:
            if not title or not title.strip():
                raise ValidationError("Task title cannot be empty")
            task.title = title.strip()

        if description is not None:
            task.description = description

        return task

    def delete_task(self, task_id: int) -> None:
        """Delete a task by ID.

        Args:
            task_id: ID of the task to delete.

        Raises:
            TaskNotFoundError: If no task exists with the given ID.

        Note:
            The deleted task's ID will not be reused.
        """
        if task_id not in self._tasks:
            raise TaskNotFoundError(task_id)
        del self._tasks[task_id]

    def mark_complete(self, task_id: int) -> Task:
        """Mark a task as complete.

        Args:
            task_id: ID of the task to mark complete.

        Returns:
            The updated Task with status COMPLETE.

        Raises:
            TaskNotFoundError: If no task exists with the given ID.
        """
        task = self.get_task(task_id)
        task.status = TaskStatus.COMPLETE
        return task

    def mark_incomplete(self, task_id: int) -> Task:
        """Mark a task as pending (incomplete).

        Args:
            task_id: ID of the task to mark incomplete.

        Returns:
            The updated Task with status PENDING.

        Raises:
            TaskNotFoundError: If no task exists with the given ID.
        """
        task = self.get_task(task_id)
        task.status = TaskStatus.PENDING
        return task
