from rest_framework import serializers
from .models import ContactMessage, SocialMediaLink

class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
    
    def validate(self, data):
        user = self.context.get('user')
        
        # Əgər istifadəçi giriş etmişdirsə, name və email tələb olunmur
        if user and user.is_authenticated:
            # Giriş olan istifadəçilər üçün name və email-i None kimi təyin et
            data['name'] = None
            data['email'] = None
            return data
        
        # Giriş olmayan istifadəçilər üçün name və email tələb olunur
        if not data.get('name'):
            raise serializers.ValidationError("Ad Soyad tələb olunur")
        if not data.get('email'):
            raise serializers.ValidationError("E-mail tələb olunur")
        
        return data


class SocialMediaLinkSerializer(serializers.ModelSerializer):
    icon_class = serializers.SerializerMethodField()
    
    class Meta:
        model = SocialMediaLink
        fields = ['platform', 'url', 'icon_class', 'is_active', 'is_hidden', 'order']
    
    def get_icon_class(self, obj):
        return obj.get_icon_class() 