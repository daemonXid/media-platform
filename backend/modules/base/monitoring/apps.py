from django.apps import AppConfig


class MonitoringConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "modules.base.monitoring"
    label = "sys_monitoring"
    verbose_name = "🛡️ System Monitoring"
