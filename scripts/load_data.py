from __future__ import annotations

from pathlib import Path

from app.utils.helpers import save_json_file

DEFAULT_LAPTOPS = [
    {
        "id": 1,
        "brand": "Lenovo",
        "model": "IdeaPad Slim 3",
        "category": "laptop",
        "price": 145000,
        "currency": "LKR",
        "ram_gb": 8,
        "storage_gb": 512,
        "storage_type": "SSD",
        "processor": "Intel Core i5 12th Gen",
        "display_size_inches": 15.6,
        "battery_hours": 8,
        "rating": 4.4,
        "weight_kg": 1.63,
        "use_case": ["student", "office", "coding"]
    },
    {
        "id": 2,
        "brand": "HP",
        "model": "15s",
        "category": "laptop",
        "price": 139000,
        "currency": "LKR",
        "ram_gb": 8,
        "storage_gb": 512,
        "storage_type": "SSD",
        "processor": "Intel Core i3 12th Gen",
        "display_size_inches": 15.6,
        "battery_hours": 7,
        "rating": 4.2,
        "weight_kg": 1.69,
        "use_case": ["student", "office"]
    },
    {
        "id": 3,
        "brand": "Dell",
        "model": "Inspiron 15",
        "category": "laptop",
        "price": 165000,
        "currency": "LKR",
        "ram_gb": 16,
        "storage_gb": 512,
        "storage_type": "SSD",
        "processor": "Intel Core i5 12th Gen",
        "display_size_inches": 15.6,
        "battery_hours": 8,
        "rating": 4.5,
        "weight_kg": 1.70,
        "use_case": ["coding", "office", "multitasking"]
    },
]

DEFAULT_PHONES = [
    {
        "id": 101,
        "brand": "Samsung",
        "model": "Galaxy A25",
        "category": "phone",
        "price": 92000,
        "currency": "LKR",
        "ram_gb": 8,
        "storage_gb": 256,
        "processor": "Exynos",
        "battery_mah": 5000,
        "camera_mp": 50,
        "rating": 4.4,
        "use_case": ["student", "daily", "camera"]
    },
    {
        "id": 102,
        "brand": "Xiaomi",
        "model": "Redmi Note 13",
        "category": "phone",
        "price": 85000,
        "currency": "LKR",
        "ram_gb": 8,
        "storage_gb": 256,
        "processor": "Snapdragon",
        "battery_mah": 5000,
        "camera_mp": 108,
        "rating": 4.3,
        "use_case": ["daily", "camera", "budget"]
    },
    {
        "id": 103,
        "brand": "Samsung",
        "model": "Galaxy A35",
        "category": "phone",
        "price": 118000,
        "currency": "LKR",
        "ram_gb": 8,
        "storage_gb": 256,
        "processor": "Exynos",
        "battery_mah": 5000,
        "camera_mp": 50,
        "rating": 4.6,
        "use_case": ["student", "daily", "premium-midrange"]
    },
]


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