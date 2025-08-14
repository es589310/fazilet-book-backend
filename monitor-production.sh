#!/bin/bash

# Production Monitoring Script for Kitab Backend
# Bu script-i production server-də regular olaraq işlədin

set -e

# Configuration
APP_URL="https://dostumkitab.az"
HEALTH_ENDPOINT="/health/"
LOG_FILE="/var/log/django/monitoring.log"
ALERT_EMAIL="admin@dostumkitab.az"

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Timestamp
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

# Function to log messages
log_message() {
    echo "[$TIMESTAMP] $1" | tee -a "$LOG_FILE"
}

# Function to send alert
send_alert() {
    local message="$1"
    log_message "🚨 ALERT: $message"
    
    # Send email alert (if mail command available)
    if command -v mail &> /dev/null; then
        echo "$message" | mail -s "Kitab Backend Alert" "$ALERT_EMAIL"
    fi
}

# Function to check application health
check_health() {
    log_message "🔍 Checking application health..."
    
    local response
    local status_code
    
    if response=$(curl -s -w "%{http_code}" "$APP_URL$HEALTH_ENDPOINT" 2>/dev/null); then
        status_code="${response: -3}"
        response_body="${response%???}"
        
        if [ "$status_code" -eq 200 ]; then
            log_message "✅ Health check passed (HTTP $status_code)"
            
            # Check if response contains "healthy"
            if echo "$response_body" | grep -q '"status":"healthy"'; then
                log_message "✅ Application status: healthy"
            else
                log_message "⚠️  Application status: unhealthy"
                send_alert "Application health check failed - status unhealthy"
            fi
        else
            log_message "❌ Health check failed (HTTP $status_code)"
            send_alert "Health check failed with HTTP $status_code"
        fi
    else
        log_message "❌ Health check request failed"
        send_alert "Health check request failed - connection error"
    fi
}

# Function to check database connection
check_database() {
    log_message "🔍 Checking database connection..."
    
    if cd /var/www/kitab_backend && source venv/bin/activate; then
        if python manage.py dbshell <<< "\q" &>/dev/null; then
            log_message "✅ Database connection: healthy"
        else
            log_message "❌ Database connection: failed"
            send_alert "Database connection failed"
        fi
    else
        log_message "❌ Failed to activate virtual environment"
        send_alert "Failed to activate virtual environment"
    fi
}

# Function to check disk space
check_disk_space() {
    log_message "🔍 Checking disk space..."
    
    local disk_usage=$(df / | awk 'NR==2 {print $5}' | sed 's/%//')
    
    if [ "$disk_usage" -gt 90 ]; then
        log_message "🚨 Disk usage critical: ${disk_usage}%"
        send_alert "Disk usage critical: ${disk_usage}%"
    elif [ "$disk_usage" -gt 80 ]; then
        log_message "⚠️  Disk usage high: ${disk_usage}%"
    else
        log_message "✅ Disk usage: ${disk_usage}%"
    fi
}

# Function to check memory usage
check_memory() {
    log_message "🔍 Checking memory usage..."
    
    local memory_usage=$(free | awk 'NR==2{printf "%.0f", $3*100/$2}')
    
    if [ "$memory_usage" -gt 90 ]; then
        log_message "🚨 Memory usage critical: ${memory_usage}%"
        send_alert "Memory usage critical: ${memory_usage}%"
    elif [ "$memory_usage" -gt 80 ]; then
        log_message "⚠️  Memory usage high: ${memory_usage}%"
    else
        log_message "✅ Memory usage: ${memory_usage}%"
    fi
}

# Function to check service status
check_services() {
    log_message "🔍 Checking service status..."
    
    # Check Gunicorn service
    if systemctl is-active --quiet kitab-backend; then
        log_message "✅ Gunicorn service: running"
    else
        log_message "❌ Gunicorn service: stopped"
        send_alert "Gunicorn service stopped"
    fi
    
    # Check Nginx service
    if systemctl is-active --quiet nginx; then
        log_message "✅ Nginx service: running"
    else
        log_message "❌ Nginx service: stopped"
        send_alert "Nginx service stopped"
    fi
    
    # Check PostgreSQL service
    if systemctl is-active --quiet postgresql; then
        log_message "✅ PostgreSQL service: running"
    else
        log_message "❌ PostgreSQL service: stopped"
        send_alert "PostgreSQL service stopped"
    fi
}

# Function to check log files
check_logs() {
    log_message "🔍 Checking log files..."
    
    local log_dir="/var/log/django"
    local max_size_mb=100
    
    for log_file in "$log_dir"/*.log; do
        if [ -f "$log_file" ]; then
            local size_mb=$(du -m "$log_file" | cut -f1)
            local filename=$(basename "$log_file")
            
            if [ "$size_mb" -gt "$max_size_mb" ]; then
                log_message "⚠️  Log file $filename is large: ${size_mb}MB"
                
                # Rotate log file if too large
                if [ "$size_mb" -gt 200 ]; then
                    log_message "🔄 Rotating large log file: $filename"
                    mv "$log_file" "${log_file}.old"
                    touch "$log_file"
                    systemctl reload kitab-backend
                fi
            else
                log_message "✅ Log file $filename: ${size_mb}MB"
            fi
        fi
    done
}

# Function to check SSL certificate
check_ssl() {
    log_message "🔍 Checking SSL certificate..."
    
    local cert_expiry
    if cert_expiry=$(echo | openssl s_client -servername "$APP_URL" -connect "$APP_URL:443" 2>/dev/null | openssl x509 -noout -dates | grep notAfter | cut -d= -f2); then
        local expiry_date=$(date -d "$cert_expiry" +%s)
        local current_date=$(date +%s)
        local days_until_expiry=$(( (expiry_date - current_date) / 86400 ))
        
        if [ "$days_until_expiry" -lt 7 ]; then
            log_message "🚨 SSL certificate expires in $days_until_expiry days"
            send_alert "SSL certificate expires in $days_until_expiry days"
        elif [ "$days_until_expiry" -lt 30 ]; then
            log_message "⚠️  SSL certificate expires in $days_until_expiry days"
        else
            log_message "✅ SSL certificate expires in $days_until_expiry days"
        fi
    else
        log_message "❌ Failed to check SSL certificate"
        send_alert "Failed to check SSL certificate"
    fi
}

# Function to check performance
check_performance() {
    log_message "🔍 Checking application performance..."
    
    local start_time=$(date +%s.%N)
    local response_time
    
    if response_time=$(curl -s -w "%{time_total}" "$APP_URL$HEALTH_ENDPOINT" -o /dev/null 2>/dev/null); then
        local response_ms=$(echo "$response_time * 1000" | bc -l | cut -d. -f1)
        
        if [ "$response_ms" -gt 5000 ]; then
            log_message "🚨 Response time slow: ${response_ms}ms"
            send_alert "Application response time slow: ${response_ms}ms"
        elif [ "$response_ms" -gt 2000 ]; then
            log_message "⚠️  Response time high: ${response_ms}ms"
        else
            log_message "✅ Response time: ${response_ms}ms"
        fi
    else
        log_message "❌ Failed to measure response time"
    fi
}

# Function to cleanup old logs
cleanup_old_logs() {
    log_message "🧹 Cleaning up old log files..."
    
    local log_dir="/var/log/django"
    local days_to_keep=30
    
    # Remove old log files
    find "$log_dir" -name "*.log.old" -mtime +$days_to_keep -delete 2>/dev/null || true
    find "$log_dir" -name "*.log.*" -mtime +$days_to_keep -delete 2>/dev/null || true
    
    log_message "✅ Cleanup completed"
}

# Main monitoring function
main() {
    log_message "🚀 Starting production monitoring..."
    
    # Create log directory if not exists
    mkdir -p "$(dirname "$LOG_FILE")"
    
    # Run all checks
    check_health
    check_database
    check_disk_space
    check_memory
    check_services
    check_logs
    check_ssl
    check_performance
    
    # Cleanup old logs (once per day)
    if [ "$(date +%H)" = "02" ]; then
        cleanup_old_logs
    fi
    
    log_message "✅ Monitoring completed"
    echo ""
}

# Run main function
main "$@" 