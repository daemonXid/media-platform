# ============================================
# 😈 DAEMON-ONE Production Dockerfile
# ============================================
# Multi-stage build with Rust support
# Uses: Python 3.12 + Rust + bun + Granian
# ============================================

# --- Stage 1: Frontend Build ---
FROM oven/bun:1 AS frontend-builder

WORKDIR /app

# Copy frontend dependencies
COPY package.json bun.lock ./
RUN bun install --frozen-lockfile

# Copy frontend source and build
COPY tailwind.config.js ./
COPY backend/static/ backend/static/
COPY backend/templates/ backend/templates/
COPY backend/modules/ backend/modules/

RUN bun run build

# --- Stage 2: Python + Rust Build ---
FROM python:3.12-slim-bookworm AS python-builder

WORKDIR /app

# Install build dependencies including Rust
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    curl \
    && curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y --profile minimal \
    && rm -rf /var/lib/apt/lists/*

# Add Rust to PATH
ENV PATH="/root/.cargo/bin:$PATH"

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Copy project files (including Rust crates)
COPY pyproject.toml uv.lock ./
COPY Cargo.toml Cargo.lock ./
COPY crates/ crates/
COPY README.md ./

# Install all dependencies (including building Rust module)
RUN uv sync --frozen --no-dev

# --- Stage 3: Production Runtime ---
FROM python:3.12-slim-bookworm AS runtime

WORKDIR /app

# Install runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && useradd --create-home --shell /bin/bash appuser

# Copy virtual environment from builder
COPY --from=python-builder /app/.venv /app/.venv

# Copy application code
COPY backend/ backend/
COPY main.py ./

# Copy built frontend assets
COPY --from=frontend-builder /app/backend/static/dist/ backend/static/dist/
COPY --from=frontend-builder /app/backend/static/css/output.css backend/static/css/output.css

# Set environment
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONPATH=/app:/app/backend:/app/backend/modules
ENV DJANGO_SETTINGS_MODULE=backend.config.settings
ENV DEBUG=false

# Collect static files
RUN python backend/manage.py collectstatic --noinput

# Change ownership
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 2120

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:2120/health/live/ || exit 1

# Run with Granian (Rust ASGI)
CMD ["granian", "--interface", "asgi", "main:app", "--host", "0.0.0.0", "--port", "2120", "--workers", "4"]
