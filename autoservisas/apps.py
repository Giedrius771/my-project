from django.apps import AppConfig

class LibraryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'autoservisas'

    def ready(self):
        from .sygnals import create_profile, save_profile