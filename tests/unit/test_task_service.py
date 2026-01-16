"""Unit tests for TaskService.

Tests for all CRUD operations on the TaskService class.
Following TDD approach: tests written before implementation.
"""

import pytest

from src.models.task import Task, TaskStatus
from src.services.task_service import TaskService
from src.services.exceptions import TaskNotFoundError, ValidationError


class TestCreateTask:
    """Tests for TaskService.create_task method."""

    def test_create_task_with_valid_title(self) -> None:
        """Test creating a task with a valid title."""
        service = TaskService()
        task = service.create_task("Buy groceries")

        assert task.id == 1
        assert task.title == "Buy groceries"
        assert task.description == ""
        assert task.status == TaskStatus.PENDING

    def test_create_task_with_title_and_description(self) -> None:
        """Test creating a task with both title and description."""
        service = TaskService()
        task = service.create_task("Buy groceries", "Milk, eggs, bread")

        assert task.id == 1
        assert task.title == "Buy groceries"
        assert task.description == "Milk, eggs, bread"
        assert task.status == TaskStatus.PENDING

    def test_create_task_with_empty_title_raises_validation_error(self) -> None:
        """Test that empty title raises ValidationError."""
        service = TaskService()

        with pytest.raises(ValidationError) as exc_info:
            service.create_task("")

        assert "title cannot be empty" in str(exc_info.value).lower()

    def test_create_task_with_whitespace_title_raises_validation_error(self) -> None:
        """Test that whitespace-only title raises ValidationError."""
        service = TaskService()

        with pytest.raises(ValidationError) as exc_info:
            service.create_task("   ")

        assert "title cannot be empty" in str(exc_info.value).lower()

    def test_create_task_auto_increments_id(self) -> None:
        """Test that task IDs auto-increment starting from 1."""
        service = TaskService()

        task1 = service.create_task("Task 1")
        task2 = service.create_task("Task 2")
        task3 = service.create_task("Task 3")

        assert task1.id == 1
        assert task2.id == 2
        assert task3.id == 3

    def test_create_task_strips_title_whitespace(self) -> None:
        """Test that leading/trailing whitespace is stripped from title."""
        service = TaskService()
        task = service.create_task("  Buy groceries  ")

        assert task.title == "Buy groceries"


class TestGetAllTasks:
    """Tests for TaskService.get_all_tasks method."""

    def test_get_all_tasks_returns_empty_list_when_no_tasks(self) -> None:
        """Test that get_all_tasks returns empty list when no tasks exist."""
        service = TaskService()
        tasks = service.get_all_tasks()

        assert tasks == []

    def test_get_all_tasks_returns_all_tasks_sorted_by_id(self) -> None:
        """Test that get_all_tasks returns all tasks sorted by ID."""
        service = TaskService()
        service.create_task("Task 1")
        service.create_task("Task 2")
        service.create_task("Task 3")

        tasks = service.get_all_tasks()

        assert len(tasks) == 3
        assert tasks[0].id == 1
        assert tasks[1].id == 2
        assert tasks[2].id == 3


class TestMarkComplete:
    """Tests for TaskService.mark_complete method."""

    def test_mark_complete_updates_status(self) -> None:
        """Test that mark_complete changes status to COMPLETE."""
        service = TaskService()
        task = service.create_task("Test task")
        assert task.status == TaskStatus.PENDING

        updated_task = service.mark_complete(1)

        assert updated_task.status == TaskStatus.COMPLETE

    def test_mark_complete_with_invalid_id_raises_task_not_found_error(self) -> None:
        """Test that mark_complete with invalid ID raises TaskNotFoundError."""
        service = TaskService()

        with pytest.raises(TaskNotFoundError) as exc_info:
            service.mark_complete(99)

        assert exc_info.value.task_id == 99


class TestMarkIncomplete:
    """Tests for TaskService.mark_incomplete method."""

    def test_mark_incomplete_updates_status(self) -> None:
        """Test that mark_incomplete changes status to PENDING."""
        service = TaskService()
        task = service.create_task("Test task")
        service.mark_complete(1)
        assert task.status == TaskStatus.COMPLETE

        updated_task = service.mark_incomplete(1)

        assert updated_task.status == TaskStatus.PENDING


class TestUpdateTask:
    """Tests for TaskService.update_task method."""

    def test_update_task_with_new_title(self) -> None:
        """Test updating a task with a new title."""
        service = TaskService()
        service.create_task("Old title", "Description")

        updated_task = service.update_task(1, title="New title")

        assert updated_task.title == "New title"
        assert updated_task.description == "Description"

    def test_update_task_with_new_description(self) -> None:
        """Test updating a task with a new description only."""
        service = TaskService()
        service.create_task("Title", "Old description")

        updated_task = service.update_task(1, description="New description")

        assert updated_task.title == "Title"
        assert updated_task.description == "New description"

    def test_update_task_with_both_title_and_description(self) -> None:
        """Test updating a task with both new title and description."""
        service = TaskService()
        service.create_task("Old title", "Old description")

        updated_task = service.update_task(
            1, title="New title", description="New description"
        )

        assert updated_task.title == "New title"
        assert updated_task.description == "New description"

    def test_update_task_with_invalid_id_raises_task_not_found_error(self) -> None:
        """Test that update_task with invalid ID raises TaskNotFoundError."""
        service = TaskService()

        with pytest.raises(TaskNotFoundError) as exc_info:
            service.update_task(99, title="New title")

        assert exc_info.value.task_id == 99

    def test_update_task_with_empty_title_raises_validation_error(self) -> None:
        """Test that update_task with empty title raises ValidationError."""
        service = TaskService()
        service.create_task("Original title")

        with pytest.raises(ValidationError) as exc_info:
            service.update_task(1, title="")

        assert "title cannot be empty" in str(exc_info.value).lower()


class TestDeleteTask:
    """Tests for TaskService.delete_task method."""

    def test_delete_task_removes_task(self) -> None:
        """Test that delete_task removes the task from storage."""
        service = TaskService()
        service.create_task("Task to delete")
        assert len(service.get_all_tasks()) == 1

        service.delete_task(1)

        assert len(service.get_all_tasks()) == 0

    def test_delete_task_with_invalid_id_raises_task_not_found_error(self) -> None:
        """Test that delete_task with invalid ID raises TaskNotFoundError."""
        service = TaskService()

        with pytest.raises(TaskNotFoundError) as exc_info:
            service.delete_task(99)

        assert exc_info.value.task_id == 99

    def test_deleted_id_is_not_reused(self) -> None:
        """Test that deleted task IDs are not reused."""
        service = TaskService()
        service.create_task("Task 1")  # ID 1
        service.create_task("Task 2")  # ID 2
        service.delete_task(1)

        task3 = service.create_task("Task 3")

        assert task3.id == 3  # Not 1


class TestGetTask:
    """Tests for TaskService.get_task method."""

    def test_get_task_returns_task(self) -> None:
        """Test that get_task returns the correct task."""
        service = TaskService()
        created_task = service.create_task("Test task", "Description")

        retrieved_task = service.get_task(1)

        assert retrieved_task.id == created_task.id
        assert retrieved_task.title == "Test task"
        assert retrieved_task.description == "Description"

    def test_get_task_with_invalid_id_raises_task_not_found_error(self) -> None:
        """Test that get_task with invalid ID raises TaskNotFoundError."""
        service = TaskService()

        with pytest.raises(TaskNotFoundError) as exc_info:
            service.get_task(99)

        assert exc_info.value.task_id == 99
