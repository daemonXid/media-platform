from django.apps import AppConfig


class SiteSettingsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "modules.base.settings"
    label = "site_settings"  # Avoid collision with Django settings module
    verbose_name = "⚙️ Site Settings"
