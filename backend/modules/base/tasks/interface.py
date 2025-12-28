"""
⏱️ Tasks Interface

Public API for background task management.
"""

import logging
from collections.abc import Callable
from typing import Any

logger = logging.getLogger(__name__)


async def enqueue(task_func: Callable, *args, **kwargs) -> Any:
    """
    Enqueue a task for background execution.

    Args:
        task_func: The task function (decorated with @background_task)
        *args, **kwargs: Arguments to pass to the task

    Returns:
        Task result handle

    Usage:
        from modules.base.tasks.interface import enqueue

        result = await enqueue(send_email, to="user@example.com")
    """
    try:
        # If it's a Taskiq task, use kiq()
        if hasattr(task_func, "kiq"):
            return await task_func.kiq(*args, **kwargs)
        # Otherwise, run synchronously
        return await task_func(*args, **kwargs)
    except Exception as e:
        logger.error(f"Failed to enqueue task: {e}")
        raise


def run_sync(task_func: Callable, *args, **kwargs) -> Any:
    """
    Run a task synchronously (for testing or simple cases).

    Args:
        task_func: The task function
        *args, **kwargs: Arguments

    Returns:
        Task result
    """
    import asyncio

    if asyncio.iscoroutinefunction(task_func):
        return asyncio.run(task_func(*args, **kwargs))
    return task_func(*args, **kwargs)


# Re-export decorators
from .manager import background_task, retry_task

__all__ = [
    "background_task",
    "enqueue",
    "retry_task",
    "run_sync",
]
