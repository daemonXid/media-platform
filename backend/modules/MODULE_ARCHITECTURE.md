# 📦 Module Architecture v4.0

> This document describes the DAEMON-ONE module structure and conventions.

## Directory Structure

```text
backend/modules/
├── __init__.py
├── MODULE_ARCHITECTURE.md
│
├── base/                      # 📍 Foundational Pillars (Always Included)
│   # --- Technical Foundation ---
│   ├── core/                  # Landing Page, Base Templates, Base Models
│   ├── tasks/                 # Async Background Workers (Taskiq)
│   ├── media/                 # File & Storage Management
│   ├── registry/              # Service Discovery & Plugin System
│   │
│   # --- Stability & Defense ---
│   ├── health/                # Liveness/Readiness probes
│   ├── monitoring/            # Advanced Observability (Logfire)
│   ├── backup/                # Data Resilience & Snapshots
│   ├── security/              # App Hardening & Anti-Bot
│   │
│   # --- Identity & Security ---
│   ├── accounts/              # User Authentication (Allauth)
│   ├── policy/                # Policy-as-Code & Advanced AuthZ
│   ├── audit/                 # Action Logging & Compliance
│   ├── legal/                 # ToS, Privacy, Consent Management
│   │
│   # --- Business & Growth ---
│   ├── analytics/             # Admin Performance Dashboard
│   ├── seo/                   # Search Engine Optimization
│   ├── marketing/             # UTM Tracking & Growth Engines
│   │
│   # --- Experience & Comm ---
│   ├── ux/                    # Global Design System (Animation/Scroll)
│   ├── notifications/         # Multi-channel Alert System
│   ├── events/                # Internal Domain Event Bus
│   ├── settings/              # Runtime Site Configuration
│   └── manual/                # Self-Documenting Engine (Living Manual)
│
├── ai/                        # 🤖 AI-First Layer
│   ├── providers/             # AI Abstraction (HF, DS, OR)
│   │   └── agents/            # Pydantic AI Persona Agents
│   └── chatbot/               # Project-aware AI sidebar assistant
│
└── custom/                    # 🔌 Plug & Play (From ABYSS)
    └── ...                    # Feature-specific modules
```

## Module Categories

### 1. base/ - Foundational Pillars

The complete infrastructure required for a production-ready SaaS. The `base` category is extensible, hosting modules that provide shared services, security, growth, or infrastructure.

### 2. ai/ - AI-First Intelligence

Encapsulates AI logic and provider abstractions. **AI Agents** focus on specialized personas.

### 3. custom/ - Vertical Feature Slices

Business-specific features that can be added or removed. Each is a self-contained vertical slice.

## Interface Pattern

**Rule: Only import from `interface.py`** to ensure loose coupling.

## Portability Requirement

Every module MUST contain its own `README.md` for zero-friction portability.
