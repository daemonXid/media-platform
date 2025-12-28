# 😈 DAEMON-ONE v4.0

> **The AI-First Template** — Django Ninja HATEOAS Modular Polyglot Monolith

A production-ready, high-performance web application template built with **Hypermedia-Driven Architecture** and **AI Provider Abstraction**. Part of the **DAEMON System**.

[![MIT License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.12+](https://img.shields.io/badge/Python-3.12+-3776AB.svg)](https://www.python.org/)
[![Django 5](https://img.shields.io/badge/Django-5.x-092E20.svg)](https://www.djangoproject.com/)

---

## 🤖 AI Provider Strategy

```text
HuggingFace (Free) → DeepSeek (Quality/Korean) → OpenRouter (Multi-Model)
```

| Provider | Use Case | Cost |
| -------- | -------- | ---- |
| **HuggingFace** | Development, prototyping | 🟢 Free |
| **DeepSeek** | Production, Korean language | 🟡 Low |
| **OpenRouter** | Multi-model access (GPT-4, Claude, Gemini) | 🔴 Varies |

```python
from modules.ai.providers.interface import get_ai_client

client = get_ai_client()  # Auto-select based on AI_PROVIDER
response = client.complete("Explain HTMX")
print(response.text)
```

---

## 📦 v4.0 Module Architecture: "The 20 Foundational Pillars"

```text
backend/modules/
├── base/                      # 📍 Foundational Pillars (20)
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
├── ai/                        # 🤖 AI-First Layer (Optional)
│   ├── providers/             # AI Provider Abstraction
│   │   ├── interface.py       # ← Public API
│   │   └── agents/            # Pydantic AI Agents
│   └── chatbot/               # Project-aware AI Chatbot
│
└── custom/                    # 🔌 Plug & Play from ABYSS
    └── ...                    # Feature-specific modules
```

---

## 🚀 Quick Start

```bash
# 1. Clone
git clone https://github.com/daemonXid/DAEMON-ONE.git
cd DAEMON-ONE

# 2. Environment
cp .env.example .env
# Edit .env with your API keys

# 3. Setup (uv + bun + rust)
just setup

# 4. Run
just dev

# 5. Open http://localhost:2020
```

---

## 🐳 Production Deployment

### Local Docker

```bash
# Build and deploy full stack
just deploy

# View logs
just deploy-logs

# Stop
just deploy-down
```

### Coolify / VPS Deployment

 **Zero to Production in ~40 Minutes**

1. **Push to GitHub**: Push your customized code to a private repository.
2. **Coolify Setup**:
   - Go to Coolify Dashboard → Projects → New.
   - Select **Docker Compose**.
   - Paste the contents of `docker-compose.prod.yml`.
   - **Important**: Add environment variables from `.env.example`.
3. **Deploy**: Click deploy and wait for the magic (~3 mins).
4. **Domain**: Connect your domain in Coolify settings.

**Required Environment Variables for Production:**

| Variable | Description |
| :--- | :--- |
| `SECRET_KEY` | Generate with `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"` |
| `POSTGRES_PASSWORD` | Strong password for DB |
| `ALLOWED_HOSTS` | Your domain (e.g., `myapp.com`) |
| `CSRF_TRUSTED_ORIGINS` | Full URL (e.g., `https://myapp.com`) |

### ⚠️ Troubleshooting Local Production Test

If you run `just deploy` (production mode) locally, your browser might cache **HSTS settings** (forcing HTTPS).
If you cannot access `http://localhost:2020` afterwards:

1. Use **Incognito Mode** (recommended).
2. Or clear HSTS cache at `chrome://net-internals/#hsts` (Delete domain security policies for `localhost`).
3. Or access via `http://127.0.0.1:2020` instead.

---

## 🛠️ Available Commands

| Command | Description |
| ------- | ----------- |
| `just setup` | Install all dependencies (uv + bun + rust) |
| `just dev` | Start development server with hot reload |
| `just prod` | Start production server (Granian) |
| `just deploy` | Deploy full Docker production stack |
| `just build-docker` | Build production Docker image |
| `just lint` | Run linters (ruff + mypy) |
| `just fmt` | Format code with ruff |
| `just test` | Run pytest test suite |
| `just mig` | Create and apply migrations |
| `just superuser` | Create superuser from .env |
| `just modules` | List all auto-discovered modules |

---

## 🔗 Key Endpoints

| Endpoint | Description |
| -------- | ----------- |
| `/` | Home page |
| `/getting-started/` | Documentation |
| `/health/` | System health status |
| `/health/ready/` | Readiness probe (DB, cache) |
| `/health/live/` | Liveness probe |
| `/api/docs` | API documentation |
| `/admin/` | Admin panel (Unfold) |
| `/analytics/` | Analytics dashboard |

---

## 🧰 Technology Stack

| Category | Technologies |
| -------- | ------------ |
| **Backend** | Django 5, Django Ninja, Pydantic |
| **Frontend** | HTMX, Alpine.js, Tailwind CSS |
| **Server** | Granian (Rust ASGI) |
| **Database** | PostgreSQL + pgvector, Redis |
| **AI** | HuggingFace, DeepSeek, OpenRouter, Pydantic AI |
| **Package Manager** | uv (Python), bun (JS) |
| **Observability** | Logfire, Sentry |
| **Task Queue** | Taskiq |

---

## 📁 Environment Variables

See `.env.example` for all available configuration options:

- **Core**: `DEBUG`, `SECRET_KEY`
- **Database**: `POSTGRES_*`, `REDIS_*`
- **AI**: `AI_PROVIDER`, `HUGGINGFACE_API_KEY`, `DEEPSEEK_API_KEY`, `OPENROUTER_API_KEY`
- **Monitoring**: `LOGFIRE_TOKEN`, `SENTRY_DSN`
- **Security**: `TURNSTILE_SITE_KEY`, `TURNSTILE_SECRET_KEY`
- **Backup**: `BACKUP_S3_*`

---

## 📜 License

MIT License - See [LICENSE](LICENSE) for details.

---

Made with 😈 by [xid](https://github.com/daemonXid)
