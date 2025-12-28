from django.apps import AppConfig


class HealthConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "modules.base.health"
    label = "health"
    verbose_name = "🏥 Health Checks"
