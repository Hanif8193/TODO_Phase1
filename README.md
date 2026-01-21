# Phase I In-Memory CLI Todo App

A command-line todo application built with Python 3.12+ that stores tasks in memory. Part of "The Evolution of Todo" project.

## Features

- **Add Task**: Create tasks with title and optional description
- **View Tasks**: List all tasks with status indicators
- **Mark Complete/Incomplete**: Toggle task completion status
- **Update Task**: Modify task title and/or description
- **Delete Task**: Remove tasks by ID

## Requirements

- Python 3.12 or higher
- No external runtime dependencies (uses only Python standard library)

## Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd todoapp
```

### 2. (Optional) Create virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate  # Linux/macOS
# OR
.venv\Scripts\activate     # Windows
```

### 3. Install development dependencies (for testing)

```bash
pip install pytest pytest-cov
```

## Usage

### Interactive Mode (Recommended)

Run the app in interactive menu mode where tasks persist throughout your session:

```bash
python -m src.cli.main -i
# OR
python -m src.cli.main --interactive
```

This will show a menu where you can:
1. Add task
2. List tasks
3. Mark task as done
4. Mark task as undone
5. Update task
6. Delete task
7. Exit

**Note:** Tasks persist during the interactive session and are lost when you exit.

### Command-Line Mode

You can also run individual commands (tasks will NOT persist between commands):

```bash
# Using module invocation (recommended)
python -m src.cli.main <command> [arguments]

# Or direct script execution
python src/cli/main.py <command> [arguments]
```

### Commands

#### Add a Task

```bash
python -m src.cli.main add "Buy groceries"
python -m src.cli.main add "Buy groceries" -d "Milk, eggs, bread"
```

#### List All Tasks

```bash
python -m src.cli.main list
```

#### Mark Task Complete

```bash
python -m src.cli.main done 1
```

#### Mark Task Incomplete

```bash
python -m src.cli.main undone 1
```

#### Update a Task

```bash
python -m src.cli.main update 1 -t "New title"
python -m src.cli.main update 1 -d "New description"
python -m src.cli.main update 1 -t "New title" -d "New description"
```

#### Delete a Task

```bash
python -m src.cli.main delete 1
```

#### Get Help

```bash
python -m src.cli.main --help
python -m src.cli.main add --help
```

## Example Session (Interactive Mode)

```bash
$ python -m src.cli.main -i

==================================================
TODO APP - INTERACTIVE MODE
==================================================
1. Add task
2. List tasks
3. Mark task as done
4. Mark task as undone
5. Update task
6. Delete task
7. Exit
==================================================

Select an option (1-7): 1
Enter task title: Buy groceries
Enter task description (optional): Milk, eggs, bread
Task #1 created successfully
  Title: Buy groceries
  Status: pending

==================================================
TODO APP - INTERACTIVE MODE
==================================================
...

Select an option (1-7): 1
Enter task title: Call dentist
Enter task description (optional):
Task #2 created successfully
  Title: Call dentist
  Status: pending

==================================================
TODO APP - INTERACTIVE MODE
==================================================
...

Select an option (1-7): 2
Tasks (2 total):

[1] [ ] Buy groceries
    Milk, eggs, bread

[2] [ ] Call dentist
    (no description)

Legend: [ ] pending, [x] complete

==================================================
TODO APP - INTERACTIVE MODE
==================================================
...

Select an option (1-7): 3
Enter task ID to mark as done: 1
Task #1 marked as complete

==================================================
TODO APP - INTERACTIVE MODE
==================================================
...

Select an option (1-7): 2
Tasks (2 total):

[1] [x] Buy groceries
    Milk, eggs, bread

[2] [ ] Call dentist
    (no description)

Legend: [ ] pending, [x] complete

==================================================
TODO APP - INTERACTIVE MODE
==================================================
...

Select an option (1-7): 7

Goodbye!
```

## Running Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run with coverage report
pytest --cov=src --cov-report=term-missing

# Run only unit tests
pytest tests/unit/

# Run only integration tests
pytest tests/integration/
```

## Project Structure

```
todoapp/
├── src/
│   ├── __init__.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── task.py           # Task dataclass and TaskStatus enum
│   ├── services/
│   │   ├── __init__.py
│   │   ├── exceptions.py     # Custom exceptions
│   │   └── task_service.py   # CRUD operations
│   └── cli/
│       ├── __init__.py
│       ├── commands.py       # Command handlers
│       └── main.py           # Entry point and argument parsing
├── tests/
│   ├── unit/
│   │   └── test_task_service.py
│   └── integration/
│       └── test_cli.py
├── specs/                    # Feature specifications
├── history/                  # PHR and ADR records
├── pyproject.toml           # Project configuration
├── README.md                # This file
└── CLAUDE.md               # Claude Code instructions
```

## Important Notes

- **Interactive Mode vs Command Mode**:
  - **Interactive Mode** (`-i` flag): Tasks persist throughout the session until you exit. Best for normal use.
  - **Command Mode**: Each command runs independently - tasks do NOT persist between commands.
- **Data is NOT persisted to disk**: All tasks are stored in memory and will be lost when the application exits. This is by design for Phase I.
- **Single-user**: The application is designed for single-user use.
- **No network required**: Works completely offline.

## Development

This project follows Spec-Driven Development (SDD) using:
- Constitution-based principles
- TDD with 80%+ test coverage for services
- Clean code architecture (models → services → cli)

See `.specify/memory/constitution.md` for project principles.

## License

MIT
# TODO_Phase1
