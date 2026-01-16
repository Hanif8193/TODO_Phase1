"""Main entry point for the Todo App CLI.

This module sets up the argument parser and dispatches commands
to the appropriate handler functions.
"""

import argparse
import sys

from src.services.task_service import TaskService
from src.cli.commands import (
    handle_add,
    handle_list,
    handle_done,
    handle_undone,
    handle_update,
    handle_delete,
)


# Global service instance for the CLI session
_service: TaskService | None = None


def get_service() -> TaskService:
    """Get or create the global TaskService instance.

    Returns:
        The global TaskService instance.
    """
    global _service
    if _service is None:
        _service = TaskService()
    return _service


def create_parser() -> argparse.ArgumentParser:
    """Create and configure the argument parser.

    Returns:
        Configured ArgumentParser with all subcommands.
    """
    parser = argparse.ArgumentParser(
        prog="todo",
        description="Phase I In-Memory CLI Todo App",
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Add command
    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("title", help="Task title")
    add_parser.add_argument(
        "-d", "--description", default="", help="Task description"
    )

    # List command
    subparsers.add_parser("list", help="List all tasks")

    # Done command
    done_parser = subparsers.add_parser("done", help="Mark a task as complete")
    done_parser.add_argument("id", type=int, help="Task ID")

    # Undone command
    undone_parser = subparsers.add_parser("undone", help="Mark a task as pending")
    undone_parser.add_argument("id", type=int, help="Task ID")

    # Update command
    update_parser = subparsers.add_parser("update", help="Update a task")
    update_parser.add_argument("id", type=int, help="Task ID")
    update_parser.add_argument("-t", "--title", help="New task title")
    update_parser.add_argument("-d", "--description", help="New task description")

    # Delete command
    delete_parser = subparsers.add_parser("delete", help="Delete a task")
    delete_parser.add_argument("id", type=int, help="Task ID")

    return parser


def main(args: list[str] | None = None) -> int:
    """Main entry point for the CLI.

    Args:
        args: Command line arguments (defaults to sys.argv[1:]).

    Returns:
        Exit code (0 for success, 1 for user error, 2 for system error).
    """
    parser = create_parser()
    parsed_args = parser.parse_args(args)

    if parsed_args.command is None:
        parser.print_help()
        return 0

    service = get_service()

    try:
        if parsed_args.command == "add":
            return handle_add(
                service, parsed_args.title, parsed_args.description
            )
        elif parsed_args.command == "list":
            return handle_list(service)
        elif parsed_args.command == "done":
            return handle_done(service, parsed_args.id)
        elif parsed_args.command == "undone":
            return handle_undone(service, parsed_args.id)
        elif parsed_args.command == "update":
            if parsed_args.title is None and parsed_args.description is None:
                print(
                    "Error: At least one of --title or --description is required",
                    file=sys.stderr,
                )
                return 1
            return handle_update(
                service,
                parsed_args.id,
                title=parsed_args.title,
                description=parsed_args.description,
            )
        elif parsed_args.command == "delete":
            return handle_delete(service, parsed_args.id)
        else:
            parser.print_help()
            return 0
    except Exception as e:
        print(f"Error: Unexpected error - {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
