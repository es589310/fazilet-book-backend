from django.urls import path
from . import views

app_name = 'contact'

urlpatterns = [
    path('send/', views.send_contact_message, name='send_contact_message'),
    path('test-email/', views.test_email, name='test_email'),
] 