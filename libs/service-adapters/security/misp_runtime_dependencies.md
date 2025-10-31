# MISP Runtime Dependencies Analysis

## System Packages Required

### Core System Dependencies
- **Apache2** - Web server for HTTP/HTTPS serving
- **MariaDB/MySQL** - Primary data storage for threat intelligence
- **Redis** - Caching and session management
- **PHP 8.3** - Server-side runtime environment
- **Python 3.x** - Background processing and worker tasks
- **Supervisor** - Process monitoring and worker management

### Essential System Binaries
- **`/usr/local/bin/composer`** - PHP dependency management
- **`/usr/bin/gpg`** - GPG binary for encryption/signing operations
- **`curl`** - HTTP client for external API integrations
- **`git`** - Version control for updates and modules
- **`zip/unzip`** - Archive handling for data exchange
- **`openssl`** - SSL/TLS certificate management
- **`gcc`** - C compiler for PECL extensions

### PHP Extensions (System-Level)
- **Core Extensions**: xml, mysql, opcache, readline, mbstring, zip, intl, bcmath, gd, curl
- **Caching**: redis, apcu
- **Security**: gnupg
- **Performance**: brotli, simdjson, zstd (PECL extensions)

### Python System Dependencies
- **Virtual Environment**: `/var/www/MISP/venv/bin/python`
- **System Python Packages**: python3-pip, python3-virtualenv, python3-magic
- **Binary Dependencies**: Required for pydeep2, lief, python-magic

### External Service Dependencies
- **Redis Server**: `redis-server` service on port 6379
- **MySQL/MariaDB**: Database service on port 3306
- **Apache2**: Web service on ports 80/443
- **Supervisor**: Worker process management

## File System Requirements

### Directory Structure
```
/var/www/MISP/                # Main application directory
├── app/                      # CakePHP application code
├── venv/                     # Python virtual environment
├── files/                    # Uploaded attachments storage
└── logs/                     # Application logs
```

### File Permissions
- **Apache User**: `www-data` (Ubuntu/Debian) or `apache` (CentOS/RHEL)
- **Directory Permissions**: 755 for directories, 644 for files
- **Writable Directories**: files/, logs/, tmp/

### Configuration Files
- **Apache**: `/etc/apache2/sites-available/misp.conf`
- **PHP**: `/etc/php/8.3/apache2/php.ini`
- **MySQL**: `/etc/mysql/mariadb.conf.d/50-server.cnf`
- **Supervisor**: `/etc/supervisor/conf.d/misp-workers.conf`

## Network Requirements

### Outbound Connections
- **HTTPS (443)** - For threat feed updates and external API calls
- **HTTP (80)** - For non-secure external integrations
- **DNS (53)** - For domain resolution

### Inbound Services
- **HTTP (80)** - Web interface access
- **HTTPS (443)** - Secure web interface access
- **MySQL (3306)** - Database access (if remote)
- **Redis (6379)** - Cache access (if remote)

## Migration Strategy for Modular Monolith

### Service Adaptation
1. **Database**: Migrate from MySQL to PostgreSQL unified schema
2. **Web Server**: Replace Apache with FastAPI built-in server
3. **PHP Runtime**: Migrate business logic to Python FastAPI
4. **File Storage**: Integrate with unified file management system
5. **Background Workers**: Integrate with FastAPI background tasks

### Dependency Resolution
1. **System Packages**: Document in main `requirements.txt` and `Dockerfile`
2. **Binary Dependencies**: Handle via Docker container or system package manager
3. **External Services**: Integrate with existing Redis and PostgreSQL services
4. **File Permissions**: Handle via containerized deployment with proper user mapping

### Preservation Requirements
- **GPG Functionality**: Maintain encryption/signing capabilities
- **File Upload/Download**: Preserve attachment handling
- **Background Processing**: Maintain worker task functionality
- **External API Integration**: Preserve threat feed connectivity
- **Database Performance**: Maintain indexing and query optimization patterns

## Implementation Notes

### Critical System Dependencies to Preserve
1. **GPG Binary**: Required for threat intelligence signing/verification
2. **Python Virtual Environment**: Required for background processing
3. **File System Access**: Required for attachment storage and processing
4. **Network Access**: Required for threat feed updates and API integrations

### Migration Approach
- **Containerization**: Package system dependencies in Docker containers
- **Service Abstraction**: Create service layer for external dependency access
- **Configuration Management**: Centralize configuration through unified config system
- **Testing Strategy**: Validate all system dependencies work in new environment

This analysis supports T1935f completion by documenting all runtime dependencies that must be handled during MISP integration into the modular monolith architecture.