"""Unit tests for interactive_mode() in src/cli/main.py.

Uses unittest.mock.patch to simulate stdin input sequences,
driving every menu branch to completion.
"""

import pytest
from unittest.mock import patch

import src.cli.main as main_module
from src.cli.main import interactive_mode, main
import src.cli.commands as commands_module


@pytest.fixture(autouse=True)
def reset_service() -> None:
    """Reset the global service before each test."""
    main_module._service = None


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _run(inputs: list) -> int:
    """Run interactive_mode with a fixed sequence of simulated inputs.

    List entries may be strings or exceptions (raised on that input call).
    """
    with patch("builtins.input", side_effect=inputs):
        return interactive_mode()


# ---------------------------------------------------------------------------
# Exit (choice 7)
# ---------------------------------------------------------------------------

class TestInteractiveModeExit:
    def test_choice_7_exits_with_zero(self, capsys: pytest.CaptureFixture) -> None:
        exit_code = _run(["7"])

        assert exit_code == 0
        assert "Goodbye" in capsys.readouterr().out

    def test_keyboard_interrupt_inside_handler_exits_cleanly(
        self, capsys: pytest.CaptureFixture
    ) -> None:
        # "1" selects Add, then KeyboardInterrupt fires on the title input —
        # that's inside the try block so it's caught by except KeyboardInterrupt.
        exit_code = _run(["1", KeyboardInterrupt()])

        assert exit_code == 0
        assert "Goodbye" in capsys.readouterr().out


# ---------------------------------------------------------------------------
# Invalid menu choice
# ---------------------------------------------------------------------------

class TestInteractiveModeInvalidChoice:
    def test_invalid_choice_shows_error_then_exits(
        self, capsys: pytest.CaptureFixture
    ) -> None:
        exit_code = _run(["9", "7"])

        out = capsys.readouterr().out
        assert exit_code == 0
        assert "Invalid option" in out


# ---------------------------------------------------------------------------
# Choice 1 — Add task
# ---------------------------------------------------------------------------

class TestInteractiveModeAdd:
    def test_add_task_success(self, capsys: pytest.CaptureFixture) -> None:
        # menu, title, description, then exit
        exit_code = _run(["1", "Buy milk", "", "7"])

        out = capsys.readouterr().out
        assert exit_code == 0
        assert "Buy milk" in out

    def test_add_task_empty_title_shows_error(
        self, capsys: pytest.CaptureFixture
    ) -> None:
        # empty title → error printed → loop continues → exit
        exit_code = _run(["1", "", "7"])

        out = capsys.readouterr().out
        assert exit_code == 0
        assert "Title cannot be empty" in out


# ---------------------------------------------------------------------------
# Choice 2 — List tasks
# ---------------------------------------------------------------------------

class TestInteractiveModeList:
    def test_list_with_no_tasks(self, capsys: pytest.CaptureFixture) -> None:
        exit_code = _run(["2", "7"])

        out = capsys.readouterr().out
        assert exit_code == 0
        assert "No tasks found" in out

    def test_list_shows_added_tasks(self, capsys: pytest.CaptureFixture) -> None:
        # add a task, then list, then exit
        exit_code = _run(["1", "Walk dog", "", "2", "7"])

        out = capsys.readouterr().out
        assert exit_code == 0
        assert "Walk dog" in out


# ---------------------------------------------------------------------------
# Choice 3 — Mark done
# ---------------------------------------------------------------------------

class TestInteractiveModeDone:
    def test_mark_done_success(self, capsys: pytest.CaptureFixture) -> None:
        # add task then mark it done in one session
        exit_code = _run(["1", "Test task", "", "3", "1", "7"])

        out = capsys.readouterr().out
        assert exit_code == 0
        assert "marked as complete" in out

    def test_mark_done_invalid_id_shows_error(
        self, capsys: pytest.CaptureFixture
    ) -> None:
        # handle_done prints "Error: ..." to stderr
        exit_code = _run(["3", "99", "7"])

        assert exit_code == 0
        assert "not found" in capsys.readouterr().err.lower()

    def test_mark_done_non_numeric_id_shows_error(
        self, capsys: pytest.CaptureFixture
    ) -> None:
        exit_code = _run(["3", "abc", "7"])

        assert exit_code == 0
        assert "Invalid task ID" in capsys.readouterr().out


# ---------------------------------------------------------------------------
# Choice 4 — Mark undone
# ---------------------------------------------------------------------------

class TestInteractiveModeUndone:
    def test_mark_undone_success(self, capsys: pytest.CaptureFixture) -> None:
        # add → done → undone → exit, all in one session
        exit_code = _run(["1", "Test task", "", "3", "1", "4", "1", "7"])

        out = capsys.readouterr().out
        assert exit_code == 0
        assert "marked as pending" in out

    def test_mark_undone_non_numeric_id_shows_error(
        self, capsys: pytest.CaptureFixture
    ) -> None:
        exit_code = _run(["4", "xyz", "7"])

        assert exit_code == 0
        assert "Invalid task ID" in capsys.readouterr().out


# ---------------------------------------------------------------------------
# Choice 5 — Update task
# ---------------------------------------------------------------------------

class TestInteractiveModeUpdate:
    def test_update_title_success(self, capsys: pytest.CaptureFixture) -> None:
        # add task, then update title only (leave description blank)
        exit_code = _run(["1", "Old title", "", "5", "1", "New title", "", "7"])

        out = capsys.readouterr().out
        assert exit_code == 0
        assert "updated successfully" in out

    def test_update_description_success(self, capsys: pytest.CaptureFixture) -> None:
        # add task, then update description only (leave title blank)
        exit_code = _run(["1", "My task", "", "5", "1", "", "New desc", "7"])

        out = capsys.readouterr().out
        assert exit_code == 0
        assert "updated successfully" in out

    def test_update_no_fields_shows_error(
        self, capsys: pytest.CaptureFixture
    ) -> None:
        # provide neither title nor description → error → loop back → exit
        exit_code = _run(["1", "My task", "", "5", "1", "", "", "7"])

        out = capsys.readouterr().out
        assert exit_code == 0
        assert "At least one field" in out

    def test_update_non_numeric_id_shows_error(
        self, capsys: pytest.CaptureFixture
    ) -> None:
        exit_code = _run(["5", "abc", "7"])

        assert exit_code == 0
        assert "Invalid task ID" in capsys.readouterr().out


# ---------------------------------------------------------------------------
# Choice 6 — Delete task
# ---------------------------------------------------------------------------

class TestInteractiveModeDelete:
    def test_delete_success(self, capsys: pytest.CaptureFixture) -> None:
        exit_code = _run(["1", "Delete me", "", "6", "1", "7"])

        out = capsys.readouterr().out
        assert exit_code == 0
        assert "deleted successfully" in out

    def test_delete_non_numeric_id_shows_error(
        self, capsys: pytest.CaptureFixture
    ) -> None:
        exit_code = _run(["6", "abc", "7"])

        assert exit_code == 0
        assert "Invalid task ID" in capsys.readouterr().out

    def test_delete_invalid_id_shows_error(
        self, capsys: pytest.CaptureFixture
    ) -> None:
        # handle_delete prints "Error: ..." to stderr
        exit_code = _run(["6", "99", "7"])

        assert exit_code == 0
        assert "not found" in capsys.readouterr().err.lower()


# ---------------------------------------------------------------------------
# Outer except Exception (line 170-171)
# ---------------------------------------------------------------------------

class TestInteractiveModeUnexpectedException:
    def test_unexpected_exception_is_caught_and_loop_continues(
        self, capsys: pytest.CaptureFixture
    ) -> None:
        # Patch handle_list to raise an unexpected error; loop should survive
        with patch.object(
            main_module, "handle_list", side_effect=RuntimeError("boom")
        ):
            exit_code = _run(["2", "7"])

        captured = capsys.readouterr()
        assert exit_code == 0
        assert "boom" in captured.err


# ---------------------------------------------------------------------------
# -i / --interactive flag wires to interactive_mode
# ---------------------------------------------------------------------------

class TestInteractiveModeFlag:
    def test_interactive_flag_launches_interactive_mode(
        self, capsys: pytest.CaptureFixture
    ) -> None:
        with patch("builtins.input", side_effect=["7"]):
            exit_code = main(["-i"])

        assert exit_code == 0
        assert "Goodbye" in capsys.readouterr().out
