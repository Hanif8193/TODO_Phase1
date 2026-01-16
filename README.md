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

### Running the Application

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

## Example Session

```bash
$ python -m src.cli.main add "Buy groceries" -d "Milk, eggs, bread"
Task #1 created successfully
  Title: Buy groceries
  Status: pending

$ python -m src.cli.main add "Call dentist"
Task #2 created successfully
  Title: Call dentist
  Status: pending

$ python -m src.cli.main list
Tasks (2 total):

[1] [ ] Buy groceries
    Milk, eggs, bread

[2] [ ] Call dentist
    (no description)

Legend: [ ] pending, [x] complete

$ python -m src.cli.main done 1
Task #1 marked as complete

$ python -m src.cli.main list
Tasks (2 total):

[1] [x] Buy groceries
    Milk, eggs, bread

[2] [ ] Call dentist
    (no description)

Legend: [ ] pending, [x] complete
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

- **Data is NOT persisted**: All tasks are stored in memory and will be lost when the application exits. This is by design for Phase I.
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
