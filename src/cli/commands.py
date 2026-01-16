"""Command handlers for the Todo App CLI.

This module implements handler functions for each CLI command.
Each handler is responsible for calling the appropriate service method
and formatting the output for the user.
"""

import sys

from src.models.task import Task, TaskStatus
from src.services.task_service import TaskService
from src.services.exceptions import TaskNotFoundError, ValidationError


def handle_add(service: TaskService, title: str, description: str = "") -> int:
    """Handle the 'add' command to create a new task.

    Args:
        service: TaskService instance for task operations.
        title: Title for the new task.
        description: Optional description for the new task.

    Returns:
        Exit code (0 for success, 1 for error).
    """
    try:
        task = service.create_task(title, description)
        print(f"Task #{task.id} created successfully")
        print(f"  Title: {task.title}")
        print(f"  Status: {task.status.value}")
        return 0
    except ValidationError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


def handle_list(service: TaskService) -> int:
    """Handle the 'list' command to display all tasks.

    Args:
        service: TaskService instance for task operations.

    Returns:
        Exit code (0 for success).
    """
    tasks = service.get_all_tasks()

    if not tasks:
        print('No tasks found. Add one with: todo add "Task title"')
        return 0

    print(f"Tasks ({len(tasks)} total):")
    print()

    for task in tasks:
        status_marker = "[x]" if task.status == TaskStatus.COMPLETE else "[ ]"
        print(f"[{task.id}] {status_marker} {task.title}")
        if task.description:
            print(f"    {task.description}")
        else:
            print("    (no description)")
        print()

    print("Legend: [ ] pending, [x] complete")
    return 0


def handle_done(service: TaskService, task_id: int) -> int:
    """Handle the 'done' command to mark a task as complete.

    Args:
        service: TaskService instance for task operations.
        task_id: ID of the task to mark complete.

    Returns:
        Exit code (0 for success, 1 for error).
    """
    try:
        service.mark_complete(task_id)
        print(f"Task #{task_id} marked as complete")
        return 0
    except TaskNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


def handle_undone(service: TaskService, task_id: int) -> int:
    """Handle the 'undone' command to mark a task as pending.

    Args:
        service: TaskService instance for task operations.
        task_id: ID of the task to mark pending.

    Returns:
        Exit code (0 for success, 1 for error).
    """
    try:
        service.mark_incomplete(task_id)
        print(f"Task #{task_id} marked as pending")
        return 0
    except TaskNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


def handle_update(
    service: TaskService,
    task_id: int,
    title: str | None = None,
    description: str | None = None,
) -> int:
    """Handle the 'update' command to modify a task.

    Args:
        service: TaskService instance for task operations.
        task_id: ID of the task to update.
        title: New title (if provided).
        description: New description (if provided).

    Returns:
        Exit code (0 for success, 1 for error).
    """
    try:
        task = service.update_task(task_id, title=title, description=description)
        print(f"Task #{task_id} updated successfully")
        print(f"  Title: {task.title}")
        print(f"  Description: {task.description if task.description else '(none)'}")
        print(f"  Status: {task.status.value}")
        return 0
    except TaskNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except ValidationError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


def handle_delete(service: TaskService, task_id: int) -> int:
    """Handle the 'delete' command to remove a task.

    Args:
        service: TaskService instance for task operations.
        task_id: ID of the task to delete.

    Returns:
        Exit code (0 for success, 1 for error).
    """
    try:
        service.delete_task(task_id)
        print(f"Task #{task_id} deleted successfully")
        return 0
    except TaskNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
