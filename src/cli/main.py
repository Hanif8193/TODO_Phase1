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


def interactive_mode() -> int:
    """Run the app in interactive menu mode.

    Tasks persist throughout the session until the user exits.

    Returns:
        Exit code (0 for success).
    """
    service = get_service()

    while True:
        print("\n" + "="*50)
        print("TODO APP - INTERACTIVE MODE")
        print("="*50)
        print("1. Add task")
        print("2. List tasks")
        print("3. Mark task as done")
        print("4. Mark task as undone")
        print("5. Update task")
        print("6. Delete task")
        print("7. Exit")
        print("="*50)

        choice = input("\nSelect an option (1-7): ").strip()

        try:
            if choice == "1":
                title = input("Enter task title: ").strip()
                if not title:
                    print("Error: Title cannot be empty")
                    continue
                description = input("Enter task description (optional): ").strip()
                handle_add(service, title, description)

            elif choice == "2":
                handle_list(service)

            elif choice == "3":
                task_id = input("Enter task ID to mark as done: ").strip()
                try:
                    handle_done(service, int(task_id))
                except ValueError:
                    print("Error: Invalid task ID. Must be a number.")

            elif choice == "4":
                task_id = input("Enter task ID to mark as undone: ").strip()
                try:
                    handle_undone(service, int(task_id))
                except ValueError:
                    print("Error: Invalid task ID. Must be a number.")

            elif choice == "5":
                task_id = input("Enter task ID to update: ").strip()
                try:
                    task_id = int(task_id)
                    print("Leave blank to keep current value")
                    title = input("Enter new title (optional): ").strip()
                    description = input("Enter new description (optional): ").strip()

                    if not title and not description:
                        print("Error: At least one field must be provided")
                        continue

                    handle_update(
                        service,
                        task_id,
                        title=title if title else None,
                        description=description if description else None
                    )
                except ValueError:
                    print("Error: Invalid task ID. Must be a number.")

            elif choice == "6":
                task_id = input("Enter task ID to delete: ").strip()
                try:
                    handle_delete(service, int(task_id))
                except ValueError:
                    print("Error: Invalid task ID. Must be a number.")

            elif choice == "7":
                print("\nGoodbye!")
                return 0

            else:
                print("Error: Invalid option. Please select 1-7.")

        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            return 0
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)


def main(args: list[str] | None = None) -> int:
    """Main entry point for the CLI.

    Args:
        args: Command line arguments (defaults to sys.argv[1:]).

    Returns:
        Exit code (0 for success, 1 for user error, 2 for system error).
    """
    parser = create_parser()

    # Add interactive mode flag
    parser.add_argument(
        "-i", "--interactive",
        action="store_true",
        help="Run in interactive mode with persistent session"
    )

    parsed_args = parser.parse_args(args)

    # Check for interactive mode first
    if parsed_args.interactive:
        return interactive_mode()

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
