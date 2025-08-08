from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from .models import ContactMessage
from .serializers import ContactMessageSerializer
import logging

logger = logging.getLogger(__name__)

@api_view(['POST'])
@permission_classes([AllowAny])
def send_contact_message(request):
    """
    Contact mesajı göndərmək üçün endpoint
    """
    try:
        # Debug: Gələn məlumatları log et
        logger.info(f"Contact request - User authenticated: {request.user.is_authenticated}")
        logger.info(f"Contact request - User: {request.user}")
        logger.info(f"Contact request - Data: {request.data}")
        
        # Giriş olan istifadəçilər üçün request data-nı təmizlə
        data = request.data.copy()
        if request.user.is_authenticated:
            # Giriş olan istifadəçilər üçün name və email sahələrini çıxar
            if 'name' in data:
                del data['name']
            if 'email' in data:
                del data['email']
        
        logger.info(f"Contact request - Cleaned data: {data}")
        
        # Serializer yaradırıq
        serializer = ContactMessageSerializer(
            data=data,
            context={'user': request.user}
        )
        
        if serializer.is_valid():
            # Mesajı yaradırıq
            contact_message = serializer.save()
            
            # Əgər istifadəçi giriş etmişdirsə, user sahəsini təyin edirik
            if request.user.is_authenticated:
                contact_message.user = request.user
                contact_message.save()
            
            # Email-ləri paralel göndəririk
            import asyncio
            import concurrent.futures
            
            with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
                admin_future = executor.submit(send_admin_notification, contact_message)
                auto_reply_future = executor.submit(send_auto_reply, contact_message)
                
                admin_email_sent = admin_future.result()
                auto_reply_sent = auto_reply_future.result()
            
            if admin_email_sent and auto_reply_sent:
                contact_message.status = 'sent'
                contact_message.auto_reply_sent = True
                contact_message.auto_reply_date = timezone.now()
                contact_message.save()
            
            return Response({
                'message': 'Mesajınız uğurla göndərildi. Tezliklə sizinlə əlaqə saxlayacağıq.',
                'success': True
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                'message': 'Məlumatları düzgün doldurun',
                'errors': serializer.errors,
                'success': False
            }, status=status.HTTP_400_BAD_REQUEST)
            
    except Exception as e:
        logger.error(f"Contact message error: {str(e)}")
        return Response({
            'message': 'Xəta baş verdi. Zəhmət olmasa daha sonra yenidən cəhd edin.',
            'success': False
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def send_admin_notification(contact_message):
    """
    Admin-ə bildiriş email-i göndərir
    """
    try:
        subject = f"Yeni əlaqə mesajı: {contact_message.subject}"
        
        message = f"""
Yeni əlaqə mesajı alındı:

Göndərən: {contact_message.sender_name}
Email: {contact_message.sender_email}
Mövzu: {contact_message.subject}
Mesaj: {contact_message.message}

Tarix: {contact_message.created_at}
        """
        
        # Admin email-ini settings-dən alırıq
        admin_email = getattr(settings, 'ADMIN_EMAIL', 'admin@faziletkitab.az')
        
        # Email konfiqurasiyasını log edirik
        logger.info(f"Admin notification - FROM: {settings.DEFAULT_FROM_EMAIL}, TO: {admin_email}")
        
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[admin_email],
            fail_silently=False,
        )
        
        logger.info(f"Admin notification sent successfully to {admin_email}")
        return True
    except Exception as e:
        logger.error(f"Admin notification error: {str(e)}")
        logger.error(f"Email settings: HOST={settings.EMAIL_HOST}, PORT={settings.EMAIL_PORT}, USER={settings.EMAIL_HOST_USER}")
        return False

def send_auto_reply(contact_message):
    """
    Göndərənə avtomatik cavab göndərir
    """
    try:
        subject = "Mesajınız alındı - Fazilet Kitab"
        
        message = f"""
Salam {contact_message.sender_name},

Mesajınız uğurla alındı və nəzərdən keçirilir.

Mesaj məlumatları:
Mövzu: {contact_message.subject}
Tarix: {contact_message.created_at}

Tezliklə sizinlə əlaqə saxlayacağıq.

Təşəkkürlər,
Fazilet Kitab komandası
        """
        
        # Email konfiqurasiyasını log edirik
        logger.info(f"Email config - FROM: {settings.DEFAULT_FROM_EMAIL}, TO: {contact_message.sender_email}")
        logger.info(f"Email config - HOST: {settings.EMAIL_HOST}, PORT: {settings.EMAIL_PORT}")
        logger.info(f"Email config - USER: {settings.EMAIL_HOST_USER}")
        
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[contact_message.sender_email],
            fail_silently=False,
        )
        
        logger.info(f"Auto reply sent successfully to {contact_message.sender_email}")
        return True
    except Exception as e:
        logger.error(f"Auto reply error: {str(e)}")
        logger.error(f"Email settings: HOST={settings.EMAIL_HOST}, PORT={settings.EMAIL_PORT}, USER={settings.EMAIL_HOST_USER}")
        return False

@api_view(['GET'])
@permission_classes([AllowAny])
def test_email(request):
    """
    Email konfiqurasiyasını test etmək üçün endpoint
    """
    try:
        from django.core.mail import send_mail
        
        # Email konfiqurasiyasını log edirik
        logger.info(f"Testing email configuration:")
        logger.info(f"EMAIL_HOST: {settings.EMAIL_HOST}")
        logger.info(f"EMAIL_PORT: {settings.EMAIL_PORT}")
        logger.info(f"EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
        logger.info(f"DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")
        logger.info(f"ADMIN_EMAIL: {settings.ADMIN_EMAIL}")
        
        # Test email göndəririk
        send_mail(
            subject='Test Email - Fazilet Kitab',
            message='Bu bir test email-dir. Email konfiqurasiyası düzgün işləyir.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.ADMIN_EMAIL],
            fail_silently=False,
        )
        
        return Response({
            'message': 'Test email uğurla göndərildi!',
            'success': True
        })
        
    except Exception as e:
        logger.error(f"Test email error: {str(e)}")
        return Response({
            'message': f'Test email xətası: {str(e)}',
            'success': False
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
