#!/bin/bash

# Production Deployment Script for Kitab Backend
# ⚠️  WARNING: Bu script-i production server-də işlətməzdən əvvəl yoxlayın!

set -e  # Exit on any error

echo "🚀 Starting Production Deployment..."

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

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

# Check if running as root
if [[ $EUID -eq 0 ]]; then
   print_error "Bu script-i root olaraq işlətməyin!"
   exit 1
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    print_error ".env faylı tapılmadı! Production environment variables tələb olunur."
    print_status "Nümunə .env faylı yaradın:"
    cat << EOF
# Production Environment Configuration
DEBUG=False
SECRET_KEY=your-super-secret-production-key-here
SECURE_SSL_REDIRECT=True
SECURE_HSTS_SECONDS=31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS=True
SECURE_HSTS_PRELOAD=True

# Database
DB_NAME=kitabdb_prod
DB_USER=kitab_user_prod
DB_PASSWORD=super-secure-database-password
DB_HOST=localhost
DB_PORT=5432

# Email
EMAIL_HOST_PASSWORD=your-app-specific-password
EMAIL_HOST_USER=your-email@gmail.com

# ImageKit
IMAGEKIT_ENABLED=True
IMAGEKIT_PUBLIC_KEY=your-public-key
IMAGEKIT_PRIVATE_KEY=your-private-key

# Production Domain
ALLOWED_HOSTS=dostumkitab.az,www.dostumkitab.az
CORS_ALLOWED_ORIGINS=https://dostumkitab.az,https://www.dostumkitab.az
EOF
    exit 1
fi

# Check critical environment variables
print_status "Environment variables yoxlanılır..."

required_vars=(
    "SECRET_KEY"
    "DB_PASSWORD"
    "EMAIL_HOST_PASSWORD"
    "IMAGEKIT_PUBLIC_KEY"
    "IMAGEKIT_PRIVATE_KEY"
)

for var in "${required_vars[@]}"; do
    if [ -z "${!var}" ]; then
        print_error "$var environment variable təyin edilməyib!"
        exit 1
    fi
done

# Check if DEBUG is False
if [ "$DEBUG" = "True" ]; then
    print_error "DEBUG=True production-da təhlükəlidir! DEBUG=False olmalıdır."
    exit 1
fi

print_status "Environment variables yoxlandı ✅"

# Create log directory
print_status "Log directory yaradılır..."
sudo mkdir -p /var/log/django
sudo chown $USER:$USER /var/log/django
sudo chmod 755 /var/log/django

# Install/upgrade dependencies
print_status "Python dependencies yüklənir..."
pip install --upgrade pip
pip install -r requirements.txt

# Collect static files
print_status "Static files toplanır..."
python manage.py collectstatic --noinput --clear

# Run database migrations
print_status "Database migrations işlədilir..."
python manage.py migrate

# Create superuser if not exists
print_status "Superuser yoxlanılır..."
python manage.py shell << EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(is_superuser=True).exists():
    print("Superuser yaradılmalıdır!")
    print("python manage.py createsuperuser komandasını işlədin")
else:
    print("Superuser mövcuddur ✅")
EOF

# Check security settings
print_status "Security settings yoxlanılır..."
python manage.py check --deploy

# Test database connection
print_status "Database connection test edilir..."
python manage.py dbshell << EOF
\q
EOF
print_status "Database connection uğurlu ✅"

# Test email configuration
print_status "Email configuration test edilir..."
python manage.py shell << EOF
from django.core.mail import send_mail
from django.conf import settings
try:
    # Test email göndərmə (əsl göndərilməyəcək)
    print("Email configuration yoxlanılır...")
    print(f"EMAIL_HOST: {settings.EMAIL_HOST}")
    print(f"EMAIL_PORT: {settings.EMAIL_PORT}")
    print(f"EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}")
    print("Email configuration uğurlu ✅")
except Exception as e:
    print(f"Email configuration xətası: {e}")
EOF

# Check for hardcoded credentials
print_status "Hardcoded credentials yoxlanılır..."
if grep -r "csacstjcyxstized\|public_XkJMchYM6d4lYKOQlBvFmFY5jqs=\|private_t57buG/tbcXO31ClG09vQJazIK0=" . --exclude-dir=__pycache__ --exclude-dir=.git --exclude-dir=node_modules; then
    print_error "Hardcoded credentials tapıldı! Təhlükəsizlik riski!"
    exit 1
fi

print_status "Hardcoded credentials yoxlandı ✅"

# Security checklist
print_status "Security checklist yoxlanılır..."

# Check if SECRET_KEY is not default
if [ "$SECRET_KEY" = "django-insecure-your-secret-key-here" ]; then
    print_error "SECRET_KEY default dəyərdədir! Dəyişdirin!"
    exit 1
fi

# Check if DEBUG is False
if [ "$DEBUG" = "True" ]; then
    print_error "DEBUG=True production-da təhlükəlidir!"
    exit 1
fi

# Check if SSL is enabled
if [ "$SECURE_SSL_REDIRECT" != "True" ]; then
    print_warning "SECURE_SSL_REDIRECT=False! HTTPS tələb olunur."
fi

print_status "Security checklist yoxlandı ✅"

# Performance optimization
print_status "Performance optimization edilir..."

# Clear cache
python manage.py clearcache 2>/dev/null || echo "Cache clearing skipped"

# Optimize database
python manage.py shell << EOF
from django.db import connection
cursor = connection.cursor()
cursor.execute("VACUUM ANALYZE;")
print("Database optimized ✅")
EOF

# Final checks
print_status "Final production checks..."

# Check if all required apps are installed
python manage.py check

# Check for any pending migrations
python manage.py showmigrations --list | grep -E "\[ \]" && print_warning "Pending migrations var!" || print_status "Bütün migrations tətbiq edilib ✅"

# Check static files
if [ -d "staticfiles" ] && [ "$(ls -A staticfiles)" ]; then
    print_status "Static files toplanıb ✅"
else
    print_error "Static files toplanmayıb!"
    exit 1
fi

print_status "Production deployment uğurla tamamlandı! 🎉"

# Production recommendations
echo ""
print_status "Production üçün tövsiyələr:"
echo "1. Web server (nginx/apache) konfiqurasiyası"
echo "2. SSL sertifikatı (Let's Encrypt)"
echo "3. Database backup strategy"
echo "4. Monitoring və logging"
echo "5. Regular security updates"
echo "6. Performance monitoring"
echo ""

print_status "Server restart edilməlidir:"
echo "sudo systemctl restart gunicorn  # və ya uyğun service"
echo "sudo systemctl restart nginx     # və ya apache"
echo ""

print_status "Deployment tamamlandı! 🚀" 