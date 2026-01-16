# Research: Phase I In-Memory CLI Todo App

**Feature Branch**: `1-cli-todo-app`
**Date**: 2026-01-16
**Status**: Complete

## Research Summary

This document captures research findings and technology decisions for the Phase I In-Memory CLI Todo App. Given the constrained scope (in-memory, CLI-only, standard library), most decisions are straightforward.

## Technology Decisions

### 1. CLI Framework

**Decision**: Use Python's built-in `argparse` module

**Rationale**:
- Part of Python standard library (no external dependencies per Constitution Principle IV)
- Mature, well-documented, widely understood
- Supports subcommands naturally (add, delete, update, view, complete)
- Built-in help generation and argument validation

**Alternatives Considered**:
| Alternative | Rejected Because |
|-------------|-----------------|
| Click | External dependency violates Constitution |
| Typer | External dependency violates Constitution |
| sys.argv manual parsing | Less maintainable, no built-in validation |
| Interactive REPL | More complex, not specified in requirements |

### 2. Data Model Implementation

**Decision**: Use Python `dataclass` with `field` defaults

**Rationale**:
- Native to Python 3.7+ (well within 3.13+ requirement)
- Automatic `__init__`, `__repr__`, `__eq__` generation
- Type hints built-in
- No external dependencies
- Immutable option available if needed

**Alternatives Considered**:
| Alternative | Rejected Because |
|-------------|-----------------|
| Named tuples | Less flexible for updates |
| Plain dict | No type safety, harder to maintain |
| Pydantic | External dependency |
| attrs | External dependency |

### 3. In-Memory Storage Pattern

**Decision**: Simple Python `dict` with integer keys, managed by TaskService class

**Rationale**:
- O(1) lookup by ID
- Native Python, no dependencies
- Easy to iterate for view operations
- Clear separation: dict = storage, service = business logic

**Alternatives Considered**:
| Alternative | Rejected Because |
|-------------|-----------------|
| List with linear search | O(n) lookup by ID |
| SQLite in-memory | Violates "no external databases" spirit |
| Custom tree structure | Over-engineering for Phase I scope |

### 4. ID Generation Strategy

**Decision**: Auto-incrementing integer starting at 1, using class-level counter

**Rationale**:
- Simple, predictable IDs for users
- No collision risk in single-user scenario
- Easy to implement with class variable
- IDs never reused (deleted IDs remain unused)

**Alternatives Considered**:
| Alternative | Rejected Because |
|-------------|-----------------|
| UUID | Harder for users to type/remember |
| Timestamp-based | Unnecessarily complex |
| Hash-based | Overkill for in-memory use case |

### 5. Testing Framework

**Decision**: Use `pytest` for unit and integration tests

**Rationale**:
- Industry standard for Python testing
- Simple syntax, powerful fixtures
- Good CLI testing support with capsys
- Constitution Principle VI requires TDD with 80% coverage target

**Alternatives Considered**:
| Alternative | Rejected Because |
|-------------|-----------------|
| unittest | More verbose, less readable |
| nose2 | Less active development |
| doctest | Not suitable for comprehensive testing |

**Note**: pytest is the only external dev dependency, acceptable as it's testing-only and not part of runtime.

### 6. Project Entry Point

**Decision**: Use `__main__.py` pattern with `python -m` invocation

**Rationale**:
- Standard Python package execution pattern
- Works without installation
- Clean import structure
- Also support direct `main.py` execution

**Alternatives Considered**:
| Alternative | Rejected Because |
|-------------|-----------------|
| Console script entry point | Requires installation/setup |
| Standalone script | Harder to organize imports |

## Architecture Decisions

### Module Responsibilities

| Module | Responsibility | Dependencies |
|--------|---------------|--------------|
| `models/task.py` | Task dataclass definition | None |
| `services/task_service.py` | CRUD operations, business logic | models |
| `cli/main.py` | Argument parsing, user interaction | services |
| `cli/commands.py` | Individual command handlers | services |

### Error Handling Strategy

**Decision**: Use custom exceptions with user-friendly messages

- `TaskNotFoundError`: When task ID doesn't exist
- `ValidationError`: When input validation fails (empty title)

CLI layer catches exceptions and displays formatted error messages.

### Output Format

**Decision**: Human-readable text output with consistent formatting

```
Task #1 created successfully (status: pending)
---
ID: 1
Title: Buy groceries
Description: Milk, eggs, bread
Status: pending
---
```

**Future Consideration**: JSON output flag could be added in Phase II for scripting.

## Resolved Clarifications

| Topic | Resolution | Source |
|-------|------------|--------|
| CLI interaction style | Command-line arguments, not interactive REPL | Spec FR-009 |
| Error message format | Plain text, actionable messages | Spec FR-008, SC-005 |
| Task ID format | Integer, auto-incrementing from 1 | Spec FR-002 |
| Status values | "pending" and "complete" strings | Spec Key Entities |
| Persistence | None - in-memory only | Constitution Principle I |

## Open Questions

None - all technical decisions resolved for Phase I scope.
