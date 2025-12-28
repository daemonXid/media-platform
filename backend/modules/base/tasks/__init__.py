"""
⏱️ Tasks Module

Background task queue with Taskiq integration.

Features:
- Async task execution
- Task scheduling (cron-like)
- Retry logic with Tenacity
- Task status tracking

Usage:
    from modules.base.tasks.interface import enqueue, schedule

    # Enqueue a task
    result = await enqueue(send_email, to="user@example.com")

    # Schedule recurring task
    schedule(cleanup_old_files, cron="0 0 * * *")  # Daily at midnight
"""
