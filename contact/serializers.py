from rest_framework import serializers
from .models import ContactMessage, SocialMediaLink

class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
    
    def validate(self, data):
        user = self.context.get('user')
        
        # Debug: Serializer məlumatlarını log et
        # import logging
        # logger = logging.getLogger(__name__)
        # logger.info(f"Serializer validate - User: {user}")
        # logger.info(f"Serializer validate - User authenticated: {user.is_authenticated if user else False}")
        # logger.info(f"Serializer validate - Data: {data}")
        
        # Əgər istifadəçi giriş etmişdirsə, name və email tələb olunmur
        if user and user.is_authenticated:
            # Giriş olan istifadəçilər üçün name və email-i None kimi təyin et
            data['name'] = None
            data['email'] = None
            # logger.info(f"Serializer validate - Set name and email to None for authenticated user")
            return data
        
        # Giriş olmayan istifadəçilər üçün name və email tələb olunur
        if not data.get('name'):
            # logger.error(f"Serializer validate - Name is required but not provided")
            raise serializers.ValidationError("Ad Soyad tələb olunur")
        if not data.get('email'):
            # logger.error(f"Serializer validate - Email is required but not provided")
            raise serializers.ValidationError("E-mail tələb olunur")
        
        # logger.info(f"Serializer validate - Validation passed")
        return data


class SocialMediaLinkSerializer(serializers.ModelSerializer):
    icon_class = serializers.SerializerMethodField()
    
    class Meta:
        model = SocialMediaLink
        fields = ['platform', 'url', 'icon_class', 'is_active', 'is_hidden', 'order']
    
    def get_icon_class(self, obj):
        return obj.get_icon_class() 