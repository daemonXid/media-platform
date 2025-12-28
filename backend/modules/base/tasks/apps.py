from django.apps import AppConfig


class TasksConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "modules.base.tasks"
    label = "background_tasks"
    verbose_name = "⏱️ Background Tasks"
