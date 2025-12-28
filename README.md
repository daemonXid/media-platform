# 🎥 Media Platform

> **AI-Powered Vision Analysis & Research Management System**

A comprehensive media analysis platform built on the **DAEMON Stack**. This platform integrates advanced computer vision capabilities with intelligent research paper management, providing a unified system for media ingestion, AI analysis, and knowledge management.

[![Python 3.12+](https://img.shields.io/badge/Python-3.12+-3776AB.svg)](https://www.python.org/)
[![Django 5](https://img.shields.io/badge/Django-5.x-092E20.svg)](https://www.djangoproject.com/)
[![HTMX](https://img.shields.io/badge/HTMX-Hypermedia-blue.svg)](https://htmx.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## ✨ Features

### 1. 👁️ Vision AI Analysis

- **Media Ingestion**: Upload images and videos (including YouTube links via `yt-dlp`)
- **AI-Powered Analysis**: Object detection, motion tracking, and visual data analysis
- **Computer Vision**: Integration with MediaPipe and YOLO for advanced vision tasks
- **Interactive Viewer**: Frame-by-frame video viewer with AI annotation overlay

### 2. 📄 Smart Paper Management

- **PDF Parsing**: Automatic metadata extraction from research papers
- **Knowledge Graph**: Link related papers and build citation networks
- **Semantic Search**: AI-powered search through research database
- **Annotation System**: Highlight and annotate important sections

### 3. 🤖 AI Chat Interface

- **Multi-Provider Support**: HuggingFace (Free) → DeepSeek (Quality) → OpenRouter (Multi-Model)
- **Contextual Assistance**: Get help analyzing media and understanding research
- **Streaming Responses**: Real-time AI interaction with markdown support

---

## 🛠️ Technology Stack

This project uses the **DAEMON Stack** architecture:

### Backend

- **Framework**: Django 5 + Django Ninja (REST API)
- **Language**: Python 3.12+ (Strict Type Hints)
- **Server**: Granian (Rust-based ASGI)
- **Database**: PostgreSQL with pgvector
- **Cache**: Redis
- **Task Queue**: Taskiq

### Frontend

- **Hypermedia**: HTMX (Server-driven interactivity)
- **Reactivity**: Alpine.js (Client-side state)
- **Styling**: Tailwind CSS
- **Components**: Django Components

### AI & Vision

- **Providers**: HuggingFace, DeepSeek, OpenRouter
- **Vision**: MediaPipe, OpenCV, YOLO
- **Framework**: Pydantic AI, Instructor, Outlines

### Infrastructure

- **Package Manager**: uv (Python), bun (JavaScript)
- **Containerization**: Docker + Docker Compose
- **Deployment**: Coolify-ready
- **Monitoring**: Logfire, Sentry

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.12+**
- **uv** (Python package manager): `curl -LsSf https://astral.sh/uv/install.sh | sh`
- **bun** (JavaScript runtime): `curl -fsSL https://bun.sh/install | bash`
- **Docker & Docker Compose** (for production)

### Development Setup

```bash
# 1. Clone the repository
git clone https://github.com/daemonXid/media-platform.git
cd media-platform

# 2. Environment Configuration
cp .env.example .env
# Edit .env with your credentials (AI API keys, database settings, etc.)

# 3. Install Dependencies
just setup

# 4. Start Development Server
just dev

# 5. Access the Platform
# - Home: http://localhost:2120
# - Admin: http://localhost:2120/admin/
# - API Docs: http://localhost:2120/api/docs
```

### Default Admin Credentials

Username: `daemon`  
Password: `daemonkorea2026`

*Change these immediately after first login!*

---

## 🐳 Production Deployment

### Docker Deployment

```bash
# Build and deploy the full stack
just deploy

# View logs
just deploy-logs

# Stop the stack
just deploy-down
```

### Coolify Deployment

1. Create a new service in Coolify
2. Set the compose file to `docker-compose.prod.yml`
3. Configure environment variables from `.env.example`
4. Deploy!

---

## 📁 Project Structure

```
media-platform/
├── backend/
│   ├── config/              # Django settings & URLs
│   ├── modules/             # Modular application structure
│   │   ├── base/            # Core modules (auth, health, etc.)
│   │   ├── ai/              # AI provider abstraction & chatbot
│   │   └── custom/          # Project-specific modules
│   │       ├── vision/      # Vision AI analysis
│   │       └── smart_paper/ # Research paper management
│   ├── templates/           # Global templates
│   └── static/              # Static assets
├── crates/                  # Rust performance modules (optional)
├── scripts/                 # Utility scripts
├── Dockerfile               # Production container
├── docker-compose.yml       # Development infrastructure
├── docker-compose.prod.yml  # Production stack
├── Justfile                 # Task automation
├── pyproject.toml           # Python dependencies
└── package.json             # JavaScript dependencies
```

---

## 📚 Available Commands

```bash
# Development
just dev          # Start development server
just dev-lite     # Start without Docker (SQLite)
just build        # Build frontend assets
just mig          # Run database migrations
just superuser    # Create admin user

# Quality Assurance
just test         # Run tests
just test-cov     # Run tests with coverage
just lint         # Run linters
just fmt          # Format code

# Production
just prod         # Run production server locally
just deploy       # Deploy Docker stack
just deploy-logs  # View production logs

# Utilities
just shell        # Django shell
just modules      # List auto-discovered modules
just clean        # Clean build artifacts
```

---

## 🔑 Environment Variables

Key environment variables to configure in `.env`:

### Core Application

- `SECRET_KEY` - Django secret key (auto-generated during setup)
- `DEBUG` - Debug mode (true/false)
- `ALLOWED_HOSTS` - Allowed hostnames

### Database

- `POSTGRES_DB` - Database name
- `POSTGRES_USER` - Database user
- `POSTGRES_PASSWORD` - Database password
- `POSTGRES_HOST` - Database host

### AI Providers

- `AI_PROVIDER` - Active provider (huggingface/deepseek/openrouter)
- `HUGGINGFACE_API_KEY` - HuggingFace API token
- `DEEPSEEK_API_KEY` - DeepSeek API key
- `OPENROUTER_API_KEY` - OpenRouter API key

### Monitoring (Optional)

- `SENTRY_DSN` - Sentry error tracking
- `LOGFIRE_TOKEN` - Logfire observability

See `.env.example` for the complete list.

---

## 🎯 Module Architecture

This project follows the **DAEMON Stack** modular monolith pattern:

- **Vertical Slicing**: Each module contains its own models, views, templates, and logic
- **Auto-Discovery**: Modules are automatically registered (no manual INSTALLED_APPS editing)
- **Interface Pattern**: Modules communicate through well-defined interfaces
- **Self-Contained**: Each module can be developed, tested, and deployed independently

### Core Modules (Base)

- `accounts` - User authentication & profiles
- `core` - Homepage & global utilities
- `health` - Health check endpoints
- `settings` - Site-wide configuration

### AI Modules

- `providers` - AI provider abstraction layer
- `chatbot` - AI chat interface

### Custom Modules

- `vision` - Vision AI analysis system
- `smart_paper` - Research paper management

---

## 🔒 Security Best Practices

- ✅ Secret key rotation via environment variables
- ✅ CSRF protection enabled
- ✅ SQL injection prevention (ORM)
- ✅ XSS protection (Django templates)
- ✅ Secure headers (django-cors-headers)
- ✅ Rate limiting (django-axes)
- ✅ HTTPS redirect in production

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

Built with the **DAEMON Stack** philosophy:

- **Simple > Complex**
- **Strict Modularity**
- **Vertical Slicing**
- **Modern Performance**

Powered by:

- [Django](https://www.djangoproject.com/)
- [HTMX](https://htmx.org/)
- [Granian](https://github.com/emmett-framework/granian)
- [Tailwind CSS](https://tailwindcss.com/)

---

**Made with 🎥 by xid**
