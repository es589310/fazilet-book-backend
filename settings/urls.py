from django.urls import path
from . import views

urlpatterns = [
    path('site-settings/', views.SiteSettingsView.as_view(), name='site-settings'),
    path('logo/', views.LogoView.as_view(), name='logo'),
    path('whatsapp-number/', views.whatsapp_number, name='whatsapp-number'),
] 