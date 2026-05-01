from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def main() -> int:
    """
    Run the project's pytest suite.

    Returns:
        int: Exit status code from pytest.
    """
    project_root = Path(__file__).resolve().parent.parent
    tests_path = project_root / "tests"

    if not tests_path.exists():
        print("Tests directory not found.")
        return 1

    cmd = [sys.executable, "-m", "pytest", str(tests_path), "-v"]

    print("Running test suite...\n")
    print("Command:", " ".join(cmd))
    print()

    completed = subprocess.run(cmd, cwd=project_root, check=False)
    return completed.returncode


if __name__ == "__main__":
    raise SystemExit(main())