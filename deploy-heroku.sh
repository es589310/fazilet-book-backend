#!/bin/bash

# Heroku Deployment Script for Kitab Backend
# Bu script-i Heroku production deployment üçün istifadə edin

set -e

echo "🚀 Starting Heroku Deployment..."

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Heroku CLI is installed
if ! command -v heroku &> /dev/null; then
    print_error "Heroku CLI quraşdırılmayıb!"
    print_status "Quraşdırmaq üçün: https://devcenter.heroku.com/articles/heroku-cli"
    exit 1
fi

# Check if logged in to Heroku
if ! heroku auth:whoami &> /dev/null; then
    print_error "Heroku-a giriş edilməyib!"
    print_status "Giriş etmək üçün: heroku login"
    exit 1
fi

# Get app name from user
read -p "Heroku app adını daxil edin: " APP_NAME

if [ -z "$APP_NAME" ]; then
    print_error "App adı daxil edilməyib!"
    exit 1
fi

print_status "Heroku app: $APP_NAME"

# Check if app exists
if ! heroku apps:info --app "$APP_NAME" &> /dev/null; then
    print_status "Yeni Heroku app yaradılır: $APP_NAME"
    heroku create "$APP_NAME"
fi

# Set Heroku environment variables
print_status "Environment variables təyin edilir..."

# Django Security
heroku config:set DEBUG=False --app "$APP_NAME"
heroku config:set SECRET_KEY="$(python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')" --app "$APP_NAME"
heroku config:set IS_HEROKU=True --app "$APP_NAME"

# Production Domain
heroku config:set ALLOWED_HOSTS="faziletkitab.az,www.faziletkitab.az,$APP_NAME.herokuapp.com" --app "$APP_NAME"
heroku config:set CORS_ALLOWED_ORIGINS="https://dostumkitab.az,https://www.dostumkitab.az" --app "$APP_NAME"

# Email Configuration
heroku config:set EMAIL_HOST="smtp.gmail.com" --app "$APP_NAME"
heroku config:set EMAIL_PORT="587" --app "$APP_NAME"
heroku config:set EMAIL_USE_TLS="True" --app "$APP_NAME"
heroku config:set EMAIL_HOST_USER="your-email@gmail.com" --app "$APP_NAME"
heroku config:set EMAIL_HOST_PASSWORD="your-app-specific-password" --app "$APP_NAME"
heroku config:set DEFAULT_FROM_EMAIL="your-email@gmail.com" --app "$APP_NAME"
heroku config:set ADMIN_EMAIL="admin@faziletkitab.az" --app "$APP_NAME"

# ImageKit Configuration
heroku config:set IMAGEKIT_ENABLED="True" --app "$APP_NAME"
heroku config:set IMAGEKIT_PUBLIC_KEY="your-imagekit-public-key" --app "$APP_NAME"
heroku config:set IMAGEKIT_PRIVATE_KEY="your-imagekit-private-key" --app "$APP_NAME"
heroku config:set IMAGEKIT_URL_ENDPOINT="https://ik.imagekit.io/your-endpoint" --app "$APP_NAME"
heroku config:set IMAGEKIT_FOLDER="faziletkitab" --app "$APP_NAME"

# Logging
heroku config:set LOG_LEVEL="INFO" --app "$APP_NAME"

print_status "Environment variables təyin edildi ✅"

# Add PostgreSQL addon
print_status "PostgreSQL addon əlavə edilir..."
heroku addons:create heroku-postgresql:mini --app "$APP_NAME"

# Wait for database to be ready
print_status "Database hazırlanır..."
sleep 10

# Add Redis addon (optional)
read -p "Redis cache əlavə etmək istəyirsiniz? (y/n): " ADD_REDIS
if [[ $ADD_REDIS =~ ^[Yy]$ ]]; then
    print_status "Redis addon əlavə edilir..."
    heroku addons:create heroku-redis:mini --app "$APP_NAME"
fi

# Deploy to Heroku
print_status "Kod Heroku-ya deploy edilir..."
git add .
git commit -m "Heroku deployment preparation"
git push heroku main

# Run migrations
print_status "Database migrations işlədilir..."
heroku run python manage.py migrate --app "$APP_NAME"

# Collect static files
print_status "Static files toplanır..."
heroku run python manage.py collectstatic --noinput --app "$APP_NAME"

# Create superuser
print_status "Superuser yaradılır..."
heroku run python manage.py createsuperuser --app "$APP_NAME"

# Check deployment
print_status "Deployment yoxlanılır..."
heroku run python manage.py check --deploy --app "$APP_NAME"

# Open app
print_status "App açılır..."
heroku open --app "$APP_NAME"

print_status "Heroku deployment uğurla tamamlandı! 🎉"

# Show app info
print_status "App məlumatları:"
heroku info --app "$APP_NAME"

# Show logs
print_status "Logları görmək üçün: heroku logs --tail --app $APP_NAME" 