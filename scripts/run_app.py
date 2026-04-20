from __future__ import annotations

import os
import sys
from pathlib import Path


def add_project_root_to_path() -> Path:
    """
    Add the project root directory to sys.path so that `app` imports work.

    Returns:
        Path: The resolved project root path.
    """
    project_root = Path(__file__).resolve().parent.parent
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
    return project_root


def main() -> int:
    """
    Entry point for running the MAS application.

    Returns:
        int: Exit status code.
    """
    project_root = add_project_root_to_path()

    try:
        from app.main import main as app_main
    except ImportError as exc:
        print("Failed to import app.main.")
        print("Make sure the project structure is correct and app/main.py exists.")
        print(f"Import error: {exc}")
        return 1

    print(f"Project root: {project_root}")
    print("Starting AI Smart E-Commerce MAS...\n")

    try:
        app_main()
        return 0
    except KeyboardInterrupt:
        print("\nExecution interrupted by user.")
        return 130
    except Exception as exc:  # pylint: disable=broad-except
        print(f"Application failed: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())