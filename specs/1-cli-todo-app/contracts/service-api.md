# Service API Contract: Phase I In-Memory CLI Todo App

**Feature Branch**: `1-cli-todo-app`
**Date**: 2026-01-16
**Source**: `specs/1-cli-todo-app/spec.md` (Functional Requirements)

## Overview

This document defines the internal service API contract for the TaskService class. The CLI layer calls these methods to perform task operations.

## TaskService Class

### Module Location

```
src/services/task_service.py
```

### Class Definition

```python
class TaskService:
    """Service for managing in-memory task storage and CRUD operations."""
```

## Methods

### create_task

Creates a new task with auto-generated ID.

**Signature**:
```python
def create_task(self, title: str, description: str = "") -> Task
```

**Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| title | str | Yes | Task title (must be non-empty after stripping whitespace) |
| description | str | No | Task description (defaults to empty string) |

**Returns**: `Task` - The newly created task with assigned ID

**Raises**:
- `ValidationError` - If title is empty or whitespace-only

**Behavior**:
1. Validate title is non-empty
2. Generate next sequential ID
3. Create Task with status PENDING
4. Store task in memory
5. Return created task

**Example**:
```python
task = service.create_task("Buy groceries", "Milk, eggs")
# task.id = 1, task.status = TaskStatus.PENDING
```

---

### get_task

Retrieves a single task by ID.

**Signature**:
```python
def get_task(self, task_id: int) -> Task
```

**Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| task_id | int | Yes | ID of the task to retrieve |

**Returns**: `Task` - The requested task

**Raises**:
- `TaskNotFoundError` - If no task exists with the given ID

**Example**:
```python
task = service.get_task(1)
```

---

### get_all_tasks

Retrieves all tasks in creation order.

**Signature**:
```python
def get_all_tasks(self) -> list[Task]
```

**Parameters**: None

**Returns**: `list[Task]` - List of all tasks, ordered by ID (creation order)

**Behavior**:
- Returns empty list if no tasks exist
- Tasks are sorted by ID ascending

**Example**:
```python
tasks = service.get_all_tasks()
# [Task(id=1, ...), Task(id=2, ...), ...]
```

---

### update_task

Updates a task's title and/or description.

**Signature**:
```python
def update_task(
    self,
    task_id: int,
    title: str | None = None,
    description: str | None = None
) -> Task
```

**Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| task_id | int | Yes | ID of the task to update |
| title | str \| None | No | New title (if provided) |
| description | str \| None | No | New description (if provided) |

**Returns**: `Task` - The updated task

**Raises**:
- `TaskNotFoundError` - If no task exists with the given ID
- `ValidationError` - If new title is empty or whitespace-only

**Behavior**:
1. Find existing task by ID
2. If title provided, validate non-empty and update
3. If description provided, update (empty string allowed)
4. Return updated task

**Example**:
```python
task = service.update_task(1, title="New title")
task = service.update_task(1, description="New description")
task = service.update_task(1, title="New", description="Both updated")
```

---

### delete_task

Deletes a task by ID.

**Signature**:
```python
def delete_task(self, task_id: int) -> None
```

**Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| task_id | int | Yes | ID of the task to delete |

**Returns**: `None`

**Raises**:
- `TaskNotFoundError` - If no task exists with the given ID

**Behavior**:
1. Verify task exists
2. Remove task from storage
3. ID is not reused

**Example**:
```python
service.delete_task(1)  # Task 1 removed, ID 1 never reused
```

---

### mark_complete

Marks a task as complete.

**Signature**:
```python
def mark_complete(self, task_id: int) -> Task
```

**Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| task_id | int | Yes | ID of the task to mark complete |

**Returns**: `Task` - The updated task with status COMPLETE

**Raises**:
- `TaskNotFoundError` - If no task exists with the given ID

**Behavior**:
1. Find existing task
2. Update status to COMPLETE
3. Return updated task

**Example**:
```python
task = service.mark_complete(1)
# task.status == TaskStatus.COMPLETE
```

---

### mark_incomplete

Marks a task as pending (incomplete).

**Signature**:
```python
def mark_incomplete(self, task_id: int) -> Task
```

**Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| task_id | int | Yes | ID of the task to mark incomplete |

**Returns**: `Task` - The updated task with status PENDING

**Raises**:
- `TaskNotFoundError` - If no task exists with the given ID

**Behavior**:
1. Find existing task
2. Update status to PENDING
3. Return updated task

**Example**:
```python
task = service.mark_incomplete(1)
# task.status == TaskStatus.PENDING
```

---

## Exceptions

### TaskNotFoundError

**Module**: `src/services/exceptions.py`

```python
class TaskNotFoundError(Exception):
    """Raised when a task with the specified ID does not exist."""

    def __init__(self, task_id: int):
        self.task_id = task_id
        super().__init__(f"Task with ID {task_id} not found")
```

### ValidationError

**Module**: `src/services/exceptions.py`

```python
class ValidationError(Exception):
    """Raised when input validation fails."""

    def __init__(self, message: str):
        super().__init__(message)
```

---

## Usage Example

```python
from src.services.task_service import TaskService
from src.services.exceptions import TaskNotFoundError, ValidationError

# Initialize service
service = TaskService()

# Create tasks
task1 = service.create_task("Buy groceries", "Milk, eggs")
task2 = service.create_task("Call dentist")

# View all tasks
all_tasks = service.get_all_tasks()

# Mark complete
service.mark_complete(1)

# Update task
service.update_task(2, description="Schedule for Tuesday")

# Delete task
service.delete_task(1)

# Handle errors
try:
    service.get_task(999)
except TaskNotFoundError as e:
    print(f"Error: {e}")
```

---

## Thread Safety

**Note**: TaskService is NOT thread-safe. Phase I assumes single-user, single-threaded CLI execution. Thread safety could be added in Phase II if needed using:
- Threading locks around storage operations
- Or immutable data structures with atomic updates
