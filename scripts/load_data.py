from __future__ import annotations

from pathlib import Path

from scripts.default_laptops import DEFAULT_LAPTOPS
from scripts.default_phones import DEFAULT_PHONES
from app.utils.helpers import save_json_file


def main() -> int:
    """
    Generate default dataset files for the app.
    """
    project_root = Path(__file__).resolve().parent.parent
    data_dir = project_root / "app" / "data"

    laptops_path = data_dir / "laptops.json"
    phones_path = data_dir / "phones.json"

    save_json_file(laptops_path, DEFAULT_LAPTOPS)
    save_json_file(phones_path, DEFAULT_PHONES)

    print(f"Created: {laptops_path}")
    print(f"Created: {phones_path}")
    print("Default datasets loaded successfully.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())