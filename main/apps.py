from django.apps import AppConfig

class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'
    def ready(self):
        # from .signals import started, created,finished
        from .signals import bgt_deletion,sld_deletion,drug_deletion