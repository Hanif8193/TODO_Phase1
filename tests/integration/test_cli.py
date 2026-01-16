"""Integration tests for the Todo App CLI.

Tests the CLI commands end-to-end by invoking the main function
with simulated command-line arguments.
"""

import pytest
from io import StringIO
import sys

from src.cli.main import main, get_service, _service
import src.cli.main as main_module


@pytest.fixture(autouse=True)
def reset_service() -> None:
    """Reset the global service before each test."""
    main_module._service = None


class TestAddCommand:
    """Integration tests for the 'add' command."""

    def test_add_command_creates_task(self, capsys: pytest.CaptureFixture) -> None:
        """Test that add command creates a task and shows confirmation."""
        exit_code = main(["add", "Buy groceries"])

        captured = capsys.readouterr()
        assert exit_code == 0
        assert "Task #1 created successfully" in captured.out
        assert "Buy groceries" in captured.out
        assert "pending" in captured.out

    def test_add_command_with_description(
        self, capsys: pytest.CaptureFixture
    ) -> None:
        """Test add command with description option."""
        exit_code = main(["add", "Buy groceries", "-d", "Milk, eggs, bread"])

        captured = capsys.readouterr()
        assert exit_code == 0
        assert "Task #1 created successfully" in captured.out

    def test_add_command_with_empty_title_fails(
        self, capsys: pytest.CaptureFixture
    ) -> None:
        """Test that add command with empty title fails."""
        exit_code = main(["add", ""])

        captured = capsys.readouterr()
        assert exit_code == 1
        assert "Error" in captured.err
        assert "title" in captured.err.lower()


class TestListCommand:
    """Integration tests for the 'list' command."""

    def test_list_command_with_no_tasks(
        self, capsys: pytest.CaptureFixture
    ) -> None:
        """Test list command when no tasks exist."""
        exit_code = main(["list"])

        captured = capsys.readouterr()
        assert exit_code == 0
        assert "No tasks found" in captured.out

    def test_list_command_with_tasks(self, capsys: pytest.CaptureFixture) -> None:
        """Test list command shows all tasks."""
        main(["add", "Task 1"])
        main(["add", "Task 2", "-d", "Description"])

        exit_code = main(["list"])

        captured = capsys.readouterr()
        assert exit_code == 0
        assert "Tasks (2 total)" in captured.out
        assert "Task 1" in captured.out
        assert "Task 2" in captured.out
        assert "Description" in captured.out

    def test_list_command_shows_status(self, capsys: pytest.CaptureFixture) -> None:
        """Test list command distinguishes pending and complete tasks."""
        main(["add", "Pending task"])
        main(["add", "Complete task"])
        main(["done", "2"])

        exit_code = main(["list"])

        captured = capsys.readouterr()
        assert exit_code == 0
        assert "[ ]" in captured.out  # Pending marker
        assert "[x]" in captured.out  # Complete marker


class TestDoneCommand:
    """Integration tests for the 'done' command."""

    def test_done_command_marks_task_complete(
        self, capsys: pytest.CaptureFixture
    ) -> None:
        """Test done command marks task as complete."""
        main(["add", "Test task"])

        exit_code = main(["done", "1"])

        captured = capsys.readouterr()
        assert exit_code == 0
        assert "marked as complete" in captured.out

    def test_done_command_with_invalid_id(
        self, capsys: pytest.CaptureFixture
    ) -> None:
        """Test done command with non-existent ID fails."""
        exit_code = main(["done", "99"])

        captured = capsys.readouterr()
        assert exit_code == 1
        assert "Error" in captured.err
        assert "not found" in captured.err.lower()


class TestUndoneCommand:
    """Integration tests for the 'undone' command."""

    def test_undone_command_marks_task_pending(
        self, capsys: pytest.CaptureFixture
    ) -> None:
        """Test undone command marks task as pending."""
        main(["add", "Test task"])
        main(["done", "1"])

        exit_code = main(["undone", "1"])

        captured = capsys.readouterr()
        assert exit_code == 0
        assert "marked as pending" in captured.out

    def test_undone_command_with_invalid_id(
        self, capsys: pytest.CaptureFixture
    ) -> None:
        """Test undone command with non-existent ID fails."""
        exit_code = main(["undone", "99"])

        captured = capsys.readouterr()
        assert exit_code == 1
        assert "Error" in captured.err


class TestUpdateCommand:
    """Integration tests for the 'update' command."""

    def test_update_command_updates_title(
        self, capsys: pytest.CaptureFixture
    ) -> None:
        """Test update command can update task title."""
        main(["add", "Old title"])

        exit_code = main(["update", "1", "-t", "New title"])

        captured = capsys.readouterr()
        assert exit_code == 0
        assert "updated successfully" in captured.out
        assert "New title" in captured.out

    def test_update_command_updates_description(
        self, capsys: pytest.CaptureFixture
    ) -> None:
        """Test update command can update task description."""
        main(["add", "Title", "-d", "Old description"])

        exit_code = main(["update", "1", "-d", "New description"])

        captured = capsys.readouterr()
        assert exit_code == 0
        assert "updated successfully" in captured.out
        assert "New description" in captured.out

    def test_update_command_requires_title_or_description(
        self, capsys: pytest.CaptureFixture
    ) -> None:
        """Test update command requires at least one option."""
        main(["add", "Test task"])

        exit_code = main(["update", "1"])

        captured = capsys.readouterr()
        assert exit_code == 1
        assert "Error" in captured.err
        assert "title" in captured.err.lower() or "description" in captured.err.lower()

    def test_update_command_with_invalid_id(
        self, capsys: pytest.CaptureFixture
    ) -> None:
        """Test update command with non-existent ID fails."""
        exit_code = main(["update", "99", "-t", "New title"])

        captured = capsys.readouterr()
        assert exit_code == 1
        assert "Error" in captured.err


class TestDeleteCommand:
    """Integration tests for the 'delete' command."""

    def test_delete_command_removes_task(
        self, capsys: pytest.CaptureFixture
    ) -> None:
        """Test delete command removes the task."""
        main(["add", "Task to delete"])

        exit_code = main(["delete", "1"])

        captured = capsys.readouterr()
        assert exit_code == 0
        assert "deleted successfully" in captured.out

    def test_delete_command_with_invalid_id(
        self, capsys: pytest.CaptureFixture
    ) -> None:
        """Test delete command with non-existent ID fails."""
        exit_code = main(["delete", "99"])

        captured = capsys.readouterr()
        assert exit_code == 1
        assert "Error" in captured.err
        assert "not found" in captured.err.lower()

    def test_deleted_task_not_in_list(self, capsys: pytest.CaptureFixture) -> None:
        """Test that deleted task no longer appears in list."""
        main(["add", "Task 1"])
        main(["add", "Task 2"])
        main(["delete", "1"])

        exit_code = main(["list"])

        captured = capsys.readouterr()
        assert exit_code == 0
        assert "Task 2" in captured.out
        assert "[1]" not in captured.out  # Task 1 should not appear


class TestHelpCommand:
    """Integration tests for help display."""

    def test_no_command_shows_help(self, capsys: pytest.CaptureFixture) -> None:
        """Test that running without command shows help."""
        exit_code = main([])

        captured = capsys.readouterr()
        assert exit_code == 0
        assert "add" in captured.out
        assert "list" in captured.out
        assert "done" in captured.out
