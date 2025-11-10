# MISP Custom Libraries Migration Plan

## Overview
Migrate MISP's internal PHP libraries and utilities to `libs/shared/` for integration with the modular monolith architecture.

## Library Categories Identified

### Category A: Core Utilities (Must Preserve - High Priority)
These are fundamental libraries used throughout MISP that provide essential functionality:

#### Data Processing & Conversion
- **JSONConverterTool.php** → `libs/shared/data/json_converter.py`
  - Function: Convert MISP objects to JSON format
  - Usage: Event, Attribute, Object serialization
  - Migration: Port to Python with identical output format

- **XMLConverterTool.php** → `libs/shared/data/xml_converter.py`
  - Function: XML data conversion and parsing
  - Usage: STIX/TAXII integration
  - Migration: Use Python xml.etree.ElementTree with MISP schema validation

#### Security & Cryptography
- **GpgTool.php** → `libs/shared/security/gpg_tool.py`
  - Function: GPG encryption, signing, key management
  - Usage: Digital signatures for threat intelligence
  - Migration: Use python-gnupg library, preserve all GPG operations

- **CryptGpgExtended.php** → `libs/shared/security/gpg_extended.py`
  - Function: Extended GPG functionality for MISP
  - Usage: Advanced key operations, verification
  - Migration: Extend base GPG tool with MISP-specific functions

#### Caching & Performance
- **RedisTool.php** → `libs/shared/cache/redis_tool.py`
  - Function: Redis connection management, compression
  - Usage: Caching, session storage, background jobs
  - Migration: Use redis-py with identical compression algorithms (brotli, zstd)

- **ApcuCacheTool.php** → `libs/shared/cache/memory_cache.py`
  - Function: Local memory caching
  - Usage: Performance optimization
  - Migration: Use Python cachetools library

### Category B: Domain-Specific Tools (Preserve in Service Adapters)
Tools specific to threat intelligence and security operations:

#### Export & Import
- **Export/*.php** (25 classes) → `libs/service-adapters/security/misp/export/`
  - Stix1Export, Stix2Export, YaraExport, NidsExport, etc.
  - Function: Convert MISP data to various security formats
  - Migration: Port to Python with format validation

#### Analysis & Processing
- **CorrelationGraphTool.php** → `libs/service-adapters/security/misp/analysis/correlation.py`
- **EventGraphTool.php** → `libs/service-adapters/security/misp/analysis/event_graph.py`
- **TrendingTool.php** → `libs/service-adapters/security/misp/analysis/trending.py`

### Category C: Utility Components (Shared Libraries)
General-purpose utilities that can be used across domains:

#### File & Network Operations
- **FileAccessTool.php** → `libs/shared/io/file_access.py`
- **CurlClient.php** → `libs/shared/http/http_client.py`
- **AttachmentTool.php** → `libs/shared/io/attachment_handler.py`

#### Data Validation & Processing
- **AttributeValidationTool.php** → `libs/shared/validation/attribute_validator.py`
- **ComplexTypeTool.php** → `libs/shared/data/complex_type_handler.py`
- **CidrTool.php** → `libs/shared/network/cidr_tools.py`

## Migration Strategy

### Phase 1: Core Infrastructure (Week 1)
1. Create directory structure in `libs/shared/`
2. Migrate critical tools (JSON/XML converters, Redis, GPG)
3. Implement Python equivalents with identical APIs
4. Create comprehensive unit tests comparing outputs

### Phase 2: Security-Specific Tools (Week 2)
1. Create MISP service adapter structure
2. Migrate export/import tools
3. Preserve all security format outputs
4. Validate against original MISP test data

### Phase 3: Utility Components (Week 3)
1. Migrate general-purpose utilities
2. Create shared interface contracts
3. Integrate with FastAPI dependency injection
4. Performance optimization and testing

### Phase 4: Integration & Testing (Week 4)
1. Integration testing with main MISP service adapter
2. Performance benchmarking against original
3. Security validation of cryptographic functions
4. End-to-end workflow testing

## Directory Structure

```
libs/
├── shared/
│   ├── cache/
│   │   ├── redis_tool.py           # RedisTool.php
│   │   └── memory_cache.py         # ApcuCacheTool.php
│   ├── data/
│   │   ├── json_converter.py       # JSONConverterTool.php
│   │   ├── xml_converter.py        # XMLConverterTool.php
│   │   └── complex_type_handler.py # ComplexTypeTool.php
│   ├── security/
│   │   ├── gpg_tool.py            # GpgTool.php
│   │   └── gpg_extended.py        # CryptGpgExtended.php
│   ├── http/
│   │   └── http_client.py         # CurlClient.php
│   ├── io/
│   │   ├── file_access.py         # FileAccessTool.php
│   │   └── attachment_handler.py   # AttachmentTool.php
│   ├── validation/
│   │   └── attribute_validator.py  # AttributeValidationTool.php
│   └── network/
│       └── cidr_tools.py          # CidrTool.php
└── service-adapters/
    └── security/
        └── misp/
            ├── export/
            │   ├── stix_export.py      # Stix1/2Export.php
            │   ├── yara_export.py      # YaraExport.php
            │   └── nids_export.py      # NidsExport.php
            └── analysis/
                ├── correlation.py       # CorrelationGraphTool.php
                └── event_graph.py      # EventGraphTool.php
```

## Critical Preservation Requirements

### API Compatibility
- All converted tools must maintain identical input/output interfaces
- JSON/XML output must match byte-for-byte when possible  
- Error handling and exception types must be equivalent

### Security Functions
- GPG operations must maintain cryptographic compatibility
- Key management functions must work with existing key stores
- Signature verification must work with legacy signatures

### Performance Requirements
- Redis compression algorithms (brotli, zstd) must be preserved
- Caching behavior must maintain same hit/miss patterns
- Memory usage should not exceed 120% of original

### Data Integrity
- All export formats must validate against format specifications
- Correlation algorithms must produce identical results
- Graph generation must maintain same node/edge relationships

## Testing Strategy

### Unit Testing
- Each migrated class gets comprehensive test suite
- Test data from original MISP installation
- Output comparison with original PHP tools

### Integration Testing
- Full workflow testing with actual MISP data
- Performance benchmarking
- Memory usage monitoring

### Security Testing
- Cryptographic function validation
- Key management testing
- Digital signature verification

## Migration Completion Criteria

1. All 50+ utility classes successfully migrated
2. 100% test coverage on critical functions
3. Performance meets or exceeds original
4. Security functions validated by external audit
5. Integration tests pass with real MISP data

This migration plan ensures 100% business logic preservation while modernizing the codebase for the modular monolith architecture.