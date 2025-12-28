# 📋 DAEMON Module: Audit (`custom.audit`)

> Comprehensive Action Logging System.

## 🎯 Purpose

Track and record sensitive actions (logins, model changes, exports) for security and compliance.

## ✨ Key Features

- **Automatic Logging**: Can be hooked into `django-lifecycle`.
- **Admin View**: Searchable logs in the admin panel.

## 🏗️ Portability

Drop-in module from DAEMON-ABYSS.

## 📝 Usage

```python
from modules.base.audit.interface import log_action

log_action(user, "resource_created", {"id": 123})
```
