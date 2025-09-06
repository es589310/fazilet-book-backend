from django.apps import AppConfig


class OrdersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'orders'
    verbose_name = '🛒 Səbətlər və Sifarişlər'
    
    def ready(self):
        pass 