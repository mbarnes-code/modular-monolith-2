# Security Domain Services

This directory contains all security-focused services within the Mental Prosthetic Platform, including penetration testing tools, incident management, and forensic analysis capabilities.

## Performance Target
- **Response Time**: <1s (Security domain critical operations)

## Services

### Incident Management & Forensics
- **dispatch-service** - Netflix's incident management and orchestration platform
- **ghostwriter-service** - Red team operation management and reporting
- **nemesis-service** - Offensive file enrichment pipeline (main service)
- **nemesis-web-api** - Nemesis web API interface
- **nemesis-frontend** - Nemesis web interface
- **nemesis-file-enrichment** - File processing and enrichment service
- **nemesis-document-conversion** - Document conversion and analysis

### Penetration Testing Tools
- **blackarch-service** - BlackArch Linux repository API (4,599+ security tools)
- **blackarch-service-e2e** - End-to-end tests for BlackArch service
- **cyberchef-service** - "The Cyber Swiss Army Knife" - data manipulation and analysis
- **apiscout-service** - Windows API usage analysis
- **brute-ratel-service** - Command and control framework
- **hexstrike-service** - Binary analysis and exploitation
- **meterpreter-service** - Advanced payload generation and management
- **software-forensic-kit-service** - Digital forensics toolkit

### Network Security & Analysis
- **helk-service** - Hunting ELK stack for threat detection
- **maltrail-service** - Malicious traffic detection system
- **misp-service** - Malware information sharing platform
- **yara-x-service** - Advanced malware detection and classification

### Infrastructure & Remote Access
- **kasmvnc-service** - Container-based VNC/desktop streaming
- **security-service** - Core security service aggregator

## Architecture Patterns

### Service Categories

**Data Processing Pipeline**
- Nemesis services (document → file enrichment → analysis)
- BlackArch repository (package metadata processing)

**Analysis & Detection**
- HELK, Maltrail, MISP, YARA-X (threat intelligence)
- CyberChef, APIScout (data analysis)

**Management & Orchestration**
- Dispatch (incident management)
- Ghostwriter (operation management)

**Access & Infrastructure**
- KasmVNC (secure remote access)
- Meterpreter, Brute Ratel (C2 infrastructure)

### Integration Patterns

**Service Adapters**
All security services preserve 100% of original functionality through service adapter patterns, ensuring no loss of capabilities during platform integration.

**Authentication**
Unified authentication through jane-orchestrator with domain-specific authorization policies for security tools.

**Data Flow**
```
jane-ui → jane-orchestrator → security-service → [specific tools]
                            ↓
                        audit-logging
```

## Development

### Running Services

```bash
# Individual services
npx nx serve security/blackarch-service
npx nx serve security/cyberchef-service
npx nx serve security/nemesis-service

# All security services
npx nx run-many --target=serve --projects=tag:domain:security

# Testing
npx nx run-many --target=test --projects=tag:domain:security

# Building
npx nx run-many --target=build --projects=tag:domain:security
```

### Project Tags

All security services should include:
- `domain:security` - Security domain identifier
- `scope:backend` or `scope:frontend` - Service type
- `type:service` or `type:application` - Project type

### Performance Monitoring

Security services have strict performance requirements:
- Critical operations: <1s response time
- Tool queries: <2s response time
- Bulk operations: <5s response time

Monitor using:
```bash
# Performance validation
python tests/performance/security-domain-validation.py
```

## Security Considerations

### Isolation
Security tools run in isolated environments to prevent cross-contamination and ensure safe analysis of malicious samples.

### Access Control
- Role-based access control (RBAC)
- Tool-specific permissions
- Audit logging for all operations

### Data Handling
- Secure data sanitization
- Encrypted storage for sensitive analysis results
- Automatic cleanup of temporary files

## Service Dependencies

### External Dependencies
- Docker containers for isolated execution
- Database services for persistent storage
- Message queues for async processing

### Internal Dependencies
- `jane-orchestrator` - Central routing and authentication
- `libs/shared` - Common utilities and types
- `libs/service-adapters` - Integration layer

## Documentation

Each service maintains its own README.md with:
- Service-specific setup instructions
- API documentation
- Integration guides
- Troubleshooting information

## Contributing

When adding new security services:
1. Follow the service adapter pattern
2. Implement proper isolation and sandboxing
3. Add comprehensive security tests
4. Document security implications
5. Include performance benchmarks