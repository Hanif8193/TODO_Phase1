<!--
SYNC IMPACT REPORT
==================
Version change: 0.0.0 → 1.0.0 (MAJOR - initial ratification)
Modified principles: N/A (initial creation)
Added sections:
  - Core Principles (6 principles)
  - Development Workflow (Agentic Dev Stack)
  - Project Structure
  - Governance
Removed sections: N/A
Templates requiring updates:
  - .specify/templates/plan-template.md ✅ (compatible)
  - .specify/templates/spec-template.md ✅ (compatible)
  - .specify/templates/tasks-template.md ✅ (compatible)
Follow-up TODOs: None
-->

# Evolution of Todo - Phase I Constitution

## Core Principles

### I. In-Memory CLI First

All task data MUST be stored in-memory during runtime. No external databases, files, or persistent storage in Phase I. The application MUST be a command-line interface (CLI) that runs in a standard terminal console.

**Rationale**: Phase I establishes the core domain logic without persistence complexity. This enables rapid iteration and validates the data model before committing to a storage solution.

### II. Five Core Features Only

The application MUST implement exactly these five features:
1. **Add Task**: Create a task with title and description
2. **Delete Task**: Remove a task by its unique ID
3. **Update Task**: Modify task title or description by ID
4. **View Tasks**: List all tasks with their current status
5. **Toggle Complete**: Mark a task as complete or incomplete

No additional features (tags, priorities, due dates, categories) in Phase I. Each feature MUST be independently testable.

**Rationale**: Constrained scope ensures MVP delivery within hackathon timeline. Features can be extended in subsequent phases.

### III. Agentic Development Stack

All code MUST be generated via Claude Code using Spec-Kit Plus workflow:
1. **Write Spec** (`/sp.specify`): Generate specification from requirements
2. **Generate Plan** (`/sp.plan`): Produce architectural plan
3. **Break into Tasks** (`/sp.tasks`): Create actionable task list
4. **Implement Code** (`/sp.implement`): Execute tasks via Claude Code

No manual coding outside this workflow. All artifacts MUST be tracked in `specs/` and `history/`.

**Rationale**: Ensures traceability, reproducibility, and alignment with SDD methodology. Human oversight at each gate prevents scope creep.

### IV. Python 3.13+ Clean Code

All source code MUST:
- Target Python 3.13 or higher
- Follow PEP 8 style guidelines
- Use type hints for all function signatures
- Include docstrings for all public functions and classes
- Be organized in modular, single-responsibility files
- Avoid external dependencies beyond standard library for core features

**Rationale**: Modern Python with strict typing catches errors early. Minimal dependencies reduce setup friction and security surface.

### V. Self-Contained Architecture

The codebase MUST follow this structure:
```
src/
├── models/          # Task data model
├── services/        # Business logic (CRUD operations)
├── cli/             # Command-line interface
└── __init__.py

tests/
├── unit/            # Unit tests for services
└── integration/     # CLI integration tests

specs/               # Feature specifications
history/             # PHR and ADR records
```

Each module MUST be independently importable and testable. No circular dependencies allowed.

**Rationale**: Clear separation enables parallel development and simplifies testing.

### VI. Test-Driven Development

For each feature implementation:
1. Write test cases FIRST (RED phase)
2. Get user approval on test design
3. Verify tests fail appropriately
4. Implement code to pass tests (GREEN phase)
5. Refactor while maintaining green tests (REFACTOR phase)

Test coverage target: 80% minimum for `services/` module.

**Rationale**: TDD ensures requirements are met and prevents regression. Tests serve as living documentation.

## Development Workflow

### Agentic Dev Stack Execution Order

| Step | Command | Output | Gate |
|------|---------|--------|------|
| 1 | `/sp.specify` | `specs/<feature>/spec.md` | User approval |
| 2 | `/sp.plan` | `specs/<feature>/plan.md` | User approval |
| 3 | `/sp.tasks` | `specs/<feature>/tasks.md` | User approval |
| 4 | `/sp.implement` | Source code in `src/` | Tests pass |

### Project Deliverables

| Artifact | Location | Purpose |
|----------|----------|---------|
| Constitution | `.specify/memory/constitution.md` | Project rules and principles |
| Specifications | `specs/<feature>/spec.md` | Feature requirements |
| Plans | `specs/<feature>/plan.md` | Architecture decisions |
| Tasks | `specs/<feature>/tasks.md` | Implementation checklist |
| Source Code | `src/` | Python implementation |
| Tests | `tests/` | Automated test suite |
| PHR Records | `history/prompts/` | Prompt history |
| ADR Records | `history/adr/` | Architecture decisions |
| README | `README.md` | Setup instructions |
| Claude Guide | `CLAUDE.md` | Claude Code usage |

## Project Structure

```
todoapp/
├── .specify/
│   ├── memory/
│   │   └── constitution.md      # This file
│   └── templates/               # SDD templates
├── specs/
│   └── cli-todo/                # Phase I feature
│       ├── spec.md
│       ├── plan.md
│       └── tasks.md
├── src/
│   ├── __init__.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── task.py              # Task dataclass
│   ├── services/
│   │   ├── __init__.py
│   │   └── task_service.py      # CRUD operations
│   └── cli/
│       ├── __init__.py
│       └── main.py              # CLI entry point
├── tests/
│   ├── unit/
│   │   └── test_task_service.py
│   └── integration/
│       └── test_cli.py
├── history/
│   ├── prompts/                 # PHR records
│   │   ├── constitution/
│   │   ├── cli-todo/
│   │   └── general/
│   └── adr/                     # ADR records
├── README.md
├── CLAUDE.md
└── pyproject.toml               # Project metadata
```

## Governance

### Amendment Process

1. Propose change with rationale in a PHR
2. Run three-part ADR significance test (Impact, Alternatives, Scope)
3. If significant, create ADR via `/sp.adr`
4. Update constitution with version bump
5. Propagate changes to dependent templates
6. Document in Sync Impact Report

### Versioning Policy

Constitution follows semantic versioning:
- **MAJOR**: Principle removal or incompatible redefinition
- **MINOR**: New principle or materially expanded guidance
- **PATCH**: Clarifications, wording, non-semantic refinements

### Compliance Review

All PRs and code reviews MUST verify:
- [ ] Code follows Python 3.13+ guidelines (Principle IV)
- [ ] No external persistence added (Principle I)
- [ ] Only five core features implemented (Principle II)
- [ ] All code generated via agentic workflow (Principle III)
- [ ] Tests written before implementation (Principle VI)
- [ ] Project structure maintained (Principle V)

### Environment Requirements

- Python 3.13+
- Standard terminal console (cmd, PowerShell, bash, zsh)
- Windows users: WSL 2 recommended for consistent behavior
- No external database or file storage required

**Version**: 1.0.0 | **Ratified**: 2026-01-16 | **Last Amended**: 2026-01-16
