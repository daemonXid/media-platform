"""
📋 Audit Interface

Public API for audit logging.
"""

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from django.contrib.auth import get_user_model
    from django.http import HttpRequest

    from .models import AuditLog

    User = get_user_model()


def log_action(
    user: "User | None",
    action: str,
    description: str = "",
    resource_type: str = "",
    resource_id: str = "",
    request: "HttpRequest | None" = None,
    extra_data: dict[str, Any] | None = None,
) -> "AuditLog":
    """
    Log an audit action.

    Args:
        user: User performing the action (can be None for anonymous)
        action: Action type (create, read, update, delete, login, logout, etc.)
        description: Human-readable description
        resource_type: Type of resource affected
        resource_id: ID of resource affected
        request: Optional request for IP/user-agent extraction
        extra_data: Additional JSON data to store

    Returns:
        Created AuditLog instance
    """
    from .models import AuditLog

    ip_address = None
    user_agent = ""

    if request:
        ip_address = _get_client_ip(request)
        user_agent = request.META.get("HTTP_USER_AGENT", "")[:500]

    return AuditLog.objects.create(
        user=user,
        action=action,
        description=description,
        resource_type=resource_type,
        resource_id=str(resource_id),
        ip_address=ip_address,
        user_agent=user_agent,
        extra_data=extra_data or {},
    )


def get_user_actions(user: "User", limit: int = 50):
    """Get recent audit logs for a user."""
    from .models import AuditLog

    return AuditLog.objects.filter(user=user)[:limit]


def get_resource_history(resource_type: str, resource_id: str, limit: int = 50):
    """Get audit history for a specific resource."""
    from .models import AuditLog

    return AuditLog.objects.filter(
        resource_type=resource_type,
        resource_id=str(resource_id),
    )[:limit]


def _get_client_ip(request: "HttpRequest") -> str | None:
    """Extract client IP from request."""
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        return x_forwarded_for.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR")


__all__ = [
    "get_resource_history",
    "get_user_actions",
    "log_action",
]
