import os
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def send_welcome_email(user):
    """
    Yeni qeydiyyatdan keçən istifadəçiyə xoş gəlmə emaili göndərir
    """
    try:
        # Email məzmunu
        subject = "dostumkitab.az-a xoş gəlmisiniz! 🚀"
        
        # HTML məzmunu
        html_message = f"""
        <!DOCTYPE html>
        <html lang="az">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Xoş gəlmisiniz!</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    max-width: 600px;
                    margin: 0 auto;
                    padding: 20px;
                }}
                .header {{
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 30px;
                    text-align: center;
                    border-radius: 10px 10px 0 0;
                }}
                .content {{
                    background: #f9f9f9;
                    padding: 30px;
                    border-radius: 0 0 10px 10px;
                }}
                .button {{
                    display: inline-block;
                    background: #667eea;
                    color: white;
                    padding: 12px 30px;
                    text-decoration: none;
                    border-radius: 25px;
                    margin: 20px 0;
                    font-weight: bold;
                }}
                .footer {{
                    margin-top: 30px;
                    padding-top: 20px;
                    border-top: 1px solid #ddd;
                    text-align: center;
                    color: #666;
                }}
                .highlight {{
                    background: #fff3cd;
                    padding: 15px;
                    border-radius: 5px;
                    border-left: 4px solid #ffc107;
                    margin: 20px 0;
                }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🎉 Xoş gəlmisiniz!</h1>
                <p>dostumkitab.az ailəsinə qoşulduğunuz üçün təşəkkür edirik!</p>
            </div>
            
            <div class="content">
                <h2>Salam {user.first_name or user.username}!</h2>
                
                <p>dostumkitab.az-a xoş gəlmisiniz! 🚀</p>
                
                <div class="highlight">
                    <p><strong>Qeydiyyatınız uğurla tamamlandı və artıq hesabınıza daxil ola bilərsiniz.</strong></p>
                </div>
                
                <p>Hesabınıza giriş etmək üçün aşağıdakı düyməyə klikləyin:</p>
                
                <div style="text-align: center;">
                    <a href="https://dostumkitab.az.com/login" class="button">
                        ➡️ Giriş Et
                    </a>
                </div>
                
                <p style="margin-top: 20px;">
                    <strong>Əgər düymə işləmirsə, bu linki kopyalayıb brauzerinizə yapışdırın:</strong><br>
                    <a href="https://dostumkitab.az.com/login">https://dostumkitab.az.com/login</a>
                </p>
                
                <p>Hesabınızda siz:</p>
                <ul>
                    <li>📚 Minlərlə kitabı kəşf edə bilərsiniz</li>
                    <li>🛒 Təhlükəsiz alış-veriş edə bilərsiniz</li>
                    <li>🚚 Sürətli çatdırılma xidmətindən istifadə edə bilərsiniz</li>
                    <li>💳 Təhlükəsiz ödəniş üsullarından istifadə edə bilərsiniz</li>
                </ul>
            </div>
            
            <div class="footer">
                <p><strong>Təşəkkür edirik və xoş istifadə təcrübəsi arzulayırıq! 🚀</strong></p>
                <p>Hörmətlə,<br><strong>dostumkitab.az komandası</strong></p>
            </div>
        </body>
        </html>
        """
        
        # Sadə mətn məzmunu (HTML dəstəklənməyən email client-lar üçün)
        plain_message = f"""
Salam {user.first_name or user.username},

dostumkitab.az xoş gəlmisiniz!  
Qeydiyyatınız uğurla tamamlandı və artıq hesabınıza daxil ola bilərsiniz.

Hesabınıza giriş etmək üçün:  
➡️ https://dostumkitab.az.com/login

Təşəkkür edirik və xoş istifadə təcrübəsi arzulayırıq! 🚀

Hörmətlə,  
dostumkitab.az komandası
        """
        
        # Email göndəririk
        send_mail(
            subject=subject,
            message=strip_tags(plain_message),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False,
        )
        
        print(f"✅ Xoş gəlmə emaili göndərildi: {user.email}")
        return True
        
    except Exception as e:
        print(f"❌ Email göndərilmədi: {str(e)}")
        return False

def send_contact_email(name, email, subject, message):
    """
    Əlaqə formundan gələn mesajı admin-ə göndərir
    """
    try:
        # Email məzmunu
        email_subject = f"Yeni Əlaqə Mesajı: {subject}"
        
        # HTML məzmunu
        html_message = f"""
        <!DOCTYPE html>
        <html lang="az">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Yeni Əlaqə Mesajı</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    max-width: 600px;
                    margin: 0 auto;
                    padding: 20px;
                }}
                .header {{
                    background: #dc3545;
                    color: white;
                    padding: 20px;
                    text-align: center;
                    border-radius: 10px 10px 0 0;
                }}
                .content {{
                    background: #f9f9f9;
                    padding: 20px;
                    border-radius: 0 0 10px 10px;
                }}
                .field {{
                    margin: 15px 0;
                    padding: 10px;
                    background: white;
                    border-radius: 5px;
                    border-left: 4px solid #007bff;
                }}
                .field strong {{
                    color: #007bff;
                }}
            </style>
        </head>
        <body>
            <div class="header">
                <h2>📧 Yeni Əlaqə Mesajı</h2>
            </div>
            
            <div class="content">
                <div class="field">
                    <strong>Ad:</strong> {name}
                </div>
                
                <div class="field">
                    <strong>Email:</strong> {email}
                </div>
                
                <div class="field">
                    <strong>Mövzu:</strong> {subject}
                </div>
                
                <div class="field">
                    <strong>Mesaj:</strong><br>
                    {message}
                </div>
                
                <p style="margin-top: 20px; text-align: center; color: #666;">
                    Bu mesaj dostumkitab.az saytının əlaqə formasından göndərilib.
                </p>
            </div>
        </body>
        </html>
        """
        
        # Sadə mətn məzmunu
        plain_message = f"""
Yeni Əlaqə Mesajı

Ad: {name}
Email: {email}
Mövzu: {subject}

Mesaj:
{message}

Bu mesaj dostumkitab.az saytının əlaqə formasından göndərilib.
        """
        
        # Email göndəririk
        send_mail(
            subject=email_subject,
            message=strip_tags(plain_message),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.ADMIN_EMAIL],
            html_message=html_message,
            fail_silently=False,
        )
        
        print(f"✅ Əlaqə emaili göndərildi: {email}")
        return True
        
    except Exception as e:
        print(f"❌ Email göndərilmədi: {str(e)}")
        return False 