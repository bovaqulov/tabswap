from django.apps import AppConfig

class TapswapConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tapswap'

    def ready(self):
        import tapswap.signals
        from .utils import start_scheduler_in_thread
        start_scheduler_in_thread()
