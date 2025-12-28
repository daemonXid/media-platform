"""
⏱️ Task Manager

Taskiq integration for background task processing.
"""

import logging
import os
from collections.abc import Callable
from functools import wraps

logger = logging.getLogger(__name__)

# Taskiq broker - lazy initialization
_broker = None


def get_broker():
    """Get or create the Taskiq broker."""
    global _broker

    if _broker is None:
        try:
            from taskiq_redis import ListQueueBroker

            redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
            _broker = ListQueueBroker(redis_url)
            logger.info(f"Taskiq broker initialized with Redis: {redis_url}")
        except ImportError:
            logger.warning("taskiq-redis not installed, using in-memory broker")
            from taskiq import InMemoryBroker

            _broker = InMemoryBroker()

    return _broker


def background_task(func: Callable) -> Callable:
    """
    Decorator to make a function run as a background task.

    Usage:
        @background_task
        async def send_email(to: str, subject: str):
            # Long-running task
            pass

        # Call normally or kick to background
        await send_email.kiq(to="user@example.com", subject="Hello")
    """
    broker = get_broker()

    @wraps(func)
    async def wrapper(*args, **kwargs):
        return await func(*args, **kwargs)

    # Register with Taskiq
    return broker.task(func)


def retry_task(
    max_retries: int = 3,
    wait_seconds: float = 1.0,
    exponential: bool = True,
) -> Callable:
    """
    Decorator for task retry logic using Tenacity.

    Args:
        max_retries: Maximum number of retry attempts
        wait_seconds: Initial wait time between retries
        exponential: Use exponential backoff

    Usage:
        @retry_task(max_retries=5, wait_seconds=2)
        async def flaky_api_call():
            # May fail sometimes
            pass
    """

    def decorator(func: Callable) -> Callable:
        try:
            from tenacity import retry, stop_after_attempt, wait_exponential, wait_fixed

            wait_strategy = (
                wait_exponential(multiplier=wait_seconds, min=1, max=60) if exponential else wait_fixed(wait_seconds)
            )

            return retry(
                stop=stop_after_attempt(max_retries),
                wait=wait_strategy,
            )(func)
        except ImportError:
            logger.warning("tenacity not installed, retry decorator disabled")
            return func

    return decorator
