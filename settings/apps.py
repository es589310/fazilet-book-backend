from django.apps import AppConfig


class SettingsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'settings'
    verbose_name = 'Sayt Tənzimləmələri'
    verbose_name_plural = 'Sayt Tənzimləmələri'
    
    def ready(self):
        import settings.signals
