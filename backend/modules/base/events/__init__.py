"""
📢 Events Module

Domain Events pattern via Django Signals.
Loose coupling between modules.

Usage:
    from modules.events.interface import domain_event, user_created

    # Define
    payment_done = domain_event("payment_done")

    # Emit
    payment_done.send(sender=Payment, id=123)
"""
