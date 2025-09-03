"""
Production Django Settings for Kitab Backend
Bu faylı production environment üçün istifadə edin
"""

import os
from pathlib import Path
from decouple import config

# Import base settings
from .base import *

# Production Security Settings
DEBUG = False
SECRET_KEY = config('SECRET_KEY')

# HTTPS Security
SECURE_SSL_REDIRECT = config('SECURE_SSL_REDIRECT', default=True, cast=bool)
SECURE_HSTS_SECONDS = config('SECURE_HSTS_SECONDS', default=31536000, cast=int)
SECURE_HSTS_INCLUDE_SUBDOMAINS = config('SECURE_HSTS_INCLUDE_SUBDOMAINS', default=True, cast=bool)
SECURE_HSTS_PRELOAD = config('SECURE_HSTS_PRELOAD', default=True, cast=bool)

# Security Headers
SECURE_BROWSER_XSS_FILTER = config('SECURE_BROWSER_XSS_FILTER', default=True, cast=bool)
SECURE_CONTENT_TYPE_NOSNIFF = config('SECURE_CONTENT_TYPE_NOSNIFF', default=True, cast=bool)
X_FRAME_OPTIONS = config('X_FRAME_OPTIONS', default='DENY')

# Session Security
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True

# Production Hosts
ALLOWED_HOSTS_STR = config('ALLOWED_HOSTS', default='dostumkitab.az,www.dostumkitab.az')
ALLOWED_HOSTS = [host.strip() for host in ALLOWED_HOSTS_STR.split(',')]

# Production CORS
CORS_ALLOWED_ORIGINS_STR = config('CORS_ALLOWED_ORIGINS', default='https://dostumkitab.az,https://www.dostumkitab.az')
CORS_ALLOWED_ORIGINS = [origin.strip() for origin in CORS_ALLOWED_ORIGINS_STR.split(',')]

# Database Configuration - Production Ready
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT'),
        'OPTIONS': {
            'sslmode': 'require',
        },
    }
}

# Alternative: Use DATABASE_URL if available
if config('DATABASE_URL', default=''):
    import dj_database_url
    DATABASES['default'] = dj_database_url.parse(config('DATABASE_URL'))

# Redis Configuration
REDIS_URL = config('REDIS_URL', default='')
if REDIS_URL:
    CACHES = {
        'default': {
            'BACKEND': 'django_redis.cache.RedisCache',
            'LOCATION': REDIS_URL,
            'OPTIONS': {
                'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            }
        }
    }

# Production Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': config('LOG_LEVEL', default='INFO'),
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': config('LOG_FILE', default='/var/log/django/kitab_backend.log'),
            'maxBytes': 1024*1024*5,  # 5 MB
            'backupCount': 5,
            'formatter': 'verbose',
        },
        'console': {
            'level': config('LOG_LEVEL', default='INFO'),
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': config('LOG_LEVEL', default='INFO'),
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': config('LOG_LEVEL', default='INFO'),
            'propagate': True,
        },
        'django.security': {
            'handlers': ['console', 'file'],
            'level': 'WARNING',
            'propagate': False,
        },
    },
}

# Email Configuration - Production Ready
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_PORT = config('EMAIL_PORT', cast=int)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL')
ADMIN_EMAIL = config('ADMIN_EMAIL')

# ImageKit Configuration - Production Ready
IMAGEKIT_ENABLED = config('IMAGEKIT_ENABLED', default=False, cast=bool)
IMAGEKIT_PUBLIC_KEY = config('IMAGEKIT_PUBLIC_KEY', default='')
IMAGEKIT_PRIVATE_KEY = config('IMAGEKIT_PRIVATE_KEY', default='')
IMAGEKIT_URL_ENDPOINT = config('IMAGEKIT_URL_ENDPOINT', default='')
IMAGEKIT_FOLDER = config('IMAGEKIT_FOLDER', default='dostumkitab')

# Production ImageKit fallback
if not IMAGEKIT_ENABLED:
    IMAGEKIT_PUBLIC_KEY = ''
    IMAGEKIT_PRIVATE_KEY = ''
    IMAGEKIT_URL_ENDPOINT = ''

# Static and Media files - Production
STATIC_ROOT = '/app/static'
MEDIA_ROOT = '/app/media'

# Security middleware
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # For static files
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# WhiteNoise configuration
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Production specific apps
if config('IMAGEKIT_ENABLED', default=False, cast=bool):
    INSTALLED_APPS += ['imagekitio']

# Sentry configuration (if available)
SENTRY_DSN = config('SENTRY_DSN', default='')
if SENTRY_DSN:
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration
    
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[DjangoIntegration()],
        traces_sample_rate=1.0,
        send_default_pii=True
    ) 