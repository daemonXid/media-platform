set shell := ["bash", "-c"]

# ============================================
# 🎥 Media Platform Justfile
# ============================================

# --- 🚀 Main Commands ---

# Install all dependencies (uv + bun + rust)
setup:
    @echo "🎥 Setting up Media Platform..."
    uv sync
    bun install
    just build
    just build-rust
    @echo "✅ Setup complete! Run 'just dev' to start."

# Start development (Django + Tailwind watch)
dev:
    just up
    just build
    uv run python backend/manage.py migrate --run-syncdb
    @echo ""
    @echo "😈 ═══════════════════════════════════════════════"
    @echo "   Media Platform Development Server"
    @echo "═══════════════════════════════════════════════════"
    @echo "   📍 Home:     http://localhost:2020"
    @echo "   📍 API Docs: http://localhost:2020/api/docs"
    @echo "   📍 Admin:    http://localhost:2020/admin/"
    @echo "═══════════════════════════════════════════════════"
    @echo ""
    (trap 'kill 0' SIGINT; \
     uv run python backend/manage.py runserver 0.0.0.0:2020 & \
     bun run tailwind:watch & \
     wait)

# Quick start without Docker (SQLite)
dev-lite:
    just build
    @echo "🎥 Starting Media Platform (Lite Mode - SQLite)..."
    uv run python backend/manage.py migrate --run-syncdb
    uv run python backend/manage.py runserver 0.0.0.0:2020

# --- 🚀 Production ---

# Start production server with Granian (Rust-based ASGI)
prod workers="4":
    @echo ""
    @echo "🦀 ═══════════════════════════════════════════════"
    @echo "   Media Platform Production Server (Granian)"
    @echo "═══════════════════════════════════════════════════"
    @echo "   📍 http://0.0.0.0:2020"
    @echo "   👷 Workers: {{workers}}"
    @echo "═══════════════════════════════════════════════════"
    @echo ""
    uv run granian --interface asgi main:app --host 0.0.0.0 --port 2020 --workers {{workers}}

# Production with hot reload (for staging)
prod-reload:
    uv run granian --interface asgi main:app --host 0.0.0.0 --port 2020 --workers 2 --reload

# Benchmark server (single worker, no reload)
bench:
    @echo "⚡ Starting benchmark mode..."
    uv run granian --interface asgi main:app --host 0.0.0.0 --port 2020 --workers 1 --threading-mode workers

# --- 🐳 Docker Production ---

# Build production Docker image
build-docker:
    @echo "🐳 Building production Docker image..."
    docker build -t daemon-one:latest .
    @echo "✅ Image built: daemon-one:latest"

# Deploy full production stack
deploy:
    @echo "🚀 Deploying Media Platform production stack..."
    docker compose -f docker-compose.prod.yml up -d --build
    @echo "✅ Deployed! Check http://localhost:2020"

# Stop production stack
deploy-down:
    docker compose -f docker-compose.prod.yml down

# View production logs
deploy-logs:
    docker compose -f docker-compose.prod.yml logs -f

# --- 🦀 Rust ---

# Build Rust modules (dev mode)
build-rust:
    uv run maturin develop

# Build Rust modules (release)
build-rust-release:
    uv run maturin develop --release

# --- 🐳 Infrastructure ---

# Start Docker containers (postgres, redis)
up:
    docker compose up -d postgres redis
    @echo "✅ Docker containers started (postgres:2021, redis:2022)"

# Stop Docker containers
down:
    docker compose down

# Stop and remove volumes
down-v:
    docker compose down -v

# View logs
logs:
    docker compose logs -f

# --- 🗄️ Database ---

# Create and apply migrations
mig:
    uv run python backend/manage.py makemigrations
    uv run python backend/manage.py migrate

# Create superuser (uses .env credentials)
superuser:
    @echo "📦 Creating superuser from .env..."
    uv run python backend/manage.py createsuperuser --noinput || echo "⚠️  Superuser may already exist"

# Create superuser interactively
superuser-interactive:
    uv run python backend/manage.py createsuperuser

# Django shell (shell_plus)
shell:
    uv run python backend/manage.py shell_plus

# Database shell (psql)
dbshell:
    docker compose exec postgres psql -U ${POSTGRES_USER:-daemon_one_user} -d ${POSTGRES_DB:-daemon_one_db}

# --- 🎨 Frontend ---

# Build all frontend assets (vendor bundle + CSS)
build:
    @echo "📦 Building frontend assets..."
    bun run build
    @echo "✅ Assets built to backend/static/dist/ and backend/static/css/"

# Build vendor bundle only (htmx + alpine + pglite)
vendor:
    bun run vendor

# Build Tailwind CSS only
css-build:
    bun run tailwind:build

# Watch Tailwind CSS
css-watch:
    bun run tailwind:watch

# --- 🧪 Quality ---

# Run linters (ruff)
lint:
    uv run ruff check . --fix --unsafe-fixes
    @echo "✅ Lint check passed!"

# Run tests
test:
    uv run python -m pytest

# Run tests with coverage
test-cov:
    uv run python -m pytest --cov=backend --cov-report=html

# Format code
fmt:
    uv run ruff format .

# Check code without fixing
check:
    uv run ruff check .

# --- 🛠️ Utilities ---

# Terminal UI dashboard
tui:
    uv run python backend/manage.py tui

# Collect static files
static:
    uv run python backend/manage.py collectstatic --noinput

# Show all auto-discovered modules
modules:
    @uv run python -c "from backend.config.settings import PROJECT_APPS; print('\n'.join(PROJECT_APPS))"

# --- 🏭 Module Factory ---

# Create a new module
new-module name:
    uv run python scripts/create_module.py {{name}}

# Create a multi-feature module
new-module-multi name +features:
    uv run python scripts/create_module.py {{name}} --multi-feature {{features}}

# --- 🧹 Clean ---

# Clean build artifacts
clean:
    rm -rf .venv __pycache__ .pytest_cache .mypy_cache .ruff_cache
    rm -rf backend/**/__pycache__ backend/**/*.pyc
    rm -rf node_modules
    rm -rf target
    rm -rf static_root
    rm -rf htmlcov
    @echo "✅ Cleaned all build artifacts"

# Clean and reinstall
reset:
    just clean
    just setup
