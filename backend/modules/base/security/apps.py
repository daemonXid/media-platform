from django.apps import AppConfig


class SecurityConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "modules.base.security"
    label = "app_security"
    verbose_name = "🔐 App Security"
