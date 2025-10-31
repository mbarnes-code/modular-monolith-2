# Phase 8 MISP Asset Relocation - T1591h Multi-Build Architectures Analysis

**Task**: T1591h - Document specialized build targets, platform-specific entry points, and deployment configurations

**Analysis Date**: 2025-01-25
**Source**: MISP threat intelligence platform deployment architecture analysis

## Executive Summary

MISP supports multiple deployment architectures and build targets across different operating systems, web servers, databases, and containerization platforms. This multi-platform support requires careful preservation of platform-specific configurations and deployment patterns during migration to the modular monolith architecture.

## 1. Platform Support Matrix

### 1.1 Operating System Support
```yaml
Primary Platforms:
  Ubuntu LTS:
    - Ubuntu 24.04 LTS (Primary support)
    - Ubuntu 22.04 LTS (Maintained)
    - Ubuntu 20.04 LTS (Legacy support)
    Install Scripts: INSTALL.ubuntu2404.sh, UPGRADE.ubuntu2404.sh

  Debian:
    - Debian 12 (Bookworm) - Current stable
    - Debian 13 (Trixie) - Testing
    Install Scripts: INSTALL.debian12.sh, INSTALL.debian13.sh

  RHEL/CentOS:
    - RHEL 9.4
    - CentOS Stream 9
    - Rocky Linux 9
    Install Scripts: xINSTALL.rhel94.sh

Legacy Platform Support:
  Discontinued but Configuration Available:
    - Ubuntu 14.04, 16.04 (archived configurations)
    - Debian 7, 8 (archived configurations)
    - CentOS 6, 7 (archived configurations)
    - FreeBSD (experimental configuration)

Platform-Specific Requirements:
  Package Managers:
    - APT (Debian/Ubuntu): apt-get based installation
    - YUM/DNF (RHEL/CentOS): rpm based installation
    - PKG (FreeBSD): pkg based installation
  
  System Services:
    - Systemd (Modern Linux): systemctl service management
    - Init.d (Legacy Linux): service command compatibility
    - Supervisor: Process management option
```

### 1.2 Web Server Architectures
```yaml
Apache HTTP Server:
  Versions Supported:
    - Apache 2.4 (Primary) - apache.24.misp.ssl
    - Apache 2.2 (Legacy) - apache.22.misp.ssl
  
  Configuration Variants:
    SSL/TLS Configurations:
      - SSL with Let's Encrypt integration
      - Self-signed certificate setup
      - Corporate PKI certificate deployment
      - Client certificate authentication
    
    Platform-Specific Configs:
      - Ubuntu/Debian: apache.misp.ubuntu
      - CentOS 7: apache.misp.centos7, apache.misp.centos7.ssl
      - CentOS 6: apache.misp.centos6 (legacy)

Nginx Support:
  Configuration: Ansible deployment with Nginx
  Features:
    - SSL/TLS termination
    - Load balancing capability
    - Static asset serving optimization
    - Security headers and rate limiting
  
  Deployment: /INSTALL/ansible/ directory
  Target: /etc/nginx/sites-available/misp configuration

Web Server Selection Factors:
  Performance: Nginx for high-traffic installations
  Compatibility: Apache for broad platform support
  Features: Apache for advanced authentication modules
  Container: Both supported in containerized deployments
```

## 2. Database Architecture Support

### 2.1 Database Engine Options
```yaml
MySQL/MariaDB (Primary):
  MySQL Versions:
    - MySQL 8.0 (Recommended)
    - MySQL 5.7 (Minimum supported)
  
  MariaDB Versions:
    - MariaDB 10.6+ (Recommended)
    - MariaDB 10.3+ (Minimum supported)
  
  Configuration Files:
    - MYSQL.sql: Database schema and initial data
    - Setup scripts integrated in platform installers
  
  Storage Engines:
    - InnoDB: Primary storage engine (required for FK constraints)
    - MyISAM: Legacy support only

PostgreSQL Support:
  Status: Secondary/Experimental support
  Configuration Files:
    - POSTGRESQL-structure.sql: Database schema
    - POSTGRESQL-data-initial.sql: Initial data
  
  Versions Supported:
    - PostgreSQL 12+
    - PostGIS extensions for geospatial data
  
  Installation Scripts:
    - xINSTALL.debian8-postgresql.txt (experimental)
    - Platform-specific PostgreSQL setup

Database Selection Criteria:
  MySQL/MariaDB: Production deployments, broad compatibility
  PostgreSQL: Advanced features, better performance for complex queries
  SQLite: Development/testing only (not production supported)
```

## 3. Deployment Architecture Patterns

### 3.1 Monolithic Deployment (Traditional)
```yaml
Architecture: Single-server deployment
Components on Single Host:
  - Web server (Apache/Nginx)
  - PHP application server
  - Database (MySQL/MariaDB)
  - Redis cache/queue
  - Background workers
  - File storage

Target Environments:
  - Small to medium organizations
  - Development and testing
  - Proof of concept deployments
  - Air-gapped environments

Installation Approach:
  - Shell script automation
  - Package-based installation
  - Configuration management tools
  - Docker containerization

Resource Requirements:
  Minimum: 4GB RAM, 2 CPU cores, 50GB storage
  Recommended: 8GB RAM, 4 CPU cores, 200GB SSD
  Large Scale: 16GB+ RAM, 8+ CPU cores, 1TB+ storage
```

### 3.2 Distributed Deployment
```yaml
Multi-Server Architecture:
  Web Tier:
    - Load balancer (HAProxy, Nginx)
    - Multiple web server instances
    - Shared session storage (Redis)
  
  Application Tier:
    - PHP-FPM process pools
    - Background worker nodes
    - Queue processing servers
  
  Data Tier:
    - Database cluster (MySQL/MariaDB)
    - Redis cluster for caching
    - Shared file storage (NFS, S3)

High Availability Features:
  Database: Master-slave replication
  Web Servers: Load balancing with health checks
  Cache: Redis Sentinel or Cluster mode
  Storage: Distributed file systems

Scaling Patterns:
  Horizontal: Add more web/worker nodes
  Vertical: Increase resources per node
  Database: Read replicas and partitioning
  Cache: Redis cluster expansion
```

### 3.3 Container Orchestration
```yaml
Docker Support:
  Container Strategy: Multi-container deployment
  Base Images: Official PHP, MySQL, Redis containers
  Orchestration: Docker Compose, Kubernetes

Kubernetes Deployment:
  Components:
    - MISP web application pods
    - MySQL/MariaDB database pods
    - Redis cache/queue pods
    - Background worker pods
  
  Services:
    - LoadBalancer for web traffic
    - ClusterIP for internal communication
    - PersistentVolumes for data storage
  
  ConfigMaps and Secrets:
    - Database connection strings
    - API keys and certificates
    - Configuration overrides

Container Benefits:
  - Consistent deployment across environments
  - Resource isolation and management
  - Automated scaling and recovery
  - Development/production parity
```

## 4. Build System Architecture

### 4.1 Package Building
```yaml
Debian Package Building:
  Script: build-deb.sh
  Requirements:
    - CakePHP submodules initialized
    - dpkg-buildpackage toolchain
    - Debian packaging metadata
  
  Output: .deb package for APT repositories
  Target: Debian/Ubuntu distribution integration

Build Dependencies:
  Submodules: CakePHP framework (git submodule)
  PHP Dependencies: Composer-managed packages
  JavaScript: npm-managed frontend assets
  System Libraries: PHP extensions and system tools

Package Contents:
  - Application code and configuration
  - Web server configuration templates
  - Systemd service files
  - Database schema and migration scripts
  - Documentation and examples
```

### 4.2 Configuration Management
```yaml
Ansible Automation:
  Playbook: misp.yml
  Target: Nginx-based deployment
  Features:
    - Automated installation and configuration
    - SSL certificate generation
    - Database setup and initialization
    - Backup script deployment

Configuration Templates:
  Platform-Specific:
    - Apache virtual host configurations
    - Nginx server blocks
    - PHP-FPM pool configurations
    - Systemd service definitions
  
  Feature-Specific:
    - SSL/TLS configurations
    - SMTP relay settings
    - S3 attachment storage
    - SMIME encryption
    - Elasticsearch logging

Environment Variables:
  Database Connection:
    - DBHOST, DBPORT, DBNAME
    - DBUSER_MISP, DBPASSWORD_MISP
  
  Application Settings:
    - MISP_DOMAIN, MISP_PATH
    - Upload limits and timeouts
    - GPG key configuration
  
  Service Integration:
    - Redis connection parameters
    - SMTP server configuration
    - External API endpoints
```

## 5. Service Management Architecture

### 5.1 Background Workers
```yaml
Worker Management:
  Primary: Systemd service (misp-workers.service)
  Alternative: Supervisor process management
  Legacy: Manual script execution

Service Configuration:
  Unit File: misp-workers.service
  User/Group: www-data
  Working Directory: /var/www/MISP
  Start Command: /var/www/MISP/app/Console/worker/start.sh
  Stop Command: CakeResque stop --all

Worker Types:
  1. Default Queue Workers:
     - Event correlation processing
     - Import/export operations
     - Email notifications
     - Synchronization tasks
  
  2. Specialized Workers:
     - Enrichment processing
     - Large dataset operations
     - Real-time correlation
     - Feed processing

Process Management:
  Restart Policy: on-failure
  Kill Mode: none (graceful shutdown)
  Dependencies: network, httpd service
  Multi-user target integration
```

### 5.2 Caching and Queue Architecture
```yaml
Redis Configuration:
  Default Settings:
    - Host: 127.0.0.1
    - Port: 6379
    - Database: 0 (default)
    - Namespace: 'resque'
  
  Use Cases:
    - Session storage
    - Application caching
    - Background job queues
    - Real-time data storage

CakeResque Configuration:
  Queue Management:
    - Default queue name: 'default'
    - Worker polling interval: 5 seconds
    - Worker count: configurable
    - Job status tracking
  
  Logging:
    - Worker error logs
    - Verbose mode support
    - Performance monitoring
    - Failure tracking
```

## 6. Security Architecture Variants

### 6.1 SSL/TLS Configurations
```yaml
SSL Certificate Options:
  1. Self-Signed Certificates:
     - Development and testing
     - Air-gapped environments
     - Proof of concept deployments
  
  2. Let's Encrypt Integration:
     - Automated certificate generation
     - Automatic renewal
     - DNS-based validation
  
  3. Corporate PKI:
     - Enterprise certificate authorities
     - Client certificate authentication
     - Certificate chain validation

SSL Configuration Profiles:
  Intermediate Security:
    - TLS 1.2/1.3 only
    - Strong cipher suites
    - HSTS headers
    - Perfect Forward Secrecy
  
  High Security:
    - Client certificate verification
    - Certificate pinning
    - Advanced cipher configuration
    - Security header enforcement
```

### 6.2 Authentication Architectures
```yaml
Authentication Methods:
  1. Local Authentication:
     - Database-stored user accounts
     - Password hashing (bcrypt)
     - Session management
     - Two-factor authentication
  
  2. LDAP/Active Directory:
     - Corporate directory integration
     - Group-based authorization
     - Single sign-on (SSO)
     - Automatic user provisioning
  
  3. SAML Integration:
     - Identity provider integration
     - Federated authentication
     - Attribute mapping
     - Session lifetime management
  
  4. OAuth 2.0/OpenID Connect:
     - Third-party identity providers
     - API authentication
     - Token-based access
     - Refresh token handling

Authorization Models:
  - Role-based access control (RBAC)
  - Organization-based permissions
  - Event-level distribution controls
  - API key management
```

## 7. Integration Architecture Patterns

### 7.1 External Service Integration
```yaml
MISP Federation:
  Synchronization Patterns:
    - Pull synchronization (fetch remote events)
    - Push synchronization (share local events)
    - Bidirectional synchronization
    - Filtered synchronization
  
  Authentication:
    - Certificate-based mutual authentication
    - API key authentication
    - Organization trust relationships
    - Distribution level enforcement

TAXII Server Integration:
  Standards Compliance:
    - TAXII 1.1 protocol support
    - TAXII 2.0/2.1 compatibility
    - STIX format conversion
    - Collection management
  
  Deployment Options:
    - Integrated TAXII server
    - External TAXII service
    - Proxy configuration
    - Load balancing

Enrichment Services:
  Architecture: Microservice-based
  Communication: HTTP REST APIs
  Service Discovery: Configuration-based
  Timeout Handling: Configurable timeouts
```

## 8. Migration Complexity Analysis

### 8.1 Platform Migration Challenges
```yaml
Multi-Platform Support Preservation:
  Challenge Level: HIGH
  Complexity Factors:
    - Platform-specific installation scripts
    - Web server configuration variations
    - Database engine differences
    - Service management variations
  
  Critical Requirements:
    - Maintain platform compatibility
    - Preserve configuration options
    - Support deployment patterns
    - Ensure feature parity

Build System Modernization:
  Current: Shell script-based installation
  Target: Container-native with traditional support
  Challenge: Configuration template migration
  Risk: Platform-specific feature loss
```

### 8.2 Deployment Pattern Evolution
```yaml
Traditional → Modern Deployment:
  Monolithic:
    Current: Single-server shell script installation
    Target: Containerized single-instance deployment
    Preservation: Configuration templates and scripts
  
  Distributed:
    Current: Manual multi-server setup
    Target: Kubernetes-native distributed deployment
    Preservation: Service separation and communication patterns
  
  Hybrid:
    Current: Mixed deployment approaches
    Target: Flexible deployment options (containers + traditional)
    Preservation: All existing deployment methods
```

## 9. Technology Stack Mapping

### 9.1 Platform Architecture Translation
```yaml
Current Architecture → Target Architecture:

Operating System Support:
  Current: Platform-specific installation scripts
  Target: Container-first with host installation options
  Strategy: Maintain platform scripts, add container support

Web Server Integration:
  Current: Apache/Nginx configuration templates
  Target: Reverse proxy with FastAPI backend
  Strategy: Preserve web server options, add API gateway

Database Architecture:
  Current: MySQL/MariaDB with PostgreSQL support
  Target: PostgreSQL primary with MySQL compatibility
  Strategy: Database-agnostic data layer with migration tools

Service Management:
  Current: Systemd/Supervisor worker management
  Target: Modern orchestration (Docker, Kubernetes)
  Strategy: Support both traditional and container orchestration
```

## 10. Recommended Migration Strategy

### 10.1 Platform Preservation Strategy
```yaml
Phase 1: Container Foundation (Months 1-3)
  Objectives:
    - Containerize existing MISP deployment
    - Preserve all platform configurations
    - Maintain installation script compatibility
    - Test deployment patterns

  Deliverables:
    - Docker containers for all components
    - Kubernetes deployment manifests
    - Platform compatibility validation
    - Migration documentation

Phase 2: Service Modernization (Months 4-6)
  Objectives:
    - Modernize background workers
    - Implement service discovery
    - Enhance monitoring and logging
    - Optimize resource utilization

  Deliverables:
    - Modern worker orchestration
    - Service mesh integration
    - Monitoring dashboards
    - Performance optimization

Phase 3: Deployment Flexibility (Months 7-9)
  Objectives:
    - Support multiple deployment patterns
    - Maintain backward compatibility
    - Implement deployment automation
    - Provide migration tools

  Deliverables:
    - Flexible deployment options
    - Automated migration tools
    - Platform compatibility matrix
    - Deployment validation tests
```

### 10.2 Configuration Management Evolution
```yaml
Configuration Strategy:
  Current: File-based configuration with database settings
  Target: Modern configuration management (12-factor app)
  Approach: Gradual migration with compatibility layer

Environment Management:
  Development: Container-based with volume mounts
  Testing: Kubernetes staging environment
  Production: Flexible deployment (containers or traditional)

Secret Management:
  Current: File-based and database-stored secrets
  Target: External secret management (Vault, Kubernetes secrets)
  Migration: Gradual secret externalization with fallback support
```

## 11. Performance and Scalability Considerations

### 11.1 Deployment-Specific Optimizations
```yaml
Single-Server Optimization:
  - Resource allocation optimization
  - Local caching strategies
  - Database tuning for single instance
  - Background worker coordination

Multi-Server Optimization:
  - Load balancing configuration
  - Session affinity management
  - Distributed caching strategies
  - Database replication setup

Container Optimization:
  - Resource limits and requests
  - Pod autoscaling configuration
  - Network policy enforcement
  - Storage optimization

Cloud-Native Features:
  - Horizontal pod autoscaling
  - Persistent volume management
  - Service mesh integration
  - Observability stack integration
```

## Conclusion

MISP's multi-build architecture supports diverse deployment patterns across multiple platforms, web servers, and databases. The migration to a modular monolith must preserve this deployment flexibility while modernizing the underlying architecture. The strategy emphasizes maintaining backward compatibility with existing deployment methods while introducing modern container-native options.

Key preservation requirements include platform-specific installation scripts, web server configurations, database options, and service management patterns. The phased migration approach ensures continuity of all deployment options while gradually introducing modern orchestration capabilities.

**Next Phase**: Additional MISP analysis tasks or Phase 8 completion review.