from django.urls import path
from . import views

app_name = 'contact'

urlpatterns = [
    path('send/', views.send_contact_message, name='send_contact_message'),
    path('social-links/', views.get_social_media_links, name='social_media_links'),
    path('site-settings/', views.get_site_settings, name='site_settings'),
    # Production: test endpoint removed for security
    # path('test-email/', views.test_email, name='test_email'),
] 