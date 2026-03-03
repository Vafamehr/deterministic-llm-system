from datetime import datetime


def get_current_time() -> dict:
    """
    Example deterministic tool.

    Returns current UTC time in ISO format.
    No side effects.
    No external calls.
    """
    return {
        "utc_time": datetime.now().isoformat()
    }