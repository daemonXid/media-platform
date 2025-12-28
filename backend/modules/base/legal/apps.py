from django.apps import AppConfig


class LegalConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "modules.base.legal"
    label = "legal_compliance"
    verbose_name = "⚖️ Legal Compliance"
