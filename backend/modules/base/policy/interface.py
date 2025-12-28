"""
🔑 Public Interface - RBAC Module

Import from here to use RBAC in other modules.

Usage:
    from modules.rbac.interface import (
        has_permission,
        require_permission,
        get_user_roles,
        PolicyEngine,
        PermissionAuth,
    )
"""

from .engine import (
    PermissionAuth,
    PolicyEngine,
    get_engine,
    get_user_roles,
    has_permission,
    require_permission,
)

__all__ = [
    "PermissionAuth",
    "PolicyEngine",
    "get_engine",
    "get_user_roles",
    "has_permission",
    "require_permission",
]
