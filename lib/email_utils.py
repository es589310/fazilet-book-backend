"""
Production-ready email utilities for Dostum Kitab
Handles email sending with proper error handling and fallbacks
"""

import logging
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone

logger = logging.getLogger(__name__)

def send_contact_email(name, email, subject, message, **kwargs):
    """
    Production-ready contact email sending with fallbacks
    
    Args:
        name: Sender name
        email: Sender email
        subject: Email subject
        message: Email message
        **kwargs: Additional email parameters
    
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    try:
        # Prepare email content
        email_subject = f"Yeni müraciət: {subject}"
        
        email_message = f"""
Yeni müraciət alındı:

Göndərən: {name}
Email: {email}
Mövzu: {subject}
Tarix: {timezone.now().strftime('%d.%m.%Y %H:%M')}

Mesaj:
{message}

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
            **kwargs
        )
        
        if result:
            logger.info(f"Contact email sent successfully to {recipient_email}")
            return True
        else:
            logger.warning(f"Contact email failed to send to {recipient_email}")
            return False
            
    except Exception as e:
        logger.error(f"Contact email error: {str(e)}")
        return False

def send_notification_email(recipient_email, subject, message, **kwargs):
    """
    Send notification email with production settings
    
    Args:
        recipient_email: Recipient email address
        subject: Email subject
        message: Email message
        **kwargs: Additional email parameters
    
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    try:
        result = send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[recipient_email],
            fail_silently=True,  # Production: don't fail on email errors
            **kwargs
        )
        
        if result:
            logger.info(f"Notification email sent successfully to {recipient_email}")
            return True
        else:
            logger.warning(f"Notification email failed to send to {recipient_email}")
            return False
            
    except Exception as e:
        logger.error(f"Notification email error: {str(e)}")
        return False

def send_auto_reply_email(recipient_email, name, subject, **kwargs):
    """
    Send auto-reply email with production settings
    
    Args:
        recipient_email: Recipient email address
        name: Recipient name
        subject: Original message subject
        **kwargs: Additional email parameters
    
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    try:
        auto_reply_subject = "Mesajınız alındı - dostumkitab.az"
        
        auto_reply_message = f"""
Salam {name},

Mesajınız uğurla alındı və nəzərdən keçirilir.

Mesaj məlumatları:
Mövzu: {subject}
Tarix: {timezone.now().strftime('%d.%m.%Y %H:%M')}

Tezliklə sizinlə əlaqə saxlayacağıq.

Təşəkkürlər,
dostumkitab.az komandası 🚀
        """
        
        result = send_mail(
            subject=auto_reply_subject,
            message=auto_reply_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[recipient_email],
            fail_silently=True,  # Production: don't fail on email errors
            **kwargs
        )
        
        if result:
            logger.info(f"Auto-reply email sent successfully to {recipient_email}")
            return True
        else:
            logger.warning(f"Auto-reply email failed to send to {recipient_email}")
            return False
            
    except Exception as e:
        logger.error(f"Auto-reply email error: {str(e)}")
        return False

def check_email_configuration():
    """
    Check if email configuration is properly set up
    
    Returns:
        dict: Configuration status and details
    """
    config_status = {
        'email_host': getattr(settings, 'EMAIL_HOST', None),
        'email_port': getattr(settings, 'EMAIL_PORT', None),
        'email_host_user': getattr(settings, 'EMAIL_HOST_USER', None),
        'default_from_email': getattr(settings, 'DEFAULT_FROM_EMAIL', None),
        'admin_email': getattr(settings, 'ADMIN_EMAIL', None),
        'is_configured': False
    }
    
    # Check if essential email settings are configured
    if (config_status['email_host'] and 
        config_status['email_port'] and 
        config_status['email_host_user'] and 
        config_status['default_from_email']):
        config_status['is_configured'] = True
    
    return config_status

def get_email_fallback_message():
    """
    Get fallback message when email is not configured
    
    Returns:
        str: Fallback message
    """
    return """
Email konfiqurasiyası hazır deyil. 
Zəhmət olmasa sistem administratoru ilə əlaqə saxlayın.
    """ 