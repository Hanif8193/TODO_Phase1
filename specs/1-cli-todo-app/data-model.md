# Data Model: Phase I In-Memory CLI Todo App

**Feature Branch**: `1-cli-todo-app`
**Date**: 2026-01-16
**Source**: `specs/1-cli-todo-app/spec.md` (Key Entities section)

## Entity Relationship Diagram

```
┌─────────────────────────────────────┐
│              Task                    │
├─────────────────────────────────────┤
│ + id: int [PK, auto-increment]      │
│ + title: str [required, non-empty]  │
│ + description: str [optional]       │
│ + status: TaskStatus [default:      │
│           pending]                   │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│           TaskStatus                 │
├─────────────────────────────────────┤
│ PENDING = "pending"                  │
│ COMPLETE = "complete"                │
└─────────────────────────────────────┘
```

## Entities

### Task

Represents a work item to be tracked by the user.

| Field | Type | Constraints | Default | Description |
|-------|------|-------------|---------|-------------|
| id | int | Primary key, unique, auto-generated | Auto-increment from 1 | Unique identifier for the task |
| title | str | Required, non-empty | N/A | Brief description of the task |
| description | str | Optional | Empty string | Detailed information about the task |
| status | TaskStatus | Enum value | PENDING | Completion state of the task |

#### Validation Rules

1. **id**: Must be a positive integer. System-generated, never user-provided.
2. **title**: Must be a non-empty string. Whitespace-only titles are invalid.
3. **description**: Any string allowed, including empty. Preserves special characters and newlines.
4. **status**: Must be one of the defined TaskStatus enum values.

#### State Transitions

```
                    mark_complete()
    ┌─────────┐ ──────────────────> ┌──────────┐
    │ PENDING │                      │ COMPLETE │
    └─────────┘ <────────────────── └──────────┘
                   mark_incomplete()
```

- New tasks always start in PENDING state
- Users can toggle between PENDING and COMPLETE
- No other states exist in Phase I

### TaskStatus (Enumeration)

| Value | String Representation | Description |
|-------|----------------------|-------------|
| PENDING | "pending" | Task has not been completed |
| COMPLETE | "complete" | Task has been completed |

## Storage Model

### In-Memory Storage Structure

```python
# Storage: dict mapping task ID to Task object
_tasks: dict[int, Task] = {}

# ID counter: tracks next available ID
_next_id: int = 1
```

### Storage Operations

| Operation | Implementation | Time Complexity |
|-----------|---------------|-----------------|
| Create | `_tasks[new_id] = task` | O(1) |
| Read (by ID) | `_tasks.get(id)` | O(1) |
| Read (all) | `list(_tasks.values())` | O(n) |
| Update | `_tasks[id] = updated_task` | O(1) |
| Delete | `del _tasks[id]` | O(1) |

### ID Generation Rules

1. IDs start at 1 (not 0) for user-friendliness
2. IDs are never reused - deleted task IDs remain unused
3. IDs always increment, even across deletes
4. Counter resets only on application restart (in-memory)

## Data Integrity

### Invariants

1. Every task has a unique, positive integer ID
2. No task exists without a non-empty title
3. Task status is always a valid TaskStatus value
4. ID counter is always greater than any existing task ID

### Error Conditions

| Condition | Error | Message |
|-----------|-------|---------|
| Task ID not found | TaskNotFoundError | "Task with ID {id} not found" |
| Empty title provided | ValidationError | "Task title cannot be empty" |
| Invalid ID format | ValidationError | "Task ID must be a valid integer" |

## Implementation Notes

### Python Dataclass Definition

```python
from dataclasses import dataclass, field
from enum import Enum

class TaskStatus(Enum):
    PENDING = "pending"
    COMPLETE = "complete"

@dataclass
class Task:
    id: int
    title: str
    description: str = ""
    status: TaskStatus = TaskStatus.PENDING
```

### Immutability Consideration

For Phase I, tasks are mutable (updated in place). If immutability is desired for Phase II:
- Use `@dataclass(frozen=True)`
- Return new Task instances on updates
- This change would be backward-compatible with the CLI interface

## Relationships

Phase I has a single entity (Task) with no relationships. Future phases may introduce:
- User → Task (ownership)
- Task → Task (subtasks, dependencies)
- Task → Tag (categorization)

These are explicitly **out of scope** for Phase I per Constitution Principle II.
