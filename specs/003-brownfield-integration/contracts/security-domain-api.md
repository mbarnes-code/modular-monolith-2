# Security Domain API Contract

**Domain**: Security (13 tools)  
**Created**: 2025-11-03  
**Tools**: MISP, HELK, SecurityOnion, YARA-X, Maltrail, CyberChef, Nemesis, MalwareBazaar MCP, VirusTotal MCP, ApexSeeker, BlackArch, Brute-Ratel-C4, Software Forensic Kit

## Domain Performance Requirements

- **Response Time SLA**: <1s (threat analysis criticality)
- **Throughput**: 1000+ threat indicators/minute
- **Availability**: 99.9% uptime (security monitoring critical)
- **Data Retention**: 7 years (compliance requirements)

## Core API Interfaces

### Threat Intelligence Operations (MISP Preservation)

```python
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
import uuid

class ThreatIndicatorRequest(BaseModel):
    """Preserve MISP Event.php functionality - 8,733 lines of correlation logic"""
    indicator_value: str = Field(..., description="IOC value (IP, domain, hash, URL)")
    indicator_type: str = Field(..., description="IOC type classification")
    confidence: float = Field(ge=0.0, le=1.0, description="Confidence score 0.0-1.0")
    tlp_marking: str = Field(default="WHITE", description="Traffic Light Protocol marking")
    source_tool: str = Field(..., description="Original tool (misp, maltrail, etc.)")
    context: Dict[str, Any] = Field(default_factory=dict, description="Additional context data")

class ThreatCorrelationResult(BaseModel):
    """Results from MISP correlation engine preservation"""
    correlation_id: uuid.UUID
    related_indicators: List[str] = Field(description="Correlated IOCs")
    correlation_score: float = Field(ge=0.0, le=1.0, description="Correlation strength")
    threat_families: List[str] = Field(description="Associated threat actor families")
    attack_patterns: List[str] = Field(description="MITRE ATT&CK patterns")
    confidence_level: str = Field(description="HIGH, MEDIUM, LOW confidence")

@app.post("/security/threats/analyze", response_model=ThreatCorrelationResult)
async def analyze_threat_indicator(
    request: ThreatIndicatorRequest,
    credentials: SecurityCredentials = Depends(get_security_credentials),
    audit_context: AuditContext = Depends(get_audit_context)
) -> ThreatCorrelationResult:
    """
    Analyze threat indicator using preserved MISP correlation algorithms
    
    Business Logic Preservation:
    - Implements 8,733 lines of MISP Event.php correlation logic
    - Maintains attribute relationship analysis
    - Preserves object template processing
    - Uses original threat scoring algorithms
    
    Performance: <1s response time (security SLA requirement)
    Security: Requires security domain authentication + audit logging
    """
    # Implementation preserves original MISP correlation engine
    pass
```

### Network Security Operations (HELK + SecurityOnion Preservation)

```python
class NetworkSecurityEvent(BaseModel):
    """Preserve HELK/SecurityOnion log analysis functionality"""
    event_id: uuid.UUID
    timestamp: datetime
    source_ip: str
    destination_ip: str
    event_type: str = Field(description="suricata, zeek, osquery, etc.")
    raw_log: str = Field(description="Original log entry")
    parsed_fields: Dict[str, Any] = Field(description="Extracted log fields")
    
class SecurityAlertResponse(BaseModel):
    """Security alert processing results"""
    alert_id: uuid.UUID
    severity: str = Field(description="CRITICAL, HIGH, MEDIUM, LOW")
    event_classification: str
    recommended_actions: List[str]
    related_events: List[uuid.UUID]
    threat_indicators: List[str]

@app.post("/security/events/analyze", response_model=SecurityAlertResponse)
async def analyze_network_event(
    event: NetworkSecurityEvent,
    credentials: SecurityCredentials = Depends(get_security_credentials)
) -> SecurityAlertResponse:
    """
    Network security event analysis (HELK + SecurityOnion logic preservation)
    
    Business Logic Preservation:
    - HELK Elasticsearch query patterns
    - SecurityOnion Suricata rule processing
    - Zeek log analysis algorithms
    - Sigma rule correlation
    
    Performance: <1s analysis time
    Integration: Triggers cross-domain productivity alerts for incidents
    """
    pass
```

### Malware Analysis Operations (YARA-X + CyberChef Preservation)

```python
class MalwareAnalysisRequest(BaseModel):
    """Preserve YARA-X + CyberChef analysis capabilities"""
    file_hash: Optional[str] = Field(description="File hash for analysis")
    file_data: Optional[bytes] = Field(description="Binary file data")
    yara_rules: Optional[List[str]] = Field(description="Custom YARA rules to apply")
    cyberchef_recipe: Optional[str] = Field(description="CyberChef operation chain")
    analysis_depth: str = Field(default="standard", description="quick, standard, deep")

class MalwareAnalysisResult(BaseModel):
    """Comprehensive malware analysis results"""
    analysis_id: uuid.UUID
    file_classification: str
    yara_matches: List[str] = Field(description="Matched YARA rule names")
    threat_score: float = Field(ge=0.0, le=100.0)
    cyberchef_results: Dict[str, Any] = Field(description="CyberChef operation results")
    iocs_extracted: List[str] = Field(description="Extracted indicators")
    family_classification: Optional[str]

@app.post("/security/malware/analyze", response_model=MalwareAnalysisResult) 
async def analyze_malware_sample(
    request: MalwareAnalysisRequest,
    credentials: SecurityCredentials = Depends(get_security_credentials)
) -> MalwareAnalysisResult:
    """
    Malware analysis using YARA-X + CyberChef preserved algorithms
    
    Business Logic Preservation:
    - YARA-X WASM compilation engine (~1,500 lines)
    - CyberChef 300+ operations preservation
    - Pattern matching algorithm integrity
    - File format analysis capabilities
    
    Performance: <1s for standard analysis, <5s for deep analysis
    Security: Sandboxed execution environment for malware samples
    """
    pass
```

## Cross-Domain Event Publishing (Async-Only)

### Security Event Publication

```python
class SecurityDomainEvent(BaseModel):
    """Base class for all security domain events"""
    event_id: uuid.UUID = Field(default_factory=uuid.uuid4)
    event_type: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    source_tool: str
    severity: str
    encrypted_payload: bytes = Field(description="Encrypted event data for sensitive intel")
    event_signature: str = Field(description="Digital signature for integrity")

class ThreatDetectedEvent(SecurityDomainEvent):
    """Published when new threat is detected"""
    threat_indicator: str
    threat_type: str
    confidence_score: float
    target_domains: List[str] = Field(description="Domains that should be notified")

@app.post("/security/events/publish")
async def publish_security_event(
    event: SecurityDomainEvent,
    target_domains: List[str] = Query(description="productivity, tcg, infrastructure")
) -> PublishResult:
    """
    Publish security events to other domains (async-only communication)
    
    Event Flow Examples:
    - Threat detected → Productivity domain (create security incident task)
    - Vulnerability found → Infrastructure domain (trigger patching workflow)  
    - Malware analysis complete → All domains (update threat intelligence)
    
    Security: All events encrypted + signed for integrity
    Performance: <100ms event publishing (non-blocking)
    """
    pass
```

## Authentication & Authorization

### Security Domain Permissions

```python
class SecurityPermissions(BaseModel):
    """Security domain specific permissions"""
    can_analyze_threats: bool = False
    can_create_yara_rules: bool = False  
    can_access_malware_samples: bool = False
    can_view_network_logs: bool = False
    can_correlate_intelligence: bool = False
    clearance_level: str = Field(description="PUBLIC, CONFIDENTIAL, SECRET")

class SecurityCredentials(BaseModel):
    """Security domain authentication context"""
    user_id: uuid.UUID
    organization_id: uuid.UUID
    permissions: SecurityPermissions
    session_token: str
    mfa_verified: bool = Field(description="Multi-factor auth required for sensitive ops")
    audit_context: Dict[str, Any]

# Authentication dependency
async def get_security_credentials(
    token: str = Depends(oauth2_scheme)
) -> SecurityCredentials:
    """Validate security domain access with federated identity"""
    pass
```

## Error Handling & Monitoring

### Security-Specific Error Responses

```python
class SecurityAPIException(HTTPException):
    """Security domain specific error handling"""
    
class ThreatAnalysisTimeout(SecurityAPIException):
    """Threat analysis exceeded 1s SLA"""
    status_code = 408
    
class InsufficientClearance(SecurityAPIException):
    """User lacks required security clearance"""
    status_code = 403

class MalwareQuarantineRequired(SecurityAPIException):
    """Sample requires quarantine before analysis"""
    status_code = 423

# Performance monitoring for <1s SLA
@app.middleware("http")
async def security_performance_monitor(request, call_next):
    """Monitor security domain performance SLA compliance"""
    start_time = time.time()
    response = await call_next(request)
    processing_time = time.time() - start_time
    
    if processing_time > 1.0:  # Security domain <1s requirement
        logger.warning(f"Security SLA violation: {processing_time:.2f}s")
        
    return response
```

## Integration Validation

### API Operation Test Mapping

This contract maps to existing API operation tests:

- **CRUD Operations**: 156 security-related tests from 822 total
- **Authentication Tests**: 475 tests validate security access patterns
- **Threat Analysis Tests**: Custom tests for MISP correlation preservation
- **Network Security Tests**: HELK/SecurityOnion log processing validation
- **Malware Analysis Tests**: YARA-X + CyberChef algorithm preservation tests

### Business Logic Preservation Validation

Each API endpoint includes validation against original tools:

1. **MISP correlation results** must match original Event.php output
2. **YARA-X pattern matching** must produce identical results to original engine
3. **CyberChef operations** must generate same output as web interface
4. **HELK queries** must return equivalent Elasticsearch results
5. **SecurityOnion alerts** must match original Salt state processing

---

**Security Domain API Contract** | **Performance SLA**: <1s | **Next**: Productivity Domain Contract