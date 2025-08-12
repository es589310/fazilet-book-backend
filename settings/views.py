from rest_framework.generics import RetrieveAPIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import SiteSettings, Logo
from .serializers import SiteSettingsSerializer, LogoSerializer

class SiteSettingsView(RetrieveAPIView):
    """Sayt tənzimləmələri"""
    serializer_class = SiteSettingsSerializer
    permission_classes = [AllowAny]
    
    def get_object(self):
        return SiteSettings.get_settings()

@api_view(['GET'])
def whatsapp_number(request):
    """WhatsApp nömrəsini qaytarır"""
    settings = SiteSettings.get_settings()
    return Response({
        'whatsapp_number': settings.whatsapp_number
    })

class LogoView(RetrieveAPIView):
    """Logo tənzimləmələri"""
    serializer_class = LogoSerializer
    permission_classes = [AllowAny]
    
    def get_object(self):
        return Logo.get_settings()
