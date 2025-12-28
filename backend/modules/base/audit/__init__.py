"""
📋 Audit Module

Audit logging system for tracking user actions.

Features:
- Automatic action logging via middleware
- Manual logging via interface
- Query audit trail by user, action, or resource
- Retention policy support

Usage:
    from modules.base.audit.interface import log_action, get_user_actions

    log_action(user, "login", "User logged in from IP: x.x.x.x")
"""
