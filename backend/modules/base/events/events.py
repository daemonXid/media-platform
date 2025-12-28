"""
🎯 Domain Events - Event Bus Pattern

This module provides Django Signals-based event system for loose coupling.
Modules can emit events without knowing who listens.

Usage:
    # Define event (in your_module/signals.py)
    from modules.daemon.events import domain_event
    payment_completed = domain_event("payment_completed")

    # Emit event (in your_module/services.py)
    payment_completed.send(sender=Payment, payment_id=123, amount=10000)

    # Listen to event (in other_module/receivers.py)
    from your_module.signals import payment_completed

    @receiver(payment_completed)
    def on_payment_completed(sender, payment_id, amount, **kwargs):
        log_analytics(payment_id, amount)
"""

from django.dispatch import Signal


def domain_event(name: str) -> Signal:
    """
    Create a named domain event (Django Signal).

    Args:
        name: Event name for debugging/logging

    Returns:
        Django Signal object

    Example:
        # signals.py
        user_registered = domain_event("user_registered")
        order_placed = domain_event("order_placed")
    """
    signal = Signal()
    signal._name = name  # For debugging
    return signal


# =============================================================================
# 📢 Core Domain Events (Cross-cutting)
# =============================================================================

# User lifecycle events
user_created = domain_event("user_created")
user_updated = domain_event("user_updated")
user_deleted = domain_event("user_deleted")
user_logged_in = domain_event("user_logged_in")

# Generic CRUD events (can be used by any module)
entity_created = domain_event("entity_created")
entity_updated = domain_event("entity_updated")
entity_deleted = domain_event("entity_deleted")
