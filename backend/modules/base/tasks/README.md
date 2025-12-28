# ⏱️ DAEMON Module: Tasks (`custom.tasks`)

> Async Background Task Queue using Taskiq.

## 🎯 Purpose

Execute long-running processes (email, AI generation, reports) without blocking the HTTP request/response cycle.

## ✨ Key Features

- **Taskiq Integration**: A modern, high-performance alternative to Celery.
- **Redis Backend**: Uses Redis for task orchestration.

## 🏗️ Portability

Drop-in module from DAEMON-ABYSS. Requires a Redis server.

## 📝 Usage

```python
from modules.custom.tasks.interface import enqueue

enqueue("my_task_name", data={"id": 1})
```
