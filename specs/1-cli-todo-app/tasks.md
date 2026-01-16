# Tasks: Phase I In-Memory CLI Todo App

**Input**: Design documents from `/specs/1-cli-todo-app/`
**Prerequisites**: plan.md (required), spec.md (required), data-model.md, contracts/
**Branch**: `1-cli-todo-app`
**Date**: 2026-01-16

**Tests**: TDD required per Constitution Principle VI (80% coverage target for services/)

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story?] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1, US2, US3, US4, US5)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- Structure: `src/models/`, `src/services/`, `src/cli/`

---

## Phase 1: Setup (Project Initialization)

**Purpose**: Create project structure and install dependencies

- [x] T001 Create directory structure: `src/`, `src/models/`, `src/services/`, `src/cli/`, `tests/`, `tests/unit/`, `tests/integration/`
- [x] T002 [P] Create `src/__init__.py` with package docstring
- [x] T003 [P] Create `src/models/__init__.py` with module exports
- [x] T004 [P] Create `src/services/__init__.py` with module exports
- [x] T005 [P] Create `src/cli/__init__.py` with module exports
- [x] T006 [P] Create `tests/__init__.py`
- [x] T007 [P] Create `tests/unit/__init__.py`
- [x] T008 [P] Create `tests/integration/__init__.py`
- [x] T009 Create `pyproject.toml` with project metadata and pytest configuration

**Checkpoint**: Project structure ready for implementation

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**CRITICAL**: No user story work can begin until this phase is complete

- [x] T010 Create `TaskStatus` enum in `src/models/task.py` with PENDING and COMPLETE values
- [x] T011 Create `Task` dataclass in `src/models/task.py` with id, title, description, status fields
- [x] T012 [P] Create `TaskNotFoundError` exception in `src/services/exceptions.py`
- [x] T013 [P] Create `ValidationError` exception in `src/services/exceptions.py`
- [x] T014 Create `TaskService` class skeleton in `src/services/task_service.py` with storage dict and ID counter
- [x] T015 Update `src/models/__init__.py` to export Task and TaskStatus
- [x] T016 Update `src/services/__init__.py` to export TaskService, TaskNotFoundError, ValidationError

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 - Add New Task (Priority: P1)

**Goal**: Users can add tasks with title and optional description

**Independent Test**: Run `add` command, verify task created with ID and pending status

### Tests for User Story 1

> **TDD: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T017 [P] [US1] Write unit test for `create_task` with valid title in `tests/unit/test_task_service.py`
- [x] T018 [P] [US1] Write unit test for `create_task` with title and description in `tests/unit/test_task_service.py`
- [x] T019 [P] [US1] Write unit test for `create_task` with empty title raises ValidationError in `tests/unit/test_task_service.py`
- [x] T020 [P] [US1] Write unit test for `create_task` auto-increments ID in `tests/unit/test_task_service.py`

### Implementation for User Story 1

- [x] T021 [US1] Implement `create_task` method in `src/services/task_service.py`
- [x] T022 [US1] Create argparse setup with `add` subcommand in `src/cli/main.py`
- [x] T023 [US1] Implement `handle_add` command handler in `src/cli/commands.py`
- [x] T024 [US1] Wire `add` command to handler in `src/cli/main.py`
- [x] T025 [US1] Run tests and verify all US1 tests pass

**Checkpoint**: User Story 1 complete - users can add tasks via CLI

---

## Phase 4: User Story 2 - View All Tasks (Priority: P1)

**Goal**: Users can view all tasks with ID, title, description, and status

**Independent Test**: Add tasks, run `list` command, verify formatted output

### Tests for User Story 2

> **TDD: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T026 [P] [US2] Write unit test for `get_all_tasks` returns empty list when no tasks in `tests/unit/test_task_service.py`
- [x] T027 [P] [US2] Write unit test for `get_all_tasks` returns all tasks sorted by ID in `tests/unit/test_task_service.py`
- [x] T028 [P] [US2] Write integration test for `list` command with no tasks in `tests/integration/test_cli.py`
- [x] T029 [P] [US2] Write integration test for `list` command with mixed status tasks in `tests/integration/test_cli.py`

### Implementation for User Story 2

- [x] T030 [US2] Implement `get_all_tasks` method in `src/services/task_service.py`
- [x] T031 [US2] Add `list` subcommand to argparse in `src/cli/main.py`
- [x] T032 [US2] Implement `handle_list` command handler with formatting in `src/cli/commands.py`
- [x] T033 [US2] Wire `list` command to handler in `src/cli/main.py`
- [x] T034 [US2] Run tests and verify all US2 tests pass

**Checkpoint**: User Story 2 complete - users can view all tasks via CLI

---

## Phase 5: User Story 3 - Mark Complete/Incomplete (Priority: P2)

**Goal**: Users can toggle task completion status

**Independent Test**: Add task, mark complete, verify status via list command

### Tests for User Story 3

> **TDD: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T035 [P] [US3] Write unit test for `mark_complete` updates status in `tests/unit/test_task_service.py`
- [x] T036 [P] [US3] Write unit test for `mark_incomplete` updates status in `tests/unit/test_task_service.py`
- [x] T037 [P] [US3] Write unit test for `mark_complete` with invalid ID raises TaskNotFoundError in `tests/unit/test_task_service.py`
- [x] T038 [P] [US3] Write integration test for `done` command in `tests/integration/test_cli.py`
- [x] T039 [P] [US3] Write integration test for `undone` command in `tests/integration/test_cli.py`

### Implementation for User Story 3

- [x] T040 [US3] Implement `get_task` helper method in `src/services/task_service.py`
- [x] T041 [US3] Implement `mark_complete` method in `src/services/task_service.py`
- [x] T042 [US3] Implement `mark_incomplete` method in `src/services/task_service.py`
- [x] T043 [US3] Add `done` and `undone` subcommands to argparse in `src/cli/main.py`
- [x] T044 [US3] Implement `handle_done` and `handle_undone` command handlers in `src/cli/commands.py`
- [x] T045 [US3] Wire `done` and `undone` commands to handlers in `src/cli/main.py`
- [x] T046 [US3] Run tests and verify all US3 tests pass

**Checkpoint**: User Story 3 complete - users can mark tasks complete/incomplete

---

## Phase 6: User Story 4 - Update Task Details (Priority: P3)

**Goal**: Users can update task title and/or description

**Independent Test**: Add task, update title, verify change via list command

### Tests for User Story 4

> **TDD: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T047 [P] [US4] Write unit test for `update_task` with new title in `tests/unit/test_task_service.py`
- [x] T048 [P] [US4] Write unit test for `update_task` with new description in `tests/unit/test_task_service.py`
- [x] T049 [P] [US4] Write unit test for `update_task` with both title and description in `tests/unit/test_task_service.py`
- [x] T050 [P] [US4] Write unit test for `update_task` with invalid ID raises TaskNotFoundError in `tests/unit/test_task_service.py`
- [x] T051 [P] [US4] Write unit test for `update_task` with empty title raises ValidationError in `tests/unit/test_task_service.py`
- [x] T052 [P] [US4] Write integration test for `update` command in `tests/integration/test_cli.py`

### Implementation for User Story 4

- [x] T053 [US4] Implement `update_task` method in `src/services/task_service.py`
- [x] T054 [US4] Add `update` subcommand to argparse in `src/cli/main.py`
- [x] T055 [US4] Implement `handle_update` command handler in `src/cli/commands.py`
- [x] T056 [US4] Wire `update` command to handler in `src/cli/main.py`
- [x] T057 [US4] Run tests and verify all US4 tests pass

**Checkpoint**: User Story 4 complete - users can update task details

---

## Phase 7: User Story 5 - Delete Task (Priority: P3)

**Goal**: Users can delete tasks by ID

**Independent Test**: Add task, delete by ID, verify removal via list command

### Tests for User Story 5

> **TDD: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T058 [P] [US5] Write unit test for `delete_task` removes task in `tests/unit/test_task_service.py`
- [x] T059 [P] [US5] Write unit test for `delete_task` with invalid ID raises TaskNotFoundError in `tests/unit/test_task_service.py`
- [x] T060 [P] [US5] Write unit test for deleted ID is not reused in `tests/unit/test_task_service.py`
- [x] T061 [P] [US5] Write integration test for `delete` command in `tests/integration/test_cli.py`

### Implementation for User Story 5

- [x] T062 [US5] Implement `delete_task` method in `src/services/task_service.py`
- [x] T063 [US5] Add `delete` subcommand to argparse in `src/cli/main.py`
- [x] T064 [US5] Implement `handle_delete` command handler in `src/cli/commands.py`
- [x] T065 [US5] Wire `delete` command to handler in `src/cli/main.py`
- [x] T066 [US5] Run tests and verify all US5 tests pass

**Checkpoint**: User Story 5 complete - users can delete tasks

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Final quality improvements and documentation

- [x] T067 [P] Add comprehensive docstrings to all classes in `src/models/task.py`
- [x] T068 [P] Add comprehensive docstrings to all methods in `src/services/task_service.py`
- [x] T069 [P] Add comprehensive docstrings to all functions in `src/cli/commands.py`
- [x] T070 [P] Add comprehensive docstrings to `src/cli/main.py`
- [x] T071 Verify PEP 8 compliance across all source files
- [x] T072 Run `pytest --cov=src --cov-report=term-missing` and verify 80% coverage for services/
- [x] T073 Create `README.md` with setup and usage instructions
- [x] T074 Validate application against `specs/1-cli-todo-app/quickstart.md` tutorial
- [x] T075 Run full test suite and ensure all tests pass

**Checkpoint**: All user stories complete, tests passing, documentation ready

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-7)**: All depend on Foundational phase completion
  - US1 (Add) and US2 (View) can run in parallel
  - US3 (Complete) depends on US1 being testable
  - US4 (Update) and US5 (Delete) can run after US1
- **Polish (Phase 8)**: Depends on all user stories being complete

### User Story Dependencies

| Story | Depends On | Can Parallel With |
|-------|------------|-------------------|
| US1 (Add) | Foundation | US2 |
| US2 (View) | Foundation | US1 |
| US3 (Complete) | US1 (for testing) | US4, US5 |
| US4 (Update) | US1 (for testing) | US3, US5 |
| US5 (Delete) | US1 (for testing) | US3, US4 |

### Within Each User Story (TDD Cycle)

1. Tests MUST be written and FAIL before implementation
2. Service methods before CLI handlers
3. Handlers before argparse wiring
4. Story complete when all tests pass

### Parallel Opportunities

**Phase 1 (Setup)**:
```bash
# All __init__.py files can be created in parallel
T002, T003, T004, T005, T006, T007, T008
```

**Phase 2 (Foundation)**:
```bash
# Exception classes can be created in parallel
T012, T013
```

**User Story Test Writing** (within each story):
```bash
# US1 tests can all be written in parallel
T017, T018, T019, T020

# US2 tests can all be written in parallel
T026, T027, T028, T029
```

---

## Implementation Strategy

### MVP First (User Story 1 + 2 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational
3. Complete Phase 3: User Story 1 (Add)
4. Complete Phase 4: User Story 2 (View)
5. **STOP and VALIDATE**: Test add/view workflow independently
6. Demo MVP: Users can add and view tasks

### Incremental Delivery

| Increment | Stories | Cumulative Capability |
|-----------|---------|----------------------|
| MVP | US1 + US2 | Add and view tasks |
| +Complete | US3 | Track completion status |
| +Update | US4 | Edit task details |
| +Delete | US5 | Full CRUD operations |

### Task Count Summary

| Phase | Task Count | Parallel Tasks |
|-------|------------|----------------|
| Setup | 9 | 7 |
| Foundational | 7 | 2 |
| US1 (Add) | 9 | 4 tests |
| US2 (View) | 9 | 4 tests |
| US3 (Complete) | 12 | 5 tests |
| US4 (Update) | 11 | 6 tests |
| US5 (Delete) | 9 | 4 tests |
| Polish | 9 | 4 |
| **Total** | **75** | **36** |

---

## Notes

- [P] tasks = different files, no dependencies on incomplete tasks
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- TDD required: verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
