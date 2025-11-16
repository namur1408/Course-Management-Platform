from django.apps import AppConfig


class ActionlogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ActionLog'

    def ready(self):
        import ActionLog.signals
