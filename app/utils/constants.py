from __future__ import annotations

APP_NAME = "AI Smart E-Commerce MAS"
DEFAULT_CATEGORY = "laptop"
DEFAULT_MAX_RESULTS = 5

SUPPORTED_CATEGORIES = {"laptop", "phone"}
# These keywords are used by the DelegatorAgent to infer user intent and constraints from the query.
PRICE_KEYWORDS = {
    "budget": ["budget", "cheap", "affordable", "low price", "under"],
    "premium": ["premium", "best", "high-end", "powerful"],
}

USE_CASE_KEYWORDS = {
    "student": ["student", "study", "university", "school"],
    "coding": ["coding", "developer", "programming", "software"],
    "office": ["office", "work", "business"],
    "gaming": ["gaming", "games"],
    "camera": ["camera", "photo", "photography"],
    "battery": ["battery", "long battery", "battery life"],
}

SORT_WEIGHTS = {
    "rating": 0.35,
    "ram_gb": 0.20,
    "storage_gb": 0.15,
    "battery_hours": 0.10,
    "battery_mah": 0.10,
    "price": 0.10,
}

LOG_DIR = "logs"
SYSTEM_LOG_FILE = "logs/system.log"
ERROR_LOG_FILE = "logs/errors.log"