from django.apps import AppConfig


class BackupConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "modules.base.backup"
    label = "data_backup"
    verbose_name = "💾 Data Backup"
