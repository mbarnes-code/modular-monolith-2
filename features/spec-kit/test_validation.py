#!/usr/bin/env python3
"""
Test the validation system with sample content
"""

from pathlib import Path

from src.specify_cli.validators import AnalysisValidator, ValidationConfig


def test_validation_system():
    """Test validation with sample analysis content"""

    # Sample analysis content that should pass with the new system
    sample_content = '''# Project Analysis: Sample Security Tool

## TECHNICAL CONTENT GUIDANCE (Important for Validation)
This section demonstrates legitimate technical patterns vs placeholders.

## 1. System Overview & Business Context

### System Identity
- **System Name**: HexStrike Security Scanner
- **Primary Function**: Network vulnerability assessment and penetration testing automation
- **Technology Stack**: Python 3.11, FastAPI, PostgreSQL, Docker
- **Business Criticality**: IMPORTANT
- **Active Users**: ~500 security professionals
- **Business Owner**: Security Team Lead
- **Technical Owner**: DevOps Engineer

### Business Value & Purpose
- **Problem Solved**: Manual penetration testing is time-consuming and inconsistent across teams
- **Success Metrics**: 80% reduction in manual testing time, 95% vulnerability detection rate
- **Business Dependencies**: Security compliance audits, customer security assessments
- **Failure Impact**: Security assessments delayed, manual fallback increases testing time 3x

## 2. Technical Architecture

### System Architecture
```yaml
Architecture Pattern: Microservices
Deployment: Docker containers on AWS ECS
Database: PostgreSQL 14 + Redis 7 for caching
Key Technologies:
  - Backend: Python 3.11 + FastAPI 0.104
  - Security Engine: Custom vulnerability scanner
  - Infrastructure: Docker, AWS ECS, Application Load Balancer
  - Monitoring: CloudWatch, Sentry error tracking
```

### Core Components & Dependencies
**Internal Components**:
- **Scanner Engine** - Core vulnerability detection - Python + Nmap integration
- **Report Generator** - PDF/JSON reporting - WeasyPrint + Jinja2 templates

**External Dependencies**:
- **CVE Database API** - CVE-2024-1234 lookups - CRITICAL
- **Nmap Scanner** - Network port scanning - CRITICAL

**Database Schema Overview**:
- **Primary Models**: Scan, Vulnerability, Target, Report (12K records each)
- **Key Relationships**: Scan → Vulnerabilities, Target → Scans, Scan → Reports
- **Data Volume**: ~50GB scan results, 5M vulnerability records

## 3. Business Logic & Domain Rules

### Critical Business Logic
**Core Algorithms** (Must be preserved exactly):
1. **Vulnerability Scoring Algorithm** - CVSS calculation + custom risk factors
   - **Location**: src/scanner/scoring.py:calculate_risk_score()
   - **Complexity**: 150 lines, medium complexity with CVE database integration
   - **Business Impact**: Incorrect scoring leads to missed critical vulnerabilities

2. **Port Scan Optimization** - Adaptive scanning based on target response
   - **Location**: src/scanner/port_scanner.py:adaptive_scan()  
   - **Complexity**: 200 lines, high complexity with timing algorithms
   - **Business Impact**: Performance affects scan completion time and accuracy

### Domain-Specific Rules
**Security Rules** (Must be preserved):
- **Rule**: "Critical vulnerabilities (CVSS 9.0+) must trigger immediate alerting"
- **Rule**: "Scans against production networks require manager approval"  
- **Rule**: "Vulnerability data retention limited to 2 years per compliance requirements"
- **Rule**: "All scan activities must be logged with user attribution for audit trails"

### Workflow Logic
**Critical Security Workflows**:
- **Workflow**: Scan Request → [validation → approval → execution → reporting → alerting]
- **Workflow**: Vulnerability Detection → [scoring → classification → deduplication → notification]
- **Workflow**: Report Generation → [template selection → data aggregation → PDF export → distribution]

## 4. Current Performance & Operational Metrics

### Performance Baselines (MEASURED DATA)
**API Response Times**:
```yaml
Critical Endpoints:
  - GET /api/v1/scans: [Avg: 120ms, P95: 300ms, P99: 800ms]
  - POST /api/v1/scans/start: [Avg: 200ms, P95: 500ms, P99: 1200ms]  
  - GET /api/v1/reports/{id}: [Avg: 80ms, P95: 200ms, P99: 500ms]

Scanner Performance:
  - Most frequent scan: Port sweep (1000 hosts) - Avg: 180s
  - Slowest regular scan: Full vulnerability scan - Avg: 2400s
  - Largest target scan: Class C network (/24) - Duration: 3600s
```

**System Resource Usage**:
```yaml
Production Load (Peak Hours):
  - CPU Usage: 75% (scanning workloads spike to 95%)
  - Memory Usage: 12 GB / 16 GB total (scanning processes)
  - Database Connections: 45 active / 100 max
  - Disk Usage: 200 GB scan data, 50 GB application logs
  
Traffic Patterns:
  - Peak Daily Scans: 150 concurrent scans
  - Peak API Requests/min: 2000 requests
  - Data Transfer: 500 GB/day (large scan reports)
```

### Operational Health
**Current Issues**:
- **Issue**: Memory leaks in long-running scans - **Severity**: MEDIUM - **Frequency**: Weekly
- **Issue**: CVE database sync failures - **Severity**: HIGH - **Frequency**: Monthly

**Reliability Metrics** (Last 90 days):
- **Uptime**: 99.2%
- **Error Rate**: 2.1% of scan requests  
- **MTTR** (Mean Time to Recovery): 15 minutes
- **Incident Count**: 8 incidents total, 2 critical

## 5. Integration & Data Flow Architecture

### External System Integrations
**Upstream Dependencies** (Systems this system depends on):
```yaml
System 1: CVE Database API
  Purpose: Vulnerability definitions and CVSS scores
  Integration Type: REST API
  Data Flow: CVE-2024-1234 format vulnerability data
  Failure Impact: Cannot score vulnerabilities, scans incomplete
  SLA/Performance: 99.5% uptime, <500ms response time

System 2: Corporate LDAP
  Purpose: User authentication and authorization
  Integration Type: LDAP protocol
  Data Flow: User credentials and group memberships
  Failure Impact: Cannot authenticate users, manual approval required
  SLA/Performance: 99.9% uptime, <200ms authentication
```

**Downstream Dependencies** (Systems that depend on this system):
```yaml
System 1: SIEM Platform
  Purpose: Security event correlation and alerting
  Integration Type: Syslog + JSON webhook
  Data Flow: Vulnerability alerts and scan completion events
  Usage Pattern: Real-time alerting for critical findings
  Breaking Changes Impact: Security team loses automated vulnerability alerts

System 2: Compliance Dashboard
  Purpose: Regulatory compliance reporting
  Integration Type: REST API + scheduled exports
  Data Flow: Scan results, vulnerability counts, remediation status
  Usage Pattern: Daily compliance metrics, quarterly audit reports
  Breaking Changes Impact: Compliance reporting breaks, manual data collection required
```

### Data Flow Patterns
**Critical Data Synchronization**:
- **Flow**: CVE Database → HexStrike → SIEM Platform (vulnerability intelligence)
- **Flow**: Network Assets → HexStrike → Compliance Dashboard (security posture)

**Event-Driven Processes**:
- **Event**: Critical Vulnerability Detected → **Triggers**: SIEM alerts, security team notifications → **Data**: CVE details, affected systems, remediation steps
- **Event**: Scan Completion → **Triggers**: Report generation, dashboard updates → **Data**: Scan results, performance metrics, executive summary

## 12. Success Criteria & Acceptance Requirements

### Migration Success Definition
**Functional Requirements** (Must work exactly the same):
- [ ] **Vulnerability Scanning**: All CVE detection algorithms produce identical results
- [ ] **Performance Scanning**: Port scans complete within same time windows  
- [ ] **Report Generation**: PDF reports match existing format and content
- [ ] **API Compatibility**: All existing integrations continue working without changes
- [ ] **Security Compliance**: Audit logging maintains same detail level

**Performance Requirements**:
- [ ] **Scan Performance**: Network scans complete within ±10% of current baseline
- [ ] **API Response**: Critical endpoints maintain <200ms response times  
- [ ] **System Uptime**: Achieve 99.5% uptime target in first month post-migration

**Data Requirements**:
- [ ] **Historical Scans**: 2 years of scan history remains accessible
- [ ] **Vulnerability Database**: Complete CVE mapping preserved
- [ ] **Audit Logs**: Security event logs maintain chain of custody

### Technical Acceptance Criteria  
**Security Standards**:
- [ ] **Penetration Testing**: System passes external security assessment
- [ ] **Code Security**: SAST/DAST scans show no new high-severity findings
- [ ] **Access Controls**: Role-based permissions work identically
- [ ] **Audit Compliance**: Logging meets SOC 2 requirements

### Migration Validation Plan
**Security-Specific Testing**:
- [ ] **Vulnerability Detection**: Scan identical targets, verify result consistency
- [ ] **Performance Testing**: Load test with 100 concurrent scans
- [ ] **Integration Testing**: Verify SIEM and compliance dashboard data flows
- [ ] **Failover Testing**: Validate system behavior during CVE database outages

---

## Analysis Metadata

**Analysis Completed By**: Security Engineering Team Lead  
**Analysis Date**: 2024-11-02
**Analysis Confidence**: HIGH - Direct team involvement in system development
**Analysis Method**: Code Review + Performance Testing + Integration Analysis

**Stakeholders Consulted**:
- **Security**: Lead Security Engineer, 2 Penetration Testers
- **Technical**: DevOps Lead, Backend Developer
- **Business**: CISO, Compliance Manager

**Documentation Sources**:
- **Code Repository**: https://github.com/company/hexstrike-scanner
- **Architecture Docs**: Confluence security architecture space
- **Performance Data**: CloudWatch dashboards, Sentry metrics
'''

    print("Testing validation system...")

    # Test with default configuration
    config = ValidationConfig()
    validator = AnalysisValidator(config)

    print(f"Configuration:")
    print(f"  Level: {config.get_validation_level().value}")
    print(f"  Threshold: {config.get_quality_threshold()}")
    print(f"  Technical Patterns: {config.uses_technical_patterns()}")
    print(f"  N/A Allowed: {config.allows_na_responses()}")

    # Validate the sample content
    report = validator.validate_analysis_content(sample_content)

    print(f"\nValidation Results:")
    print(f"  Score: {report.score:.1f}/100")
    print(f"  Threshold Met: {report.threshold_met}")
    print(
        f"  Sections: {report.passed_sections}/{report.total_sections} passed")
    print(f"  Level: {report.level.value}")

    if report.issues:
        print(f"\nIssues ({len(report.issues)}):")
        for issue in report.issues[:10]:  # Show first 10
            print(
                f"  {issue.result_type.value.upper()}: {issue.section} - {issue.message}")
        if len(report.issues) > 10:
            print(f"  ... and {len(report.issues) - 10} more")

    # Test technical pattern recognition
    print(f"\nTesting Technical Pattern Recognition:")

    test_patterns = [
        # JSON - should be legitimate
        '{"status": "ok", "vulnerabilities": []}',
        '{6A 40 68 ?? ?? 00 00}',  # Hex pattern - should be legitimate
        'CVE-2024-1234',  # CVE reference - should be legitimate
        '/api/v1/scans/{id}',  # API endpoint - should be legitimate
        'src/scanner/scoring.py',  # File path - should be legitimate
        'N/A - CLI tool has no frontend',  # Explained N/A - should be legitimate
        '{template_var}',  # Template variable - should be placeholder
        '[TODO: Add details]',  # Bare TODO - should be placeholder
        # Contextual TODO - should be legitimate
        'TODO: investigate performance impact with benchmarking',
    ]

    for pattern in test_patterns:
        is_legit, reason = validator.pattern_detector.is_legitimate_technical_content(
            pattern)
        status = "✓ LEGITIMATE" if is_legit else "✗ PLACEHOLDER"
        print(f"  {status}: '{pattern}' - {reason}")

    return report.threshold_met


if __name__ == "__main__":
    success = test_validation_system()
    exit(0 if success else 1)
