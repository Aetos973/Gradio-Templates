import os
import json
import hashlib
import datetime

def load_json(filepath):
    """Safely load JSON from file."""
    if not os.path.exists(filepath):
        return {}
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

def save_json(filepath, data):
    """Save JSON to file with safe encoding."""
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def hash_string(value: str) -> str:
    """Generate SHA256 hash for a string."""
    return hashlib.sha256(value.encode()).hexdigest()

def timestamp() -> str:
    """Return ISO8601 UTC timestamp."""
    return datetime.datetime.utcnow().isoformat()

def clamp(value, min_val, max_val):
    """Clamp a number into a safe range."""
    return max(min_val, min(value, max_val))

