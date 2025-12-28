# 🔔 DAEMON Module: Events (`base.events`)

> Domain Event System for Loose Coupling.

## 🎯 Purpose

Implements an internal event bus to allow modules to communicate without direct dependencies.

## ✨ Key Features

- **Signal-like Bus**: Decoupled module communication.
- **Async Support**: Can be hooked into `tasks` for background execution.

## 🏗️ Portability

Completely self-contained.

## 📝 Usage

```python
from modules.base.events.interface import dispatch_event

dispatch_event("user_registered", {"email": "xid@daemon.dev"})
```
