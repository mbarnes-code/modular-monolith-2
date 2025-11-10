# MISP Deployment Guide

## Overview

This guide provides comprehensive deployment instructions for the MISP integration within the modular monolith platform. The deployment maintains full compatibility with existing MISP installations while providing enhanced performance and security.

## Table of Contents

1. [System Requirements](#system-requirements)
2. [Pre-Deployment Checklist](#pre-deployment-checklist)
3. [Environment Configuration](#environment-configuration)
4. [Database Setup](#database-setup)
5. [Application Deployment](#application-deployment)
6. [Docker Deployment](#docker-deployment)
7. [Production Configuration](#production-configuration)
8. [Monitoring Setup](#monitoring-setup)
9. [Backup and Recovery](#backup-and-recovery)
10. [Troubleshooting](#troubleshooting)

## System Requirements

### Minimum Requirements
- **CPU**: 4 cores, 2.5GHz
- **RAM**: 8GB
- **Storage**: 100GB SSD
- **Network**: 1Gbps connection
- **OS**: Ubuntu 20.04+ / RHEL 8+ / CentOS 8+

### Recommended for Production
- **CPU**: 8 cores, 3.0GHz
- **RAM**: 16GB
- **Storage**: 500GB NVMe SSD
- **Network**: 10Gbps connection
- **Load Balancer**: HAProxy/NGINX
- **Monitoring**: Prometheus + Grafana

### Software Dependencies
```bash
# Core dependencies
Python 3.12+
Node.js 20+
PostgreSQL 14+
Redis 7.0+

# Optional (for enhanced features)
Elasticsearch 8.0+ (advanced search)
RabbitMQ 3.11+ (async processing)
Docker 24.0+ (containerized deployment)
```

## Pre-Deployment Checklist

### Infrastructure Preparation
- [ ] Server provisioned with adequate resources
- [ ] Network connectivity verified
- [ ] DNS records configured
- [ ] SSL certificates obtained
- [ ] Firewall rules configured
- [ ] Monitoring infrastructure ready

### Security Preparation
- [ ] Service accounts created
- [ ] API keys generated
- [ ] Database credentials secured
- [ ] JWT secrets generated
- [ ] Backup encryption keys prepared
- [ ] Security scanning completed

### Data Migration Preparation
- [ ] Existing MISP data backed up
- [ ] Migration scripts tested
- [ ] Rollback procedures documented
- [ ] Data validation scripts prepared
- [ ] Performance benchmarks established

## Environment Configuration

### Environment Variables

Create `.env` file in the deployment directory:

```bash
# Database Configuration
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=misp_platform
POSTGRES_USER=misp_user
POSTGRES_PASSWORD=secure_password_here

# Redis Configuration
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=redis_password_here
REDIS_DB=0

# Application Configuration
API_BASE_URL=https://your-domain.com/api
UI_BASE_URL=https://your-domain.com
JWT_SECRET=your_jwt_secret_key_256_bits_minimum
API_KEY_SALT=your_api_key_salt_here

# MISP Compatibility
MISP_BASE_URL=https://your-domain.com/api/security/misp
MISP_API_VERSION=2.4.0
MISP_ADMIN_EMAIL=admin@your-domain.com

# Performance Configuration
WORKER_PROCESSES=4
MAX_CONNECTIONS=1000
CORRELATION_WORKERS=2
EXPORT_WORKERS=2

# Security Configuration
ENABLE_RATE_LIMITING=true
ENABLE_AUDIT_LOGGING=true
SESSION_TIMEOUT=3600
PASSWORD_MIN_LENGTH=12

# Feature Flags
ENABLE_ADVANCED_SEARCH=true
ENABLE_AUTO_CORRELATION=true
ENABLE_WEBHOOK_DELIVERY=true
ENABLE_DATA_ENCRYPTION=true

# Monitoring Configuration
ENABLE_METRICS=true
METRICS_PORT=9090
LOG_LEVEL=INFO
SENTRY_DSN=your_sentry_dsn_here

# Backup Configuration
BACKUP_ENABLED=true
BACKUP_S3_BUCKET=misp-backups
BACKUP_RETENTION_DAYS=90
```

### Configuration Validation

Run configuration validation:
```bash
python scripts/validate_config.py --env-file .env
```

Expected output:
```
✅ Database connectivity: OK
✅ Redis connectivity: OK
✅ JWT secret strength: OK
✅ API key salt configured: OK
✅ SSL certificates valid: OK
✅ Performance settings: OK
✅ Security settings: OK
Configuration validation passed!
```

## Database Setup

### PostgreSQL Installation

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install postgresql-14 postgresql-contrib
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

**RHEL/CentOS:**
```bash
sudo dnf install postgresql14-server postgresql14-contrib
sudo postgresql-14-setup initdb
sudo systemctl start postgresql-14
sudo systemctl enable postgresql-14
```

### Database Configuration

1. **Create Database and User:**
```sql
-- Connect as postgres user
sudo -u postgres psql

-- Create database
CREATE DATABASE misp_platform;

-- Create user
CREATE USER misp_user WITH PASSWORD 'secure_password_here';

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE misp_platform TO misp_user;
ALTER USER misp_user CREATEDB;

-- Enable required extensions
\c misp_platform
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";
CREATE EXTENSION IF NOT EXISTS "btree_gin";

-- Exit
\q
```

2. **Configure PostgreSQL:**

Edit `/etc/postgresql/14/main/postgresql.conf`:
```ini
# Performance settings
max_connections = 200
shared_buffers = 2GB
effective_cache_size = 6GB
work_mem = 64MB
maintenance_work_mem = 512MB

# Logging
log_statement = 'mod'
log_min_duration_statement = 1000
log_line_prefix = '%t [%p-%l] %q%u@%d '

# Checkpoint settings
checkpoint_completion_target = 0.9
wal_buffers = 32MB
```

Edit `/etc/postgresql/14/main/pg_hba.conf`:
```
# Local connections
local   misp_platform    misp_user                     md5
host    misp_platform    misp_user    127.0.0.1/32    md5
host    misp_platform    misp_user    ::1/128         md5
```

3. **Restart PostgreSQL:**
```bash
sudo systemctl restart postgresql
```

### Database Migration

1. **Run Initial Migrations:**
```bash
cd apps/jane-orchestrator
python manage.py migrate
```

2. **Load Initial Data:**
```bash
# Load MISP taxonomies
python manage.py load_taxonomies

# Load default organizations
python manage.py load_organizations

# Create admin user
python manage.py create_admin_user --email admin@your-domain.com
```

3. **Verify Migration:**
```bash
python manage.py check_migration_status
```

## Application Deployment

### Method 1: Direct Deployment

1. **Install Dependencies:**
```bash
# Backend dependencies
cd apps/jane-orchestrator
pip install -r requirements.txt

# Frontend dependencies
cd ../jane-ui
npm install
```

2. **Build Frontend:**
```bash
cd apps/jane-ui
npm run build
```

3. **Start Services:**

**Backend (Terminal 1):**
```bash
cd apps/jane-orchestrator
uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --workers 4
```

**Frontend (Terminal 2):**
```bash
cd apps/jane-ui
npm start
```

**Background Workers (Terminal 3):**
```bash
cd apps/jane-orchestrator
python src/workers/correlation_worker.py
```

### Method 2: System Service Deployment

1. **Create Systemd Services:**

**Backend Service** (`/etc/systemd/system/misp-orchestrator.service`):
```ini
[Unit]
Description=MISP Orchestrator Service
After=network.target postgresql.service redis.service

[Service]
Type=exec
User=misp
Group=misp
WorkingDirectory=/opt/misp-platform/apps/jane-orchestrator
Environment=PATH=/opt/misp-platform/venv/bin
EnvironmentFile=/opt/misp-platform/.env
ExecStart=/opt/misp-platform/venv/bin/uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --workers 4
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**Frontend Service** (`/etc/systemd/system/misp-ui.service`):
```ini
[Unit]
Description=MISP UI Service
After=network.target misp-orchestrator.service

[Service]
Type=exec
User=misp
Group=misp
WorkingDirectory=/opt/misp-platform/apps/jane-ui
Environment=NODE_ENV=production
EnvironmentFile=/opt/misp-platform/.env
ExecStart=/usr/bin/npm start
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

2. **Enable and Start Services:**
```bash
sudo systemctl daemon-reload
sudo systemctl enable misp-orchestrator misp-ui
sudo systemctl start misp-orchestrator misp-ui
```

3. **Verify Services:**
```bash
sudo systemctl status misp-orchestrator misp-ui
```

## Docker Deployment

### Docker Compose Configuration

Create `docker-compose.prod.yml`:

```yaml
version: '3.8'

services:
  # Database
  postgres:
    image: postgres:14-alpine
    container_name: misp-postgres
    environment:
      POSTGRES_DB: misp_platform
      POSTGRES_USER: misp_user
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql
    networks:
      - misp-network
    restart: unless-stopped
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U misp_user -d misp_platform"]
      interval: 30s
      timeout: 10s
      retries: 3

  # Redis
  redis:
    image: redis:7-alpine
    container_name: misp-redis
    command: redis-server --requirepass ${REDIS_PASSWORD}
    volumes:
      - redis_data:/data
    networks:
      - misp-network
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 30s
      timeout: 10s
      retries: 3

  # Backend Orchestrator
  orchestrator:
    build:
      context: ./apps/jane-orchestrator
      dockerfile: Dockerfile.prod
    container_name: misp-orchestrator
    environment:
      - POSTGRES_HOST=postgres
      - REDIS_HOST=redis
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
      - REDIS_PASSWORD=${REDIS_PASSWORD}
      - JWT_SECRET=${JWT_SECRET}
    volumes:
      - ./logs:/app/logs
      - ./data:/app/data
    ports:
      - "8000:8000"
    networks:
      - misp-network
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  # Frontend UI
  ui:
    build:
      context: ./apps/jane-ui
      dockerfile: Dockerfile.prod
    container_name: misp-ui
    environment:
      - NEXT_PUBLIC_API_URL=http://orchestrator:8000
    ports:
      - "3000:3000"
    networks:
      - misp-network
    depends_on:
      orchestrator:
        condition: service_healthy
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  # Background Workers
  workers:
    build:
      context: ./apps/jane-orchestrator
      dockerfile: Dockerfile.worker
    container_name: misp-workers
    environment:
      - POSTGRES_HOST=postgres
      - REDIS_HOST=redis
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
      - REDIS_PASSWORD=${REDIS_PASSWORD}
    volumes:
      - ./logs:/app/logs
    networks:
      - misp-network
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    restart: unless-stopped

  # NGINX Reverse Proxy
  nginx:
    image: nginx:alpine
    container_name: misp-nginx
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    ports:
      - "80:80"
      - "443:443"
    networks:
      - misp-network
    depends_on:
      - orchestrator
      - ui
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "wget", "--quiet", "--tries=1", "--spider", "http://localhost/health"]
      interval: 30s
      timeout: 10s
      retries: 3

networks:
  misp-network:
    driver: bridge

volumes:
  postgres_data:
    driver: local
  redis_data:
    driver: local
```

### NGINX Configuration

Create `nginx.conf`:

```nginx
events {
    worker_connections 1024;
}

http {
    upstream orchestrator {
        server orchestrator:8000;
    }

    upstream ui {
        server ui:3000;
    }

    # Rate limiting
    limit_req_zone $binary_remote_addr zone=api:10m rate=100r/m;
    limit_req_zone $binary_remote_addr zone=auth:10m rate=5r/m;

    server {
        listen 80;
        server_name your-domain.com;
        return 301 https://$server_name$request_uri;
    }

    server {
        listen 443 ssl http2;
        server_name your-domain.com;

        ssl_certificate /etc/nginx/ssl/cert.pem;
        ssl_certificate_key /etc/nginx/ssl/key.pem;
        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_ciphers ECDHE-RSA-AES256-GCM-SHA384:ECDHE-RSA-AES128-GCM-SHA256;

        # Security headers
        add_header X-Frame-Options DENY;
        add_header X-Content-Type-Options nosniff;
        add_header X-XSS-Protection "1; mode=block";
        add_header Strict-Transport-Security "max-age=31536000";

        # API routes
        location /api/ {
            limit_req zone=api burst=20 nodelay;
            proxy_pass http://orchestrator;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        # Auth routes (stricter rate limiting)
        location /api/auth/ {
            limit_req zone=auth burst=5 nodelay;
            proxy_pass http://orchestrator;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        # UI routes
        location / {
            proxy_pass http://ui;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        # Health check
        location /health {
            access_log off;
            return 200 "healthy\n";
            add_header Content-Type text/plain;
        }
    }
}
```

### Deployment Commands

1. **Deploy Application:**
```bash
# Create environment file
cp .env.example .env
# Edit .env with production values

# Deploy with Docker Compose
docker-compose -f docker-compose.prod.yml up -d

# Check service health
docker-compose -f docker-compose.prod.yml ps
```

2. **Initialize Database:**
```bash
# Run migrations
docker-compose -f docker-compose.prod.yml exec orchestrator python manage.py migrate

# Load initial data
docker-compose -f docker-compose.prod.yml exec orchestrator python manage.py load_taxonomies
```

3. **Verify Deployment:**
```bash
# Check logs
docker-compose -f docker-compose.prod.yml logs -f

# Test endpoints
curl https://your-domain.com/health
curl https://your-domain.com/api/health
```

## Production Configuration

### Performance Tuning

1. **Database Optimization:**
```sql
-- Create indexes for MISP queries
CREATE INDEX CONCURRENTLY idx_events_timestamp ON events(timestamp);
CREATE INDEX CONCURRENTLY idx_attributes_value ON attributes USING gin(value gin_trgm_ops);
CREATE INDEX CONCURRENTLY idx_correlations_composite ON correlations(source_attribute_id, target_attribute_id);

-- Analyze tables
ANALYZE events;
ANALYZE attributes;
ANALYZE correlations;
```

2. **Application Tuning:**
```python
# apps/jane-orchestrator/src/config/production.py
import os

# Database pool settings
DATABASE_POOL_SIZE = 20
DATABASE_MAX_OVERFLOW = 30
DATABASE_POOL_TIMEOUT = 30

# Redis connection pool
REDIS_POOL_SIZE = 50
REDIS_RETRY_ON_TIMEOUT = True

# Correlation processing
CORRELATION_BATCH_SIZE = 1000
CORRELATION_TIMEOUT = 300

# Caching settings
CACHE_DEFAULT_TIMEOUT = 3600
CACHE_LONG_TIMEOUT = 86400
```

3. **NGINX Caching:**
```nginx
# Add to nginx.conf
proxy_cache_path /var/cache/nginx levels=1:2 keys_zone=api_cache:10m max_size=1g inactive=60m;

location /api/static/ {
    proxy_cache api_cache;
    proxy_cache_valid 200 1h;
    proxy_cache_valid 404 1m;
    proxy_pass http://orchestrator;
}
```

### Security Hardening

1. **Firewall Configuration:**
```bash
# UFW rules
sudo ufw allow 22/tcp      # SSH
sudo ufw allow 80/tcp      # HTTP
sudo ufw allow 443/tcp     # HTTPS
sudo ufw deny 8000/tcp     # Block direct API access
sudo ufw deny 3000/tcp     # Block direct UI access
sudo ufw enable
```

2. **SSL/TLS Configuration:**
```bash
# Generate strong DH parameters
openssl dhparam -out /etc/nginx/ssl/dhparam.pem 4096

# Update nginx.conf
ssl_dhparam /etc/nginx/ssl/dhparam.pem;
ssl_session_cache shared:SSL:10m;
ssl_session_timeout 10m;
```

3. **Application Security:**
```python
# Enhanced security settings
SECURE_HEADERS = {
    'X-Frame-Options': 'DENY',
    'X-Content-Type-Options': 'nosniff',
    'X-XSS-Protection': '1; mode=block',
    'Referrer-Policy': 'strict-origin-when-cross-origin',
    'Content-Security-Policy': "default-src 'self'; script-src 'self' 'unsafe-inline'"
}

# API rate limiting
RATE_LIMITS = {
    'default': '100/minute',
    'auth': '5/minute',
    'admin': '10/minute'
}
```

## Monitoring Setup

### Health Checks

Create `scripts/health_check.py`:
```python
#!/usr/bin/env python3
import requests
import sys
import json

def check_health():
    endpoints = [
        'https://your-domain.com/health',
        'https://your-domain.com/api/health',
        'https://your-domain.com/api/security/misp/health'
    ]
    
    for endpoint in endpoints:
        try:
            response = requests.get(endpoint, timeout=10)
            if response.status_code == 200:
                print(f"✅ {endpoint}: OK")
            else:
                print(f"❌ {endpoint}: HTTP {response.status_code}")
                sys.exit(1)
        except Exception as e:
            print(f"❌ {endpoint}: {str(e)}")
            sys.exit(1)
    
    print("All health checks passed!")

if __name__ == "__main__":
    check_health()
```

### Monitoring Configuration

1. **Prometheus Metrics:**
```yaml
# prometheus.yml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'misp-orchestrator'
    static_configs:
      - targets: ['localhost:8000']
    metrics_path: '/metrics'
    scrape_interval: 10s

  - job_name: 'nginx'
    static_configs:
      - targets: ['localhost:9113']
```

2. **Grafana Dashboard:**
```json
{
  "dashboard": {
    "title": "MISP Platform Monitoring",
    "panels": [
      {
        "title": "Request Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(http_requests_total[5m])",
            "legendFormat": "{{method}} {{endpoint}}"
          }
        ]
      },
      {
        "title": "Response Time",
        "type": "graph",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))",
            "legendFormat": "95th percentile"
          }
        ]
      }
    ]
  }
}
```

### Log Management

1. **Centralized Logging:**
```yaml
# docker-compose.prod.yml (add to services)
  logspout:
    image: gliderlabs/logspout
    command: syslog://logs.your-domain.com:514
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
```

2. **Log Rotation:**
```bash
# /etc/logrotate.d/misp
/opt/misp-platform/logs/*.log {
  daily
  missingok
  rotate 30
  compress
  delaycompress
  notifempty
  copytruncate
}
```

## Backup and Recovery

### Database Backup

1. **Automated Backup Script:**
```bash
#!/bin/bash
# scripts/backup_database.sh

BACKUP_DIR="/opt/backups/misp"
DATE=$(date +%Y%m%d_%H%M%S)
DB_NAME="misp_platform"

# Create backup
pg_dump -h localhost -U misp_user -d $DB_NAME | gzip > "$BACKUP_DIR/misp_db_$DATE.sql.gz"

# Upload to S3 (optional)
aws s3 cp "$BACKUP_DIR/misp_db_$DATE.sql.gz" s3://misp-backups/database/

# Cleanup old backups (keep 30 days)
find $BACKUP_DIR -name "misp_db_*.sql.gz" -mtime +30 -delete

echo "Backup completed: misp_db_$DATE.sql.gz"
```

2. **Cron Schedule:**
```bash
# Daily backups at 2 AM
0 2 * * * /opt/misp-platform/scripts/backup_database.sh
```

### Application Data Backup

```bash
#!/bin/bash
# scripts/backup_application.sh

BACKUP_DIR="/opt/backups/misp"
DATE=$(date +%Y%m%d_%H%M%S)

# Backup configuration
tar -czf "$BACKUP_DIR/config_$DATE.tar.gz" /opt/misp-platform/.env /opt/misp-platform/nginx.conf

# Backup logs
tar -czf "$BACKUP_DIR/logs_$DATE.tar.gz" /opt/misp-platform/logs/

# Backup uploaded files
tar -czf "$BACKUP_DIR/uploads_$DATE.tar.gz" /opt/misp-platform/data/uploads/

echo "Application backup completed: $DATE"
```

### Recovery Procedures

1. **Database Recovery:**
```bash
# Stop services
sudo systemctl stop misp-orchestrator misp-ui

# Restore database
gunzip -c misp_db_20251031_020000.sql.gz | psql -h localhost -U misp_user -d misp_platform

# Start services
sudo systemctl start misp-orchestrator misp-ui
```

2. **Full System Recovery:**
```bash
# Restore configuration
tar -xzf config_20251031_020000.tar.gz -C /

# Restore application data
tar -xzf uploads_20251031_020000.tar.gz -C /

# Run migration check
cd /opt/misp-platform/apps/jane-orchestrator
python manage.py check_migration_status

# Restart all services
sudo systemctl restart misp-orchestrator misp-ui nginx
```

## Troubleshooting

### Common Issues

1. **Database Connection Issues:**
```bash
# Check PostgreSQL status
sudo systemctl status postgresql

# Test connection
psql -h localhost -U misp_user -d misp_platform -c "SELECT version();"

# Check logs
sudo tail -f /var/log/postgresql/postgresql-14-main.log
```

2. **Performance Issues:**
```bash
# Check resource usage
htop
iotop
free -h
df -h

# Check database performance
sudo -u postgres psql -d misp_platform -c "
SELECT query, calls, total_time, mean_time
FROM pg_stat_statements
ORDER BY total_time DESC
LIMIT 10;"
```

3. **API Response Issues:**
```bash
# Test API endpoints
curl -H "Authorization: Bearer <token>" https://your-domain.com/api/health

# Check application logs
docker-compose logs -f orchestrator

# Monitor response times
curl -w "@curl-format.txt" -o /dev/null -s https://your-domain.com/api/events
```

### Debug Mode

Enable debug mode for troubleshooting:
```bash
# Set environment variable
export DEBUG=true
export LOG_LEVEL=DEBUG

# Restart services
sudo systemctl restart misp-orchestrator
```

### Support Contacts

- **Technical Issues**: technical-support@your-domain.com
- **Security Issues**: security@your-domain.com
- **Emergency**: +1-XXX-XXX-XXXX

---

**Deployment Guide Version**: 1.0.0  
**Last Updated**: 2025-10-31  
**Next Review**: 2025-12-31