from django.apps import AppConfig
from django.conf import settings


class RecsyswebConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'recsysweb'

    def ready(self):
        from .scheduler import scheduler
        if settings.SCHEDULER_AUTOSTART:
        	scheduler.start()