"""
🏥 Health Module - Public Interface

Import from here only:
    from modules.base.health.interface import check_health, is_ready
"""

from .views import _check_cache, _check_database


def check_health() -> dict:
    """
    Check overall system health.

    Returns:
        dict with status and individual check results
    """
    checks = {
        "database": _check_database(),
        "cache": _check_cache(),
    }

    all_healthy = all(check["status"] == "ok" for check in checks.values())

    return {
        "status": "healthy" if all_healthy else "unhealthy",
        "checks": checks,
    }


def is_ready() -> bool:
    """
    Quick check if system is ready for traffic.

    Returns:
        True if all checks pass
    """
    result = check_health()
    return result["status"] == "healthy"


def is_alive() -> bool:
    """
    Quick liveness check.

    Always returns True if this code executes.
    """
    return True


__all__ = ["check_health", "is_alive", "is_ready"]
