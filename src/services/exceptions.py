"""Custom exceptions for the Todo App services.

This module defines exceptions raised by the TaskService when
operations fail due to invalid input or missing resources.
"""


class TaskNotFoundError(Exception):
    """Raised when a task with the specified ID does not exist.

    Attributes:
        task_id: The ID that was not found.
    """

    def __init__(self, task_id: int) -> None:
        """Initialize TaskNotFoundError with the missing task ID.

        Args:
            task_id: The ID of the task that was not found.
        """
        self.task_id = task_id
        super().__init__(f"Task with ID {task_id} not found")


class ValidationError(Exception):
    """Raised when input validation fails.

    Used for cases like empty task titles or invalid input formats.
    """

    def __init__(self, message: str) -> None:
        """Initialize ValidationError with a descriptive message.

        Args:
            message: Human-readable description of the validation failure.
        """
        super().__init__(message)
