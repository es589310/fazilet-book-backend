from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
import logging
import concurrent.futures

from .models import ContactMessage, SocialMediaLink
from .serializers import ContactMessageSerializer, SocialMediaLinkSerializer

# Production logging
logger = logging.getLogger(__name__)

# Production rate limiting
class ContactMessageThrottle(UserRateThrottle):
    rate = '60/hour'  # Authenticated users: 60 requests per hour (dəqiqədə 1)

class ContactMessageAnonThrottle(AnonRateThrottle):
    rate = '40/hour'   # Anonymous users: 40 requests per hour (1.5 dəqiqədə 1)

@api_view(['POST'])
@permission_classes([AllowAny])
@throttle_classes([ContactMessageAnonThrottle, ContactMessageThrottle])
def send_contact_message(request):
    """
    Contact mesajı göndərmək üçün endpoint - Production Ready
    """
    try:
        # Giriş olan istifadəçilər üçün request data-nı təmizlə
        data = request.data.copy()
        if request.user.is_authenticated:
            # Giriş olan istifadəçilər üçün name və email sahələrini çıxar
            if 'name' in data:
                del data['name']
            if 'email' in data:
                del data['email']
        
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
            
            # Response mesajını istifadəçi statusuna görə təyin edirik
            if request.user.is_authenticated:
                response_message = "Dəyərli istifadəçi müraciətiniz qeydə alındı"
            else:
                response_message = "Mesajınız uğurla göndərildi. Tezliklə sizinlə əlaqə saxlayacağıq."
            
            logger.info(f"Contact message sent successfully by user: {request.user if request.user.is_authenticated else 'anonymous'}")
            
            return Response({
                'message': response_message,
                'success': True
            }, status=status.HTTP_201_CREATED)
        else:
            logger.warning(f"Contact message validation failed: {serializer.errors}")
            return Response({
                'message': 'Məlumatları düzgün doldurun',
                'errors': serializer.errors,
                'success': False
            }, status=status.HTTP_400_BAD_REQUEST)
            
    except Exception as e:
        logger.error(f"Contact message error: {str(e)}", exc_info=True)
        return Response({
            'message': 'Xəta baş verdi. Zəhmət olmasa daha sonra yenidən cəhd edin.',
            'success': False
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def send_admin_notification(contact_message):
    """
    Admin-ə bildiriş email-i göndərir - Production Ready
    """
    try:
        # Try to use email utility, fallback to direct send_mail
        try:
            from lib.email_utils import send_contact_email
            
            success = send_contact_email(
                name=contact_message.sender_name,
                email=contact_message.sender_email,
                subject=contact_message.subject,
                message=contact_message.message
            )
            
            if success:
                logger.info("Admin notification sent successfully using email utility")
                return True
            else:
                logger.warning("Admin notification failed using email utility, trying fallback")
                raise ImportError("Email utility failed")
                
        except ImportError:
            # Fallback to direct send_mail
            email_subject = f"Yeni müraciət: {contact_message.subject}"
            
            email_message = f"""
Yeni müraciət alındı:

Göndərən: {contact_message.sender_name}
Email: {contact_message.sender_email}
Mövzu: {contact_message.subject}
Tarix: {contact_message.created_at.strftime('%d.%m.%Y %H:%M')}

Mesaj:
{contact_message.message}

---
Bu email dostumkitab.az saytından avtomatik göndərilmişdir.
            """
            
            # Get recipient email from settings or use default
            recipient_email = getattr(settings, 'ADMIN_EMAIL', getattr(settings, 'DEFAULT_FROM_EMAIL', 'admin@dostumkitab.az'))
            
            # Send email with production settings
            result = send_mail(
                subject=email_subject,
                message=email_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[recipient_email],
                fail_silently=True,  # Production: don't fail on email errors
            )
            
            if result:
                logger.info(f"Admin notification sent successfully using fallback to {recipient_email}")
                return True
            else:
                logger.warning(f"Admin notification failed using fallback to {recipient_email}")
                return False
                
    except Exception as e:
        logger.error(f"Admin notification error: {str(e)}", exc_info=True)
        return False

def send_auto_reply(contact_message):
    """
    Göndərənə avtomatik cavab göndərir - Production Ready
    """
    try:
        # Giriş olan istifadəçilər üçün müraciət mesajı cavabı
        if contact_message.user and contact_message.user.is_authenticated:
            subject = "Dəyərli istifadəçi müraciətiniz qeyd-ə alındı"
            
            message = f"""
Salam {contact_message.user.get_full_name() or contact_message.user.username},

Dəyərli istifadəçi müraciətiniz qeydə alındı və nəzərdən keçirilir.

Mesaj məlumatları:
Mövzu: {contact_message.subject}
Tarix: {contact_message.created_at.strftime('%d.%m.%Y %H:%M')}

Tezliklə sizinlə əlaqə saxlayacağıq.

Təşəkkürlər,
dostumkitab.az komandası 🚀
            """
            
            recipient_email = contact_message.user.email
        else:
            # Giriş olmayan istifadəçilər üçün adi cavab
            subject = "Mesajınız alındı - dostumkitab.az"
            
            message = f"""
Salam {contact_message.sender_name},

Mesajınız uğurla alındı və nəzərdən keçirilir.

Mesaj məlumatları:
Mövzu: {contact_message.subject}
Tarix: {contact_message.created_at.strftime('%d.%m.%Y %H:%M')}

Tezliklə sizinlə əlaqə saxlayacağıq.

Təşəkkürlər,
dostumkitab.az komandası 🚀
            """
            
            recipient_email = contact_message.sender_email
        
        # Try to use email utility, fallback to direct send_mail
        try:
            from lib.email_utils import send_auto_reply_email
            
            success = send_auto_reply_email(
                recipient_email=recipient_email,
                name=contact_message.sender_name,
                subject=contact_message.subject
            )
            
            if success:
                logger.info(f"Auto reply sent successfully using email utility to {recipient_email}")
                return True
            else:
                logger.warning(f"Auto reply failed using email utility, trying fallback")
                raise ImportError("Email utility failed")
                
        except ImportError:
            # Fallback to direct send_mail
            result = send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[recipient_email],
                fail_silently=True,  # Production: don't fail on email errors
            )
            
            if result:
                logger.info(f"Auto reply sent successfully using fallback to {recipient_email}")
                return True
            else:
                logger.warning(f"Auto reply failed using fallback to {recipient_email}")
                return False
                
    except Exception as e:
        logger.error(f"Auto reply error: {str(e)}", exc_info=True)
        return False

@api_view(['GET'])
@permission_classes([AllowAny])
def get_social_media_links(request):
    """
    Aktiv və gizlənməmiş sosial media linklərini qaytarır - Production Ready
    """
    try:
        links = SocialMediaLink.objects.filter(
            is_active=True, 
            is_hidden=False
        ).order_by('order', 'platform')
        serializer = SocialMediaLinkSerializer(links, many=True)
        
        return Response({
            'links': serializer.data,
            'success': True
        })
        
    except Exception as e:
        logger.error(f"Social media links error: {str(e)}", exc_info=True)
        return Response({
            'message': 'Sosial media linkləri yüklənərkən xəta baş verdi.',
            'success': False
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_site_settings(request):
    """
    Sayt tənzimləmələrini qaytarır - Production Ready
    """
    try:
        # Try to import SiteSettings, fallback if not available
        try:
            from settings.models import SiteSettings
            from settings.serializers import SiteSettingsSerializer
            
            site_settings = SiteSettings.objects.filter(is_active=True).first()
            if site_settings:
                serializer = SiteSettingsSerializer(site_settings)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({
                    'message': 'Sayt tənzimləmələri tapılmadı.',
                    'success': False
                }, status=status.HTTP_404_NOT_FOUND)
                
        except ImportError:
            # Fallback response if SiteSettings is not available
            logger.warning("SiteSettings not available, returning fallback response")
            return Response({
                'message': 'Sayt tənzimləmələri hazır deyil.',
                'success': False
            }, status=status.HTTP_503_SERVICE_UNAVAILABLE)
            
    except Exception as e:
        logger.error(f"Site settings error: {str(e)}", exc_info=True)
        return Response({
            'message': 'Sayt tənzimləmələri yüklənərkən xəta baş verdi.',
            'success': False
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def test_email(request):
    """
    Email konfiqurasiyasını test etmək üçün endpoint - Production Ready (Admin Only)
    """
    try:
        # Check if user is staff/admin
        if not request.user.is_staff:
            logger.warning(f"Unauthorized test email attempt by user: {request.user.username}")
            return Response({
                'error': 'Bu əməliyyat üçün icazəniz yoxdur',
                'success': False
            }, status=status.HTTP_403_FORBIDDEN)
        
        # Check email configuration
        try:
            from lib.email_utils import check_email_configuration
            
            config_status = check_email_configuration()
            if not config_status['is_configured']:
                logger.warning("Email configuration incomplete for test")
                return Response({
                    'message': 'Email konfiqurasiyası tam deyil',
                    'config': config_status,
                    'success': False
                }, status=status.HTTP_400_BAD_REQUEST)
                
        except ImportError:
            # Fallback configuration check
            config_status = {
                'email_host': getattr(settings, 'EMAIL_HOST', None),
                'email_port': getattr(settings, 'EMAIL_PORT', None),
                'email_host_user': getattr(settings, 'EMAIL_HOST_USER', None),
                'default_from_email': getattr(settings, 'DEFAULT_FROM_EMAIL', None),
                'admin_email': getattr(settings, 'ADMIN_EMAIL', None),
                'is_configured': False
            }
            
            if not all([config_status['email_host'], config_status['email_port'], 
                       config_status['email_host_user'], config_status['default_from_email']]):
                return Response({
                    'message': 'Email konfiqurasiyası tam deyil',
                    'config': config_status,
                    'success': False
                }, status=status.HTTP_400_BAD_REQUEST)
        
        # Test email göndəririk
        test_subject = 'Test Email - Dostum Kitab'
        test_message = 'Bu bir test email-dir. Email konfiqurasiyası düzgün işləyir.'
        
        recipient_email = getattr(settings, 'ADMIN_EMAIL', getattr(settings, 'DEFAULT_FROM_EMAIL', 'admin@dostumkitab.az'))
        
        result = send_mail(
            subject=test_subject,
            message=test_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[recipient_email],
            fail_silently=True,  # Production: don't fail on email errors
        )
        
        if result:
            logger.info(f"Test email sent successfully to {recipient_email} by admin {request.user.username}")
            return Response({
                'message': 'Test email uğurla göndərildi!',
                'success': True
            })
        else:
            logger.warning(f"Test email failed to send to {recipient_email}")
            return Response({
                'message': 'Test email göndərilmədi',
                'success': False
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    except Exception as e:
        logger.error(f"Test email error: {str(e)}", exc_info=True)
        return Response({
            'message': f'Test email xətası: {str(e)}',
            'success': False
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
