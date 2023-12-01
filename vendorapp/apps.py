from django.apps import AppConfig


class VendorauthConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'vendorapp'

    def ready(self):
        from . import signals
