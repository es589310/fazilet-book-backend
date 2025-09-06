#!/usr/bin/env python3
"""
Production Security Check Script
Bu script production environment-də security settings-i yoxlayır
"""

import os
import sys
import django
from pathlib import Path

# Django setup
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kitab_backend.settings')

try:
    django.setup()
except Exception as e:
    print(f"❌ Django setup xətası: {e}")
    sys.exit(1)

from django.conf import settings
from django.core.management import execute_from_command_line

def check_security_settings():
    """Production security settings yoxlayır"""
    print("🔒 Production Security Check başlayır...\n")
    
    issues = []
    warnings = []
    
    # 1. DEBUG check
    if settings.DEBUG:
        issues.append("❌ DEBUG=True production-da təhlükəlidir!")
    else:
        print("✅ DEBUG=False")
    
    # 2. SECRET_KEY check
    if settings.SECRET_KEY == 'django-insecure-your-secret-key-here':
        issues.append("❌ SECRET_KEY default dəyərdədir!")
    else:
        print("✅ SECRET_KEY təyin edilib")
    
    # 3. HTTPS settings
    if not settings.DEBUG:
        if not getattr(settings, 'SECURE_SSL_REDIRECT', False):
            warnings.append("⚠️  SECURE_SSL_REDIRECT=False")
        else:
            print("✅ SECURE_SSL_REDIRECT=True")
        
        if not getattr(settings, 'SECURE_HSTS_SECONDS', 0):
            warnings.append("⚠️  SECURE_HSTS_SECONDS təyin edilməyib")
        else:
            print("✅ SECURE_HSTS_SECONDS təyin edilib")
    
    # 4. ALLOWED_HOSTS check
    if 'localhost' in settings.ALLOWED_HOSTS and not settings.DEBUG:
        warnings.append("⚠️  localhost production ALLOWED_HOSTS-də")
    else:
        print("✅ ALLOWED_HOSTS production-appropriate")
    
    # 5. CORS check
    if not settings.DEBUG:
        localhost_origins = [origin for origin in settings.CORS_ALLOWED_ORIGINS if 'localhost' in origin]
        if localhost_origins:
            warnings.append("⚠️  localhost CORS origins production-da")
        else:
            print("✅ CORS origins production-appropriate")
    
    # 6. Database SSL check
    if not settings.DEBUG:
        db_options = settings.DATABASES['default'].get('OPTIONS', {})
        if db_options.get('sslmode') != 'require':
            warnings.append("⚠️  Database SSL tələb edilmir")
        else:
            print("✅ Database SSL tələb olunur")
    
    # 7. Session security check
    if not settings.DEBUG:
        if not getattr(settings, 'SESSION_COOKIE_SECURE', False):
            warnings.append("⚠️  SESSION_COOKIE_SECURE=False")
        else:
            print("✅ SESSION_COOKIE_SECURE=True")
        
        if not getattr(settings, 'CSRF_COOKIE_SECURE', False):
            warnings.append("⚠️  CSRF_COOKIE_SECURE=False")
        else:
            print("✅ CSRF_COOKIE_SECURE=True")
    
    # 8. Logging level check
    if not settings.DEBUG:
        log_level = getattr(settings, 'LOG_LEVEL', 'DEBUG')
        if log_level == 'DEBUG':
            warnings.append("⚠️  LOG_LEVEL=DEBUG production-da")
        else:
            print(f"✅ LOG_LEVEL={log_level}")
    
    # 9. Hardcoded credentials check
    hardcoded_creds = [
        'csacstjcyxstized',
        'public_XkJMchYM6d4lYKOQlBvFmFY5jqs=',
        'private_t57buG/tbcXO31ClG09vQJazIK0='
    ]
    
    for cred in hardcoded_creds:
        if cred in str(settings):
            issues.append(f"❌ Hardcoded credential tapıldı: {cred}")
    
    if not any(cred in str(settings) for cred in hardcoded_creds):
        print("✅ Hardcoded credentials yoxdur")
    
    # Results
    print("\n" + "="*50)
    print("🔍 SECURITY CHECK RESULTS")
    print("="*50)
    
    if issues:
        print("\n🚨 CRITICAL ISSUES:")
        for issue in issues:
            print(f"  {issue}")
    
    if warnings:
        print("\n⚠️  WARNINGS:")
        for warning in warnings:
            print(f"  {warning}")
    
    if not issues and not warnings:
        print("\n🎉 Bütün security checks uğurlu!")
    
    # Recommendations
    print("\n📋 PRODUCTION RECOMMENDATIONS:")
    print("1. SSL sertifikatı quraşdırın (Let's Encrypt)")
    print("2. Web server (nginx/apache) konfiqurasiyası")
    print("3. Database backup strategy")
    print("4. Monitoring və logging")
    print("5. Regular security updates")
    print("6. Firewall konfiqurasiyası")
    
    return len(issues) == 0

def check_environment_variables():
    """Environment variables yoxlayır"""
    print("\n🔧 Environment Variables Check...")
    
    required_vars = [
        'SECRET_KEY',
        'DB_PASSWORD',
        'EMAIL_HOST_PASSWORD',
        'IMAGEKIT_PUBLIC_KEY',
        'IMAGEKIT_PRIVATE_KEY'
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Missing environment variables: {', '.join(missing_vars)}")
        return False
    else:
        print("✅ Bütün required environment variables mövcuddur")
        return True

def main():
    """Main function"""
    print("🚀 Kitab Backend Production Security Check")
    print("="*50)
    
    # Check environment variables
    env_ok = check_environment_variables()
    
    # Check Django security settings
    security_ok = check_security_settings()
    
    # Final result
    print("\n" + "="*50)
    if env_ok and security_ok:
        print("🎉 PRODUCTION READY! ✅")
        return 0
    else:
        print("❌ PRODUCTION NOT READY! Fix issues before deployment.")
        return 1

if __name__ == '__main__':
    sys.exit(main()) 