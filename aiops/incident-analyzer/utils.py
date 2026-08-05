"""
PulseOps Utility Functions
"""

import json
from datetime import datetime
from typing import Any

# ==========================================================
# Timestamp
# ==========================================================

def current_timestamp() -> str:
    """
    Return current UTC timestamp.
    """
    return datetime.utcnow().isoformat()


# ==========================================================
# Severity Formatter
# ==========================================================

def normalize_severity(severity: str) -> str:
    """
    Normalize severity values.
    """

    if not severity:
        return "low"

    severity = severity.lower().strip()

    allowed = {
        "critical",
        "high",
        "medium",
        "low",
    }

    if severity in allowed:
        return severity

    return "low"


# ==========================================================
# Safe JSON
# ==========================================================

def safe_json(data: Any):
    """
    Convert object to JSON safely.
    """

    return json.loads(json.dumps(data, default=str))


# ==========================================================
# Success Response
# ==========================================================

def success_response(message: str, data=None):
    return {
        "success": True,
        "message": message,
        "data": data,
    }


# ==========================================================
# Error Response
# ==========================================================

def error_response(message: str):
    return {
        "success": False,
        "message": message,
    }


# ==========================================================
# Incident Status
# ==========================================================

def normalize_status(status: str) -> str:

    if not status:
        return "OPEN"

    status = status.upper()

    allowed = {
        "OPEN",
        "INVESTIGATING",
        "RESOLVED",
        "CLOSED",
    }

    if status in allowed:
        return status

    return "OPEN"