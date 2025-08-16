"""
Development Django Settings for Kitab Backend
Bu faylı development environment üçün istifadə edin
"""

from .base import *

# Development Security Settings
DEBUG = True
SECRET_KEY = env('SECRET_KEY', default='django-insecure-your-secret-key-here')

# Development Hosts
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0']

# Development CORS
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:3001",
    "http://127.0.0.1:3001",
]

# Database Configuration - Development
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('DB_NAME', default='kitabdb'),
        'USER': env('DB_USER', default='kitabb_user'),
        'PASSWORD': env('DB_PASSWORD', default='1a2b3d'),
        'HOST': env('DB_HOST', default='localhost'),
        'PORT': env('DB_PORT', default='5432'),
        'OPTIONS': {
            'sslmode': 'disable',
        },
    }
}

# Development Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'debug.log'),
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'DEBUG',
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

# Email Configuration - Development
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Static and Media files - Development
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# ImageKit Configuration - Development
IMAGEKIT_ENABLED = env.bool('IMAGEKIT_ENABLED', default=False)
IMAGEKIT_PUBLIC_KEY = env('IMAGEKIT_PUBLIC_KEY', default='')
IMAGEKIT_PRIVATE_KEY = env('IMAGEKIT_PRIVATE_KEY', default='')
IMAGEKIT_URL_ENDPOINT = env('IMAGEKIT_URL_ENDPOINT', default='')
IMAGEKIT_FOLDER = env('IMAGEKIT_FOLDER', default='dostumkitab')

# Development ImageKit fallback
if not IMAGEKIT_ENABLED:
    IMAGEKIT_PUBLIC_KEY = ''
    IMAGEKIT_PRIVATE_KEY = ''
    IMAGEKIT_URL_ENDPOINT = '' 