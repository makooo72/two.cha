from django.apps import AppConfig


class MainPageConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main_page'

    def ready(self):
        from . import signals
