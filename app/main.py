from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml
from dotenv import load_dotenv

from app.crews.ecommerce_crew import EcommerceCrew
from app.utils.logger import get_logger, setup_logging

logger = get_logger(__name__)


def load_yaml_config(file_path: Path) -> dict[str, Any]:
    """
    Load a YAML configuration file.

    Args:
        file_path: Path to YAML config.

    Returns:
        dict[str, Any]: Parsed config dictionary.
    """
    if not file_path.exists():
        raise FileNotFoundError(f"Config file not found: {file_path}")

    with file_path.open("r", encoding="utf-8") as file:
        data = yaml.safe_load(file)

    if not isinstance(data, dict):
        raise ValueError(f"Invalid config format in: {file_path}")

    return data


def build_app_config(project_root: Path) -> dict[str, Any]:
    """
    Build the final app config from YAML files.

    Args:
        project_root: Project root directory.

    Returns:
        dict[str, Any]: Merged application config.
    """
    config_dir = project_root / "configs"

    app_config = load_yaml_config(config_dir / "app_config.yaml")
    agent_config = load_yaml_config(config_dir / "agent_config.yaml")

    merged = dict(app_config)
    merged["agents"] = agent_config.get("agents", {})
    merged["prompts"] = agent_config.get("prompts", {})
    merged["settings"] = agent_config.get("settings", {})

    return merged


def print_header() -> None:
    """
    Print application header.
    """
    print("=" * 68)
    print(" AI Smart E-Commerce MAS ".center(68, "="))
    print("=" * 68)
    print("Type your product query and get the best recommendation.\n")


def print_final_output(response: str) -> None:
    """
    Print final formatted output.
    """
    print("\n" + "=" * 68)
    print(" FINAL RECOMMENDATION ".center(68, "="))
    print("=" * 68)
    print(response)
    print("=" * 68 + "\n")


def print_errors(state: Any) -> None:
    """
    Print workflow errors if any.
    """
    if getattr(state, "errors", None):
        print("Errors:")
        for error in state.errors:
            print(f"- {error}")
        print()


def main() -> None:
    """
    Main CLI entrypoint.
    """
    project_root = Path(__file__).resolve().parent.parent
    load_dotenv(project_root / ".env")
    setup_logging()

    try:
        config = build_app_config(project_root)
    except Exception as exc:  # pylint: disable=broad-except
        logger.exception("Failed to load configuration: %s", exc)
        print(f"Configuration error: {exc}")
        return

    crew = EcommerceCrew(config=config, project_root=project_root)

    print_header()

    while True:
        try:
            query = input("Enter your query (or type 'exit'): ").strip()
        except KeyboardInterrupt:
            print("\nExiting application.")
            break

        if not query:
            print("Please enter a valid query.\n")
            continue

        if query.lower() in {"exit", "quit"}:
            print("Goodbye.")
            break

        try:
            result = crew.run(query)
            response = result["response"]
            state = result["state"]

            print_final_output(response)
            print_errors(state)

        except Exception as exc:  # pylint: disable=broad-except
            logger.exception("Application runtime error: %s", exc)
            print(f"Application error: {exc}\n")


if __name__ == "__main__":
    main()