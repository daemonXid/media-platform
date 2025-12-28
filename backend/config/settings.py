import sys
from pathlib import Path

import environ
import logfire

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# --- Environment Variables (v4.0) ---
env = environ.Env(
    DEBUG=(bool, True),
    LOGFIRE_TOKEN=(str, None),
    SENTRY_DSN=(str, None),
)

# Load .env file if it exists
env_file = BASE_DIR / ".env"
if env_file.exists():
    environ.Env.read_env(str(env_file))

# Add 'backend' and 'modules' to sys.path for easy imports
sys.path.append(str(BASE_DIR / "backend"))
sys.path.append(str(BASE_DIR / "backend" / "modules"))

# --- Logfire Observability (v4.0) ---
LOGFIRE_TOKEN = env("LOGFIRE_TOKEN")
if LOGFIRE_TOKEN:
    logfire.configure(token=LOGFIRE_TOKEN)
else:
    # In development, don't crash if not authenticated
    logfire.configure(send_to_logfire=False)

logfire.instrument_django()

# --- Core Django Settings ---
SECRET_KEY = env("SECRET_KEY", default="django-insecure-media-platform-local-dev-key")
DEBUG = env("DEBUG")
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["*"])

# --- Production Security (v4.0) ---
CSRF_TRUSTED_ORIGINS = env.list("CSRF_TRUSTED_ORIGINS", default=[])

if not DEBUG:
    # HTTPS settings
    SECURE_SSL_REDIRECT = env.bool("SECURE_SSL_REDIRECT", default=True)
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

    # HSTS
    SECURE_HSTS_SECONDS = 31536000  # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

# --- Ports (2020-2030 range) ---
DJANGO_PORT = env("DJANGO_PORT", default="2020")
POSTGRES_PORT = env("POSTGRES_PORT", default="2021")
REDIS_PORT = env("REDIS_PORT", default="2022")

# --- AI Provider Configuration (v4.0) ---
# Options: huggingface | deepseek | openrouter
AI_PROVIDER = env("AI_PROVIDER", default="huggingface")


# =============================================================================
# 🔍 Auto-Discovery: Automatically find and register Django apps in modules/
# =============================================================================


def auto_discover_apps(modules_dir: Path) -> list[str]:
    """
    Scan the modules folder and discover all Django apps.

    v4.0 Structure:
    - modules/base/core/apps.py → "modules.base.core"
    - modules/ai/providers/apps.py → "modules.ai.providers"
    - modules/custom/oauth/apps.py → "modules.custom.oauth"

    Supports up to 3 levels of nesting.

    Returns:
        List of app paths in dot notation
    """
    discovered_apps = []

    if not modules_dir.exists():
        return []

    def scan_directory(directory: Path, prefix: str) -> None:
        """Recursively scan directory for apps.py files."""
        for item in directory.iterdir():
            if not item.is_dir():
                continue
            if not (item / "__init__.py").exists():
                continue
            if item.name.startswith("_"):
                continue

            app_path = f"{prefix}.{item.name}"

            # If this directory has apps.py, it's a Django app
            if (item / "apps.py").exists():
                discovered_apps.append(app_path)
            else:
                # Otherwise, scan subdirectories
                scan_directory(item, app_path)

    scan_directory(modules_dir, "modules")
    return sorted(discovered_apps)


# Discover modules
MODULES_DIR = BASE_DIR / "backend" / "modules"
PROJECT_APPS = auto_discover_apps(MODULES_DIR)

# Debug: Print discovered apps on startup
if DEBUG:
    print(f"😈 Auto-discovered modules: {PROJECT_APPS}")


INSTALLED_APPS = [
    # --- Django Built-ins ---
    "unfold",  # Unfold Admin (Must be before admin)
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",  # For Allauth
    # --- Third Party ---
    "ninja_extra",
    "django_components",
    "django_htmx",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "compressor",
    "storages",
    # --- Modules (Auto-Discovered) ---
    *PROJECT_APPS,
]

# Add dev-only apps if DEBUG is True
if DEBUG:
    INSTALLED_APPS += [
        "django_extensions",
        "django_browser_reload",
    ]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # Static Files
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_htmx.middleware.HtmxMiddleware",  # HTMX
    "allauth.account.middleware.AccountMiddleware",  # Allauth
]

# Allow Chatbot Iframe
X_FRAME_OPTIONS = "SAMEORIGIN"

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR / "backend" / "templates",  # Global templates (base.html, 404.html)
            BASE_DIR / "backend" / "modules" / "base" / "core" / "templates",
            BASE_DIR / "backend" / "modules" / "base" / "accounts" / "templates",
        ],
        "APP_DIRS": False,  # Loader 활용 예정 (django-components 등)
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "modules.base.settings.context_processors.site_settings",  # Site Settings
            ],
            "loaders": [
                (
                    "django.template.loaders.cached.Loader",
                    [
                        "django.template.loaders.filesystem.Loader",
                        "django.template.loaders.app_directories.Loader",
                        "django_components.template_loader.Loader",  # Component Loader
                    ],
                )
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# Database
DATABASES = {
    "default": env.db(
        "DATABASE_URL",
        default=f"postgres://{env('POSTGRES_USER', default='daemon_one_user')}:{env('POSTGRES_PASSWORD', default='daemon_one_password')}@{env('POSTGRES_HOST', default='localhost')}:{POSTGRES_PORT}/{env('POSTGRES_DB', default='daemon_one_db')}",
    )
}

# Redis (for caching and Taskiq)
REDIS_URL = f"redis://{env('REDIS_HOST', default='localhost')}:{REDIS_PORT}/0"

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_URL,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }
}

# Static & Media
STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "static_root"
STATICFILES_DIRS = [
    BASE_DIR / "backend" / "static",
    BASE_DIR / "backend" / "modules" / "base" / "core" / "static",
]

MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "backend" / "media"

# Ninja Extra
NINJA_EXTRA = {
    "PAGINATION_CLASS": "ninja_extra.pagination.PageNumberPagination",
}

SITE_ID = 1  # For Allauth

# ============================================
# 🔐 Django Allauth Settings
# ============================================

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

# Login/Logout redirects
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"
LOGIN_URL = "/accounts/login/"

# Email settings (Allauth v0.60+ format)
ACCOUNT_LOGIN_METHODS = {"email"}
ACCOUNT_SIGNUP_FIELDS = ["email*", "password1*", "password2*"]
ACCOUNT_EMAIL_VERIFICATION = "optional"  # "mandatory" for production
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_SESSION_REMEMBER = True
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True
ACCOUNT_LOGIN_ON_PASSWORD_RESET = True

# For development, print emails to console
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# 👤 Identity
AUTH_USER_MODEL = "daemon_auth.User"

# 📦 Storages & Compression
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
        # "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage", # Production
    },
}

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "compressor.finders.CompressorFinder",
]

COMPRESS_ENABLED = True
