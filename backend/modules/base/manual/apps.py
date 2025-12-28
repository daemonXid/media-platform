from django.apps import AppConfig


class ManualConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "modules.base.manual"
    label = "manual"
    verbose_name = "📖 Project Manual"
