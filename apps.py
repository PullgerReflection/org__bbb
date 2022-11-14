from django.apps import AppConfig


class Config(AppConfig):
    name = 'pullgerReflection.org__bbb'
    default_auto_field = 'django.db.models.BigAutoField'

    def ready(self):
        pass
