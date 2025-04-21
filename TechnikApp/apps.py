from django.apps import AppConfig


class TechnikappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'TechnikApp'

    def ready(self):
       import TechnikApp.signals