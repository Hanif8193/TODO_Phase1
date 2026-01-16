# CLI Interface Contract: Phase I In-Memory CLI Todo App

**Feature Branch**: `1-cli-todo-app`
**Date**: 2026-01-16
**Source**: `specs/1-cli-todo-app/spec.md` (Functional Requirements)

## Overview

This document defines the command-line interface contract for the Phase I Todo App. The CLI uses subcommands to organize the five core features.

## Invocation Pattern

```bash
python -m src.cli.main <command> [arguments] [options]
# OR
python src/cli/main.py <command> [arguments] [options]
```

## Commands

### 1. Add Task

**Command**: `add`

**Synopsis**:
```bash
todo add <title> [--description|-d <description>]
```

**Arguments**:
| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| title | string | Yes | Task title (positional) |

**Options**:
| Option | Short | Type | Default | Description |
|--------|-------|------|---------|-------------|
| --description | -d | string | "" | Task description |

**Success Output** (exit code 0):
```
Task #<id> created successfully
  Title: <title>
  Status: pending
```

**Error Output** (exit code 1):
```
Error: Task title cannot be empty
```

**Examples**:
```bash
# Add task with title only
todo add "Buy groceries"

# Add task with title and description
todo add "Buy groceries" -d "Milk, eggs, bread"
todo add "Buy groceries" --description "Milk, eggs, bread"
```

---

### 2. View Tasks

**Command**: `list`

**Synopsis**:
```bash
todo list
```

**Arguments**: None

**Options**: None

**Success Output - With Tasks** (exit code 0):
```
Tasks (3 total):

[1] [ ] Buy groceries
    Milk, eggs, bread

[2] [x] Call dentist
    Schedule appointment

[3] [ ] Review PR
    (no description)

Legend: [ ] pending, [x] complete
```

**Success Output - No Tasks** (exit code 0):
```
No tasks found. Add one with: todo add "Task title"
```

**Examples**:
```bash
todo list
```

---

### 3. Mark Complete/Incomplete

**Command**: `done` / `undone`

**Synopsis**:
```bash
todo done <id>
todo undone <id>
```

**Arguments**:
| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| id | integer | Yes | Task ID to toggle |

**Options**: None

**Success Output** (exit code 0):
```
Task #<id> marked as complete
# OR
Task #<id> marked as pending
```

**Error Output** (exit code 1):
```
Error: Task with ID <id> not found
# OR
Error: Task ID must be a valid integer
```

**Examples**:
```bash
todo done 1      # Mark task 1 as complete
todo undone 1    # Mark task 1 as pending
```

---

### 4. Update Task

**Command**: `update`

**Synopsis**:
```bash
todo update <id> [--title|-t <title>] [--description|-d <description>]
```

**Arguments**:
| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| id | integer | Yes | Task ID to update |

**Options**:
| Option | Short | Type | Required | Description |
|--------|-------|------|----------|-------------|
| --title | -t | string | No* | New task title |
| --description | -d | string | No* | New task description |

*At least one of --title or --description must be provided.

**Success Output** (exit code 0):
```
Task #<id> updated successfully
  Title: <title>
  Description: <description>
  Status: <status>
```

**Error Output** (exit code 1):
```
Error: Task with ID <id> not found
# OR
Error: Task ID must be a valid integer
# OR
Error: At least one of --title or --description is required
# OR
Error: Task title cannot be empty
```

**Examples**:
```bash
todo update 1 -t "New title"
todo update 1 --description "New description"
todo update 1 -t "New title" -d "New description"
```

---

### 5. Delete Task

**Command**: `delete`

**Synopsis**:
```bash
todo delete <id>
```

**Arguments**:
| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| id | integer | Yes | Task ID to delete |

**Options**: None

**Success Output** (exit code 0):
```
Task #<id> deleted successfully
```

**Error Output** (exit code 1):
```
Error: Task with ID <id> not found
# OR
Error: Task ID must be a valid integer
```

**Examples**:
```bash
todo delete 1
```

---

### 6. Help

**Command**: `--help` / `-h`

**Synopsis**:
```bash
todo --help
todo <command> --help
```

**Output**:
```
usage: todo [-h] {add,list,done,undone,update,delete} ...

Phase I In-Memory CLI Todo App

positional arguments:
  {add,list,done,undone,update,delete}
    add                 Add a new task
    list                List all tasks
    done                Mark a task as complete
    undone              Mark a task as pending
    update              Update a task
    delete              Delete a task

optional arguments:
  -h, --help            show this help message and exit
```

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | User error (invalid input, task not found) |
| 2 | System error (unexpected exception) |

## Error Message Format

All error messages follow this format:
```
Error: <human-readable description>
```

Errors are written to stderr, not stdout.

## Service Layer Contract

The CLI commands map to TaskService methods:

| CLI Command | Service Method | Signature |
|-------------|---------------|-----------|
| `add` | `create_task` | `(title: str, description: str = "") -> Task` |
| `list` | `get_all_tasks` | `() -> list[Task]` |
| `done` | `mark_complete` | `(task_id: int) -> Task` |
| `undone` | `mark_incomplete` | `(task_id: int) -> Task` |
| `update` | `update_task` | `(task_id: int, title: str \| None, description: str \| None) -> Task` |
| `delete` | `delete_task` | `(task_id: int) -> None` |

### Service Exceptions

| Exception | Raised When | CLI Behavior |
|-----------|-------------|--------------|
| `TaskNotFoundError` | Task ID doesn't exist | Print error, exit 1 |
| `ValidationError` | Invalid input (empty title) | Print error, exit 1 |
