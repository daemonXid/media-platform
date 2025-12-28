"""
🔐 DAEMON-ONE Policy Engine

Policy-as-Code implementation for unified RBAC across all modules.
Reads from roles.yaml and provides permission checking utilities.

Usage:
    from core.policies import PolicyEngine, has_permission, require_permission

    # Check permission
    if has_permission(user, "shorts:create"):
        create_short(...)

    # Decorator
    @require_permission("blog:publish")
    def publish_post(request, post_id):
        ...

    # In Django Ninja
    @api.post("/shorts/", auth=require_permission("shorts:create"))
    def create_short(request, data: ShortSchema):
        ...
"""

from __future__ import annotations

import functools
from collections.abc import Callable
from pathlib import Path
from typing import TYPE_CHECKING, Any

import yaml

if TYPE_CHECKING:
    from django.contrib.auth.models import AbstractUser


# ============================================
# 📋 Policy Engine
# ============================================


class PolicyEngine:
    """
    Central policy engine that loads and evaluates RBAC rules.
    """

    _instance: PolicyEngine | None = None
    _config: dict | None = None

    def __new__(cls) -> PolicyEngine:
        """Singleton pattern."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if self._config is None:
            self._load_config()

    def _load_config(self) -> None:
        """Load roles.yaml configuration."""
        config_path = Path(__file__).parent / "roles.yaml"

        if not config_path.exists():
            raise FileNotFoundError(f"Policy config not found: {config_path}")

        with open(config_path, encoding="utf-8") as f:
            self._config = yaml.safe_load(f)

        # Build permission cache with inheritance
        self._permission_cache: dict[str, set[str]] = {}
        self._build_permission_cache()

    def _build_permission_cache(self) -> None:
        """Build flattened permission sets with inheritance."""
        roles = self._config.get("roles", {})
        hierarchy = self._config.get("hierarchy", {})

        def get_all_permissions(role_name: str, visited: set | None = None) -> set[str]:
            """Recursively get all permissions including inherited."""
            if visited is None:
                visited = set()

            if role_name in visited:
                return set()  # Prevent circular inheritance
            visited.add(role_name)

            permissions = set()

            # Direct permissions
            role = roles.get(role_name, {})
            for perm in role.get("permissions", []):
                permissions.add(perm)

            # Inherited permissions
            if role_name in hierarchy:
                for parent_role in hierarchy[role_name].get("inherits", []):
                    permissions.update(get_all_permissions(parent_role, visited.copy()))

            return permissions

        for role_name in roles:
            self._permission_cache[role_name] = get_all_permissions(role_name)

    def get_role_permissions(self, role: str) -> set[str]:
        """Get all permissions for a role (including inherited)."""
        return self._permission_cache.get(role, set())

    def check_permission(self, user_roles: list[str], permission: str) -> bool:
        """
        Check if any of the user's roles has the required permission.

        Args:
            user_roles: List of role names assigned to user
            permission: Permission to check (e.g., "shorts:create")

        Returns:
            True if permission is granted
        """
        module, action = self._parse_permission(permission)

        for role in user_roles:
            role_permissions = self.get_role_permissions(role)

            for perm in role_permissions:
                if self._matches_permission(perm, module, action):
                    return True

        return False

    def _parse_permission(self, permission: str) -> tuple[str, str]:
        """Parse 'module:action' format."""
        if ":" not in permission:
            return permission, "*"
        parts = permission.split(":", 1)
        return parts[0], parts[1]

    def _matches_permission(self, rule: str, module: str, action: str) -> bool:
        """Check if a permission rule matches the requested module:action."""
        rule_module, rule_action = self._parse_permission(rule)

        # Wildcard checks
        if rule_module == "*" and rule_action == "*":
            return True
        if rule_module == module and rule_action == "*":
            return True
        if rule_module == "*" and rule_action == action:
            return True

        # Exact match
        if rule_module == module:
            # Check if action is in comma-separated list
            allowed_actions = [a.strip() for a in rule_action.split(",")]
            if action in allowed_actions or "*" in allowed_actions:
                return True

        return False

    def get_default_role(self, context: str = "new_user") -> str:
        """Get default role for a given context."""
        defaults = self._config.get("defaults", {})
        return defaults.get(context, "viewer")

    def list_roles(self) -> list[dict]:
        """List all roles with descriptions."""
        roles = self._config.get("roles", {})
        return [{"name": name, "description": role.get("description", "")} for name, role in roles.items()]

    def list_modules(self) -> list[dict]:
        """List all modules with their actions."""
        modules = self._config.get("modules", {})
        return [
            {"name": name, "description": module.get("description", ""), "actions": module.get("actions", [])}
            for name, module in modules.items()
        ]


# ============================================
# 🛠️ Helper Functions
# ============================================

# Global engine instance
_engine: PolicyEngine | None = None


def get_engine() -> PolicyEngine:
    """Get or create policy engine singleton."""
    global _engine
    if _engine is None:
        _engine = PolicyEngine()
    return _engine


def get_user_roles(user: AbstractUser) -> list[str]:
    """
    Get roles for a user.

    Override this function to integrate with your user model.
    Default implementation checks for 'roles' attribute or field.
    """
    if hasattr(user, "roles"):
        roles = user.roles
        if callable(roles):
            roles = roles()
        if isinstance(roles, str):
            return [roles]
        return list(roles)

    # Fallback: check is_superuser
    if hasattr(user, "is_superuser") and user.is_superuser:
        return ["superadmin"]

    # Default role
    return [get_engine().get_default_role()]


def has_permission(user: AbstractUser, permission: str) -> bool:
    """
    Check if user has the specified permission.

    Args:
        user: Django user instance
        permission: Permission string (e.g., "shorts:create")

    Returns:
        True if user has permission

    Example:
        if has_permission(request.user, "blog:publish"):
            publish_post(post)
    """
    if not user or not user.is_authenticated:
        return False

    roles = get_user_roles(user)
    return get_engine().check_permission(roles, permission)


def require_permission(permission: str):
    """
    Decorator to require a permission for a view.

    Works with:
    - Django views
    - Django Ninja endpoints

    Example:
        @require_permission("shorts:create")
        def create_short(request):
            ...
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(request, *args, **kwargs):
            if not has_permission(request.user, permission):
                from django.http import HttpResponseForbidden

                return HttpResponseForbidden(f"Permission denied: {permission}")
            return func(request, *args, **kwargs)

        return wrapper

    return decorator


# ============================================
# 🎫 Django Ninja Auth Class
# ============================================


class PermissionAuth:
    """
    Django Ninja authentication class for permission-based access.

    Usage:
        from core.policies import PermissionAuth

        @api.post("/shorts/", auth=PermissionAuth("shorts:create"))
        def create_short(request, data: ShortSchema):
            ...
    """

    def __init__(self, permission: str):
        self.permission = permission

    def __call__(self, request) -> Any:
        if not request.user or not request.user.is_authenticated:
            return None

        if has_permission(request.user, self.permission):
            return request.user

        return None


# ============================================
# 📦 Module Exports
# ============================================

__all__ = [
    "PermissionAuth",
    "PolicyEngine",
    "get_engine",
    "get_user_roles",
    "has_permission",
    "require_permission",
]
