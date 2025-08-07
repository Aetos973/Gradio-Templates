import time
import uuid
from typing import Dict, Optional
from threading import Lock

# ───── Global Progress State ───── #
# In-memory tracker (could be swapped for Redis or DB later)
_task_store: Dict[str, Dict] = {}
_lock = Lock()


# ───── Tracker Utilities ───── #
def create_task(label: str = "Processing...") -> str:
    """Create a new task and return its unique ID."""
    task_id = str(uuid.uuid4())
    with _lock:
        _task_store[task_id] = {
            "label": label,
            "status": "pending",  # "pending", "in_progress", "success", "error"
            "progress": 0,
            "message": "",
            "start_time": time.time(),
        }
    return task_id


def update_task(task_id: str, progress: int = 0, message: str = "", status: Optional[str] = None):
    """Update task progress, message, or status."""
    with _lock:
        task = _task_store.get(task_id)
        if not task:
            return

        task["progress"] = min(100, max(0, progress))
        task["message"] = message or task["message"]
        if status:
            task["status"] = status


def complete_task(task_id: str, message: str = "Done!"):
    update_task(task_id, progress=100, message=message, status="success")


def error_task(task_id: str, message: str = "Something went wrong."):
    update_task(task_id, progress=100, message=message, status="error")


def get_task_status(task_id: str) -> Dict:
    """Get current state of a task."""
    with _lock:
        return _task_store.get(task_id, {
            "label": "Unknown Task",
            "status": "not_found",
            "progress": 0,
            "message": "",
        })


# ───── Optional: Task Decorator (for auto-tracking) ───── #
def track_action(label="Processing..."):
    """
    Decorator to automatically create and update task progress
    for any long-running function.
    """
    def wrapper(func):
        def inner(*args, **kwargs):
            task_id = create_task(label)
            try:
                update_task(task_id, 10, "Started...", "in_progress")
                result = func(*args, **kwargs, task_id=task_id)
                complete_task(task_id, "Completed successfully.")
                return result
            except Exception as e:
                error_task(task_id, f"Failed: {e}")
                raise e
        return inner
    return wrapper
