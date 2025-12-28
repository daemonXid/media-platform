"""
🔑 Public Interface - Events Module

Import from here to use domain events.

Usage:
    from modules.events.interface import (
        domain_event,
        user_created,
        user_updated,
        entity_created,
    )
"""

from .events import (
    domain_event,
    entity_created,
    entity_deleted,
    entity_updated,
    user_created,
    user_deleted,
    user_logged_in,
    user_updated,
)

__all__ = [
    "domain_event",
    "entity_created",
    "entity_deleted",
    "entity_updated",
    "user_created",
    "user_deleted",
    "user_logged_in",
    "user_updated",
]
