# Quickstart: Phase I In-Memory CLI Todo App

**Feature Branch**: `1-cli-todo-app`
**Date**: 2026-01-16

## Prerequisites

- Python 3.13 or higher
- Terminal/console (cmd, PowerShell, bash, zsh)
- No additional dependencies required for runtime

## Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd todoapp
```

### 2. Verify Python version

```bash
python --version
# Should output: Python 3.13.x or higher
```

### 3. (Optional) Create virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/macOS
source venv/bin/activate
```

### 4. Install development dependencies (for testing only)

```bash
pip install pytest pytest-cov
```

## Running the Application

### Method 1: Module invocation (recommended)

```bash
python -m src.cli.main <command> [arguments]
```

### Method 2: Direct script execution

```bash
python src/cli/main.py <command> [arguments]
```

## Quick Tutorial

### Step 1: Add your first task

```bash
python -m src.cli.main add "Buy groceries" -d "Milk, eggs, bread"
```

Output:
```
Task #1 created successfully
  Title: Buy groceries
  Status: pending
```

### Step 2: Add more tasks

```bash
python -m src.cli.main add "Call dentist"
python -m src.cli.main add "Review PR" -d "Check the authentication changes"
```

### Step 3: View all tasks

```bash
python -m src.cli.main list
```

Output:
```
Tasks (3 total):

[1] [ ] Buy groceries
    Milk, eggs, bread

[2] [ ] Call dentist
    (no description)

[3] [ ] Review PR
    Check the authentication changes

Legend: [ ] pending, [x] complete
```

### Step 4: Mark a task as complete

```bash
python -m src.cli.main done 1
```

Output:
```
Task #1 marked as complete
```

### Step 5: View tasks again

```bash
python -m src.cli.main list
```

Output:
```
Tasks (3 total):

[1] [x] Buy groceries
    Milk, eggs, bread

[2] [ ] Call dentist
    (no description)

[3] [ ] Review PR
    Check the authentication changes

Legend: [ ] pending, [x] complete
```

### Step 6: Update a task

```bash
python -m src.cli.main update 2 -d "Schedule for Tuesday at 2pm"
```

Output:
```
Task #2 updated successfully
  Title: Call dentist
  Description: Schedule for Tuesday at 2pm
  Status: pending
```

### Step 7: Delete a task

```bash
python -m src.cli.main delete 3
```

Output:
```
Task #3 deleted successfully
```

### Step 8: Mark a task as incomplete

```bash
python -m src.cli.main undone 1
```

Output:
```
Task #1 marked as pending
```

## Command Reference

| Command | Description | Example |
|---------|-------------|---------|
| `add <title> [-d desc]` | Add a new task | `add "Task" -d "Details"` |
| `list` | View all tasks | `list` |
| `done <id>` | Mark task complete | `done 1` |
| `undone <id>` | Mark task pending | `undone 1` |
| `update <id> [-t title] [-d desc]` | Update task | `update 1 -t "New title"` |
| `delete <id>` | Delete task | `delete 1` |
| `--help` | Show help | `--help` |

## Running Tests

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=src --cov-report=term-missing

# Run specific test file
pytest tests/unit/test_task_service.py

# Run with verbose output
pytest -v
```

## Troubleshooting

### "Module not found" error

Ensure you're running from the project root directory:
```bash
cd /path/to/todoapp
python -m src.cli.main list
```

### "Python not found" or wrong version

Check your Python installation:
```bash
# Try python3 explicitly
python3 --version
python3 -m src.cli.main list
```

### Tasks disappear after restart

This is expected behavior. Phase I stores tasks in memory only. When the application exits, all tasks are lost. This will change in Phase II with persistent storage.

## Important Notes

- **Data is not persisted**: All tasks are stored in memory and will be lost when the application exits.
- **Single-user**: The application is designed for single-user use on a local machine.
- **No network required**: The application works completely offline.

## Next Steps

After completing this quickstart:

1. Try creating multiple tasks and practicing the workflow
2. Explore the `--help` option for each command
3. Review the test files to understand expected behavior
4. Check `specs/1-cli-todo-app/spec.md` for full requirements
