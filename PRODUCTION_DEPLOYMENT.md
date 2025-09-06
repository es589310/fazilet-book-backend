# 🚀 Kitab Backend Production Deployment Guide

Bu sənəd Django backend-i production-a deploy etmək üçün tam təlimatları təqdim edir.

## 📋 Pre-Deployment Checklist

### ✅ Security Checks
- [ ] Hardcoded credentials yoxdur
- [ ] DEBUG=False production-da
- [ ] SECRET_KEY təyin edilib
- [ ] SSL sertifikatı mövcuddur
- [ ] Production CORS origins təyin edilib
- [ ] Database SSL tələb olunur

### ✅ Environment Variables
- [ ] `.env` faylı yaradılıb
- [ ] Bütün required variables təyin edilib
- [ ] Production database credentials
- [ ] Email configuration
- [ ] ImageKit credentials

### ✅ Code Quality
- [ ] Security check script işlədilib
- [ ] Bütün tests keçir
- [ ] Code linting tamamlanıb
- [ ] Performance optimization edilib

## 🖥️ Server Setup

### 1. Server Requirements
```bash
# Minimum system requirements
CPU: 2 cores
RAM: 4GB
Storage: 20GB SSD
OS: Ubuntu 20.04+ / CentOS 8+
```

### 2. System Updates
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y curl wget git build-essential
```

### 3. Python Installation
```bash
# Python 3.9+ installation
sudo apt install -y python3 python3-pip python3-venv
sudo apt install -y python3-dev libpq-dev
```

### 4. PostgreSQL Installation
```bash
sudo apt install -y postgresql postgresql-contrib
sudo systemctl enable postgresql
sudo systemctl start postgresql

# Database setup
sudo -u postgres createuser kitab_user_prod
sudo -u postgres createdb kitabdb_prod
sudo -u postgres psql -c "ALTER USER kitab_user_prod PASSWORD 'your-secure-password';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE kitabdb_prod TO kitab_user_prod;"
```

### 5. Nginx Installation
```bash
sudo apt install -y nginx
sudo systemctl enable nginx
sudo systemctl start nginx
```

## 📁 Application Deployment

### 1. Application Directory
```bash
sudo mkdir -p /var/www/kitab_backend
sudo chown $USER:$USER /var/www/kitab_backend
cd /var/www/kitab_backend
```

### 2. Code Deployment
```bash
# Clone repository
git clone https://github.com/your-repo/kitab_backend.git .

# Or copy files
sudo cp -r /path/to/your/project/* /var/www/kitab_backend/
```

### 3. Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.production.txt
```

### 4. Environment Configuration
```bash
# Create .env file
cp .env.example .env
nano .env

# Required variables
DEBUG=False
SECRET_KEY=your-super-secret-production-key
DB_NAME=kitabdb_prod
DB_USER=kitab_user_prod
DB_PASSWORD=your-secure-password
EMAIL_HOST_PASSWORD=your-email-password
IMAGEKIT_PUBLIC_KEY=your-imagekit-public-key
IMAGEKIT_PRIVATE_KEY=your-imagekit-private-key
ALLOWED_HOSTS=dostumkitab.az,www.dostumkitab.az
CORS_ALLOWED_ORIGINS=https://dostumkitab.az,https://www.dostumkitab.az
```

### 5. Django Setup
```bash
# Collect static files
python manage.py collectstatic --noinput

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Test configuration
python manage.py check --deploy
```

## 🔧 Service Configuration

### 1. Gunicorn Service
```bash
# Copy service file
sudo cp kitab-backend.service /etc/systemd/system/

# Reload systemd
sudo systemctl daemon-reload

# Enable and start service
sudo systemctl enable kitab-backend
sudo systemctl start kitab-backend

# Check status
sudo systemctl status kitab-backend
```

### 2. Nginx Configuration
```bash
# Copy nginx config
sudo cp nginx/kitab-backend.conf /etc/nginx/sites-available/

# Enable site
sudo ln -s /etc/nginx/sites-available/kitab-backend.conf /etc/nginx/sites-enabled/

# Test configuration
sudo nginx -t

# Reload nginx
sudo systemctl reload nginx
```

### 3. SSL Certificate (Let's Encrypt)
```bash
# Install certbot
sudo apt install -y certbot python3-certbot-nginx

# Get SSL certificate
sudo certbot --nginx -d dostumkitab.az -d www.dostumkitab.az

# Auto-renewal
sudo crontab -e
# Add: 0 12 * * * /usr/bin/certbot renew --quiet
```

## 📊 Monitoring Setup

### 1. Monitoring Script
```bash
# Copy monitoring script
sudo cp monitor-production.sh /usr/local/bin/
sudo chmod +x /usr/local/bin/monitor-production.sh

# Create cron job for regular monitoring
sudo crontab -e
# Add: */5 * * * * /usr/local/bin/monitor-production.sh
```

### 2. Log Management
```bash
# Create log directories
sudo mkdir -p /var/log/django
sudo chown www-data:www-data /var/log/django

# Log rotation
sudo nano /etc/logrotate.d/kitab-backend

# Add:
/var/log/django/*.log {
    daily
    missingok
    rotate 30
    compress
    delaycompress
    notifempty
    create 644 www-data www-data
    postrotate
        systemctl reload kitab-backend
    endscript
}
```

## 🔒 Security Hardening

### 1. Firewall Configuration
```bash
# UFW firewall
sudo ufw allow ssh
sudo ufw allow 80
sudo ufw allow 443
sudo ufw enable
```

### 2. Fail2ban Installation
```bash
sudo apt install -y fail2ban
sudo systemctl enable fail2ban
sudo systemctl start fail2ban

# Configure fail2ban
sudo nano /etc/fail2ban/jail.local
```

### 3. Regular Security Updates
```bash
# Automatic security updates
sudo apt install -y unattended-upgrades
sudo dpkg-reconfigure -plow unattended-upgrades
```

## 🚀 Deployment Verification

### 1. Health Check
```bash
# Test health endpoint
curl https://dostumkitab.az/health/

# Expected response:
{
    "status": "healthy",
    "timestamp": "2024-01-01T12:00:00Z",
    "services": {
        "database": "healthy",
        "application": "healthy",
        "environment": "production"
    },
    "version": "1.0.0"
}
```

### 2. Performance Test
```bash
# Load testing with Apache Bench
sudo apt install -y apache2-utils
ab -n 1000 -c 10 https://dostumkitab.az/health/
```

### 3. Security Scan
```bash
# Install security scanner
sudo apt install -y lynis

# Run security audit
sudo lynis audit system
```

## 📈 Performance Optimization

### 1. Database Optimization
```bash
# PostgreSQL tuning
sudo nano /etc/postgresql/*/main/postgresql.conf

# Key settings:
shared_buffers = 256MB
effective_cache_size = 1GB
work_mem = 4MB
maintenance_work_mem = 64MB
```

### 2. Redis Caching
```bash
# Install Redis
sudo apt install -y redis-server
sudo systemctl enable redis-server
sudo systemctl start redis-server
```

### 3. CDN Setup
```bash
# Configure Cloudflare or similar CDN
# Update ALLOWED_HOSTS and CORS settings
```

## 🆘 Troubleshooting

### Common Issues

#### 1. Service Won't Start
```bash
# Check logs
sudo journalctl -u kitab-backend -f

# Check permissions
sudo chown -R www-data:www-data /var/www/kitab_backend
```

#### 2. Database Connection Issues
```bash
# Test connection
sudo -u postgres psql -d kitabdb_prod -c "SELECT 1;"

# Check PostgreSQL status
sudo systemctl status postgresql
```

#### 3. Static Files Not Loading
```bash
# Check static files
ls -la /var/www/kitab_backend/staticfiles/

# Recollect static files
python manage.py collectstatic --noinput --clear
```

## 📞 Support & Maintenance

### 1. Regular Maintenance
- [ ] Weekly security updates
- [ ] Monthly performance review
- [ ] Quarterly security audit
- [ ] Annual backup testing

### 2. Monitoring Alerts
- [ ] Email alerts configured
- [ ] SMS alerts (optional)
- [ ] Slack/Discord integration
- [ ] Uptime monitoring

### 3. Backup Strategy
- [ ] Database daily backup
- [ ] Code repository backup
- [ ] Configuration backup
- [ ] Disaster recovery plan

## 🎯 Success Metrics

### Performance Targets
- Response time: < 200ms
- Uptime: > 99.9%
- Error rate: < 0.1%
- Database queries: < 100ms

### Security Targets
- Zero hardcoded credentials
- All security headers enabled
- SSL certificate valid
- Regular security updates

---

**🎉 Congratulations! Your Django backend is now production-ready!**

For additional support, check the monitoring logs and system status regularly. 