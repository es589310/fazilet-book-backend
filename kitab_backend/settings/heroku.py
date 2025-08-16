"""
Heroku Django Settings for Kitab Backend
Bu faylı Heroku production environment üçün istifadə edin
"""

import os
import dj_database_url
from .base import *

# Heroku Environment Detection
IS_HEROKU = os.environ.get('IS_HEROKU', 'True').lower() == 'true'

# Production Security Settings
DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'
SECRET_KEY = os.environ.get('SECRET_KEY')

# HTTPS Security (Heroku automatically provides HTTPS)
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Security Headers
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Session Security
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True

# Production Hosts
ALLOWED_HOSTS_STR = os.environ.get('ALLOWED_HOSTS', 'dostumkitab.az,www.dostumkitab.az,dostumkitabapp-bb96d7362d57.herokuapp.com,dostumkitabapp-backend-b9b3b208224b.herokuapp.com')
ALLOWED_HOSTS = [host.strip() for host in ALLOWED_HOSTS_STR.split(',')]

# Production CORS
CORS_ALLOWED_ORIGINS_STR = os.environ.get('CORS_ALLOWED_ORIGINS', 'https://dostumkitab.az,https://www.dostumkitab.az,https://dostumkitabapp-bb96d7362d57.herokuapp.com,https://dostumkitabapp-backend-b9b3b208224b.herokuapp.com')
CORS_ALLOWED_ORIGINS = [origin.strip() for origin in CORS_ALLOWED_ORIGINS_STR.split(',')]

# Database Configuration - Heroku PostgreSQL
DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL'),
        conn_max_age=600,
        conn_health_checks=True,
    )
}

# Redis Configuration (if available)
REDIS_URL = os.environ.get('REDIS_URL')
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
        'console': {
            'level': os.environ.get('LOG_LEVEL', 'INFO'),
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': os.environ.get('LOG_LEVEL', 'INFO'),
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.environ.get('LOG_LEVEL', 'INFO'),
            'propagate': True,
        },
        'django.security': {
            'handlers': ['console'],
            'level': 'WARNING',
            'propagate': False,
        },
    },
}

# Email Configuration - Heroku Ready
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', '587'))
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', 'True').lower() == 'true'
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL')
ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL')

# ImageKit Configuration - Heroku Ready
IMAGEKIT_ENABLED = os.environ.get('IMAGEKIT_ENABLED', 'False').lower() == 'true'
IMAGEKIT_PUBLIC_KEY = os.environ.get('IMAGEKIT_PUBLIC_KEY', '')
IMAGEKIT_PRIVATE_KEY = os.environ.get('IMAGEKIT_PRIVATE_KEY', '')
IMAGEKIT_URL_ENDPOINT = os.environ.get('IMAGEKIT_URL_ENDPOINT', '')
IMAGEKIT_FOLDER = os.environ.get('IMAGEKIT_FOLDER', 'dostumkitab')

# Production ImageKit fallback
if not IMAGEKIT_ENABLED:
    IMAGEKIT_PUBLIC_KEY = ''
    IMAGEKIT_PRIVATE_KEY = ''
    IMAGEKIT_URL_ENDPOINT = ''

# Static and Media files - Heroku
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# WhiteNoise for static files (Heroku)
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Production specific apps
if IMAGEKIT_ENABLED:
    INSTALLED_APPS += ['imagekitio']

# Sentry configuration (if available)
SENTRY_DSN = os.environ.get('SENTRY_DSN')
if SENTRY_DSN:
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration
    
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[DjangoIntegration()],
        traces_sample_rate=1.0,
        send_default_pii=True
    )

# Heroku specific settings
if IS_HEROKU:
    # Trust Heroku's proxy
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    
    # Allow all hosts in Heroku
    ALLOWED_HOSTS = ['*'] 