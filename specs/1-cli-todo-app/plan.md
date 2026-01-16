# Implementation Plan: Phase I In-Memory CLI Todo App

**Branch**: `1-cli-todo-app` | **Date**: 2026-01-16 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/1-cli-todo-app/spec.md`

## Summary

Build a command-line Todo application in Python 3.13+ that stores tasks in memory with five core features: Add, Delete, Update, View, and Toggle Complete. The application follows clean code principles with modular architecture (models → services → cli) and uses only Python standard library for runtime.

## Technical Context

**Language/Version**: Python 3.13+
**Primary Dependencies**: Standard library only (argparse, dataclasses, enum)
**Storage**: In-memory (Python dict)
**Testing**: pytest (dev dependency only)
**Target Platform**: Cross-platform CLI (Windows, Linux, macOS)
**Project Type**: Single project
**Performance Goals**: Interactive CLI response (<100ms per command)
**Constraints**: No persistence, no external runtime dependencies, single-user
**Scale/Scope**: Single user, unlimited tasks (memory-limited)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| I. In-Memory CLI First | ✅ PASS | No persistence, CLI-only interface |
| II. Five Core Features Only | ✅ PASS | Add, Delete, Update, View, Toggle - no extras |
| III. Agentic Development Stack | ✅ PASS | Following spec → plan → tasks → implement workflow |
| IV. Python 3.13+ Clean Code | ✅ PASS | Type hints, PEP 8, docstrings, stdlib only |
| V. Self-Contained Architecture | ✅ PASS | models/ → services/ → cli/ structure |
| VI. Test-Driven Development | ✅ PASS | pytest with 80% coverage target for services |

**Gate Status**: PASS - No violations

## Project Structure

### Documentation (this feature)

```text
specs/1-cli-todo-app/
├── spec.md              # Feature specification
├── plan.md              # This file
├── research.md          # Technology decisions
├── data-model.md        # Entity definitions
├── quickstart.md        # User guide
├── contracts/
│   ├── cli-interface.md # CLI command contract
│   └── service-api.md   # Service layer contract
├── checklists/
│   └── requirements.md  # Specification checklist
└── tasks.md             # Implementation tasks (created by /sp.tasks)
```

### Source Code (repository root)

```text
src/
├── __init__.py
├── models/
│   ├── __init__.py
│   └── task.py              # Task dataclass, TaskStatus enum
├── services/
│   ├── __init__.py
│   ├── task_service.py      # TaskService class with CRUD operations
│   └── exceptions.py        # TaskNotFoundError, ValidationError
└── cli/
    ├── __init__.py
    ├── main.py              # Entry point with argparse setup
    └── commands.py          # Command handler functions

tests/
├── __init__.py
├── unit/
│   ├── __init__.py
│   └── test_task_service.py # Service layer unit tests
└── integration/
    ├── __init__.py
    └── test_cli.py          # CLI integration tests
```

**Structure Decision**: Single project structure per Constitution Principle V. Modular organization with clear separation: models (data), services (logic), cli (interface).

## Design Decisions

### 1. Module Organization

| Module | Responsibility | Dependencies |
|--------|---------------|--------------|
| `models/task.py` | Task dataclass, TaskStatus enum | None |
| `services/exceptions.py` | Custom exceptions | None |
| `services/task_service.py` | CRUD operations, business logic | models, exceptions |
| `cli/commands.py` | Command handlers | services |
| `cli/main.py` | Argument parsing, entry point | commands |

### 2. Data Flow

```
User Input → argparse → Command Handler → TaskService → In-Memory Storage
                                              ↓
User Output ← Formatter ← Command Handler ← Task/Exception
```

### 3. Error Handling Strategy

- Service layer raises typed exceptions (`TaskNotFoundError`, `ValidationError`)
- CLI layer catches exceptions and formats user-friendly messages
- Exit codes: 0 (success), 1 (user error), 2 (system error)

### 4. Testing Strategy

| Test Type | Location | Coverage Target |
|-----------|----------|-----------------|
| Unit | `tests/unit/test_task_service.py` | 80% of services/ |
| Integration | `tests/integration/test_cli.py` | All CLI commands |

## Complexity Tracking

> No violations to justify - all Constitution checks passed.

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| N/A | N/A | N/A |

## Implementation Phases

### Phase 1: Foundation

1. Create project structure with `__init__.py` files
2. Implement `Task` dataclass and `TaskStatus` enum
3. Implement custom exceptions
4. Set up pytest configuration

### Phase 2: Core Service

1. Implement `TaskService` class with storage
2. Implement `create_task` method
3. Implement `get_task` and `get_all_tasks` methods
4. Implement `update_task` method
5. Implement `delete_task` method
6. Implement `mark_complete` and `mark_incomplete` methods
7. Write unit tests (TDD)

### Phase 3: CLI Layer

1. Set up argparse with subcommands
2. Implement `add` command
3. Implement `list` command
4. Implement `done` and `undone` commands
5. Implement `update` command
6. Implement `delete` command
7. Write integration tests (TDD)

### Phase 4: Polish

1. Add docstrings and type hints
2. Ensure PEP 8 compliance
3. Validate 80% test coverage
4. Create README.md and project documentation
5. Final validation against quickstart.md

## Artifacts Generated

| Artifact | Path | Purpose |
|----------|------|---------|
| Research | `specs/1-cli-todo-app/research.md` | Technology decisions |
| Data Model | `specs/1-cli-todo-app/data-model.md` | Entity definitions |
| CLI Contract | `specs/1-cli-todo-app/contracts/cli-interface.md` | Command reference |
| Service Contract | `specs/1-cli-todo-app/contracts/service-api.md` | API specification |
| Quickstart | `specs/1-cli-todo-app/quickstart.md` | User guide |

## Next Steps

1. Run `/sp.tasks` to generate detailed implementation task list
2. Run `/sp.implement` to begin code generation
3. Follow TDD: write tests first, then implementation
