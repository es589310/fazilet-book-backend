# heroku.py – Heroku Production Settings

import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# DEBUG
DEBUG = os.environ.get("DEBUG", "False") == "True"

# SECRET_KEY
SECRET_KEY = os.environ.get("SECRET_KEY", "django-insecure-default-secret-key")

# IS_HEROKU flag (Heroku env variable)
IS_HEROKU = os.environ.get("IS_HEROKU", "False") == "True"

# Allowed Hosts
# 1. Env-dən oxu
allowed_hosts_env = os.environ.get(
    "ALLOWED_HOSTS",
    "localhost,127.0.0.1"
)
ALLOWED_HOSTS = [host.strip() for host in allowed_hosts_env.split(",")]

# 2. Heroku-da *.herokuapp.com əlavə et
if IS_HEROKU:
    heroku_app_host = os.environ.get("HEROKU_APP_NAME")
    if heroku_app_host:
        ALLOWED_HOSTS.append(f"{heroku_app_host}.herokuapp.com")

# CORS
cors_origins_env = os.environ.get("CORS_ALLOWED_ORIGINS", "")
CORS_ALLOWED_ORIGINS = [origin.strip() for origin in cors_origins_env.split(",") if origin.strip()]

# Database (Heroku DATABASE_URL)
import dj_database_url
DATABASES = {
    "default": dj_database_url.config(
        default=os.environ.get("DATABASE_URL")
    )
}

# Static and Media files (WhiteNoise for Heroku)
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# WhiteNoise settings
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    # Əvvəlki middleware-lər
]

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Email
EMAIL_HOST = os.environ.get("EMAIL_HOST", "smtp.gmail.com")
EMAIL_PORT = int(os.environ.get("EMAIL_PORT", 587))
EMAIL_USE_TLS = os.environ.get("EMAIL_USE_TLS", "True") == "True"
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", "")
DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL", EMAIL_HOST_USER)
ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL", EMAIL_HOST_USER)

# ImageKit
IMAGEKIT_ENABLED = os.environ.get("IMAGEKIT_ENABLED", "False") == "True"
IMAGEKIT_PUBLIC_KEY = os.environ.get("IMAGEKIT_PUBLIC_KEY", "")
IMAGEKIT_PRIVATE_KEY = os.environ.get("IMAGEKIT_PRIVATE_KEY", "")
IMAGEKIT_URL_ENDPOINT = os.environ.get("IMAGEKIT_URL_ENDPOINT", "")
IMAGEKIT_FOLDER = os.environ.get("IMAGEKIT_FOLDER", "books")

# Logging
LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")
