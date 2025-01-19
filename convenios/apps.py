from django.apps import AppConfig


class ConveniosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'convenios'

    def ready(self):
        import convenios.signals