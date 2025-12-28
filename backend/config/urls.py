"""
😈 DAEMON-ONE URL Configuration

Routes are organized as:
- /           → daemon module (home, htmx endpoints)
- /admin/     → Django admin
- /api/       → Ninja API (for external integrations)
- /accounts/  → Allauth authentication
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from ninja_extra import NinjaExtraAPI

# API for external integrations (3rd party, mobile apps)
api = NinjaExtraAPI(
    title="DAEMON-ONE API",
    description="External API endpoints for DAEMON-ONE",
    version="0.1.0",
)

urlpatterns = [
    # 😈 Core module - Home & HTMX endpoints
    path("", include("modules.base.core.urls")),
    # 🏥 Health checks - Kubernetes/Docker/LB probes
    path("health/", include("modules.base.health.urls")),
    # 🤖 AI Chatbot - Project-aware AI assistant
    path("chatbot/", include("modules.ai.chatbot.urls")),
    # 📊 Analytics module
    path("analytics/", include("modules.base.analytics.urls")),
    # 📖 Project Manual (Auto-docs)
    path("manual/", include("modules.base.manual.urls")),
    # Admin
    path("admin/", admin.site.urls),
    # External API (Ninja)
    path("api/", api.urls),
    # 👤 Custom auth views (profile, etc.)
    path("accounts/", include("modules.base.accounts.urls")),
    # Authentication (Allauth)
    path("accounts/", include("allauth.urls")),
]

# Development-only routes
if settings.DEBUG:
    urlpatterns += [
        path("__reload__/", include("django_browser_reload.urls")),
    ]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
