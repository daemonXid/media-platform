from django.apps import AppConfig


class RegistryConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "modules.base.registry"
    label = "registry"
    verbose_name = "🗄️ Registry"
