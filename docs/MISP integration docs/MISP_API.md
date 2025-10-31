# MISP API Documentation

## Overview

This document provides comprehensive API documentation for the MISP integration within the modular monolith platform. All endpoints maintain backward compatibility with the original MISP API while being enhanced with additional security and performance features.

## Base URL

```
https://your-platform.com/api/security/misp
```

## Authentication

### JWT Authentication (Recommended)
```http
Authorization: Bearer <jwt_token>
```

### API Key Authentication
```http
X-API-Key: <misp_api_key>
```

### Rate Limiting
- **Default**: 100 requests per minute per API key
- **Admin endpoints**: 10 requests per minute
- **Auth endpoints**: 5 requests per minute
- **Headers**: Rate limit info returned in response headers

## Events API

### List Events
```http
GET /events
```

**Parameters:**
- `page` (integer, optional): Page number (default: 1)
- `limit` (integer, optional): Results per page (max: 100, default: 25)
- `organization` (string, optional): Filter by organization name
- `tags` (array, optional): Filter by tags
- `published` (boolean, optional): Filter by published status
- `threat_level_id` (integer, optional): Filter by threat level (1-4)
- `distribution` (integer, optional): Filter by distribution level (0-4)
- `from_date` (string, optional): Filter events from date (ISO 8601)
- `to_date` (string, optional): Filter events to date (ISO 8601)

**Example Request:**
```http
GET /events?page=1&limit=10&organization=ACME&published=true
```

**Response:**
```json
{
  "events": [
    {
      "id": "123",
      "uuid": "550e8400-e29b-41d4-a716-446655440000",
      "info": "Malware campaign targeting financial sector",
      "published": true,
      "threat_level_id": 2,
      "analysis": 1,
      "distribution": 1,
      "sharing_group_id": null,
      "timestamp": "1640995200",
      "publish_timestamp": "1640995200",
      "org_id": "1",
      "orgc_id": "1",
      "attribute_count": "15",
      "proposal_email_lock": false,
      "locked": false,
      "event_creator_email": "analyst@acme.com",
      "correlations": {
        "count": 42,
        "related_events": 8
      },
      "tags": [
        {
          "id": "1",
          "name": "tlp:white",
          "colour": "#ffffff"
        }
      ],
      "org": {
        "id": "1",
        "name": "ACME Corporation",
        "uuid": "550e8400-e29b-41d4-a716-446655440001"
      }
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 10,
    "total_pages": 15,
    "total_count": 147,
    "has_next": true,
    "has_prev": false
  },
  "performance": {
    "query_time_ms": 45,
    "cache_hit": true
  }
}
```

### Get Event
```http
GET /events/{event_id}
```

**Parameters:**
- `event_id` (string, required): Event ID or UUID
- `include_attributes` (boolean, optional): Include event attributes (default: true)
- `include_correlations` (boolean, optional): Include correlation data (default: false)

**Response:**
```json
{
  "event": {
    "id": "123",
    "uuid": "550e8400-e29b-41d4-a716-446655440000",
    "info": "Malware campaign targeting financial sector",
    "published": true,
    "threat_level_id": 2,
    "analysis": 1,
    "distribution": 1,
    "timestamp": "1640995200",
    "publish_timestamp": "1640995200",
    "attributes": [
      {
        "id": "456",
        "uuid": "550e8400-e29b-41d4-a716-446655440002",
        "event_id": "123",
        "category": "Network activity",
        "type": "domain",
        "value": "malicious-domain.com",
        "to_ids": true,
        "distribution": 1,
        "timestamp": "1640995200",
        "comment": "C2 domain observed in campaign",
        "correlations": {
          "count": 5,
          "related_attributes": [
            {
              "attribute_id": "789",
              "event_id": "124",
              "correlation_type": "domain_overlap"
            }
          ]
        }
      }
    ],
    "correlations": {
      "related_events": [
        {
          "event_id": "124",
          "correlation_count": 3,
          "correlation_types": ["domain_overlap", "ip_overlap"]
        }
      ],
      "threat_intelligence": {
        "confidence_score": 0.85,
        "severity": "high",
        "attribution": ["APT29", "Cozy Bear"]
      }
    }
  }
}
```

### Create Event
```http
POST /events
```

**Request Body:**
```json
{
  "info": "New threat intelligence event",
  "threat_level_id": 2,
  "analysis": 0,
  "distribution": 1,
  "sharing_group_id": null,
  "published": false,
  "tags": ["tlp:white", "malware"],
  "attributes": [
    {
      "category": "Network activity",
      "type": "domain",
      "value": "suspicious-domain.com",
      "to_ids": true,
      "distribution": 1,
      "comment": "Observed in recent campaign"
    }
  ]
}
```

**Response:**
```json
{
  "event": {
    "id": "125",
    "uuid": "550e8400-e29b-41d4-a716-446655440003",
    "info": "New threat intelligence event",
    "created": true,
    "attributes_created": 1,
    "correlations_found": 0
  },
  "validation": {
    "passed": true,
    "warnings": [],
    "auto_correlations": true
  }
}
```

### Update Event
```http
PUT /events/{event_id}
```

**Request Body:** (Same structure as create, only changed fields required)

### Delete Event
```http
DELETE /events/{event_id}
```

**Response:**
```json
{
  "success": true,
  "event_id": "125",
  "deleted_attributes": 5,
  "audit_logged": true
}
```

## Attributes API

### List Attributes
```http
GET /attributes
```

**Parameters:**
- `event_id` (string, optional): Filter by event ID
- `category` (string, optional): Filter by category
- `type` (string, optional): Filter by attribute type
- `value` (string, optional): Search by value (supports wildcards)
- `to_ids` (boolean, optional): Filter by IDS flag
- `include_correlations` (boolean, optional): Include correlation data

**Response:**
```json
{
  "attributes": [
    {
      "id": "456",
      "uuid": "550e8400-e29b-41d4-a716-446655440002",
      "event_id": "123",
      "category": "Network activity",
      "type": "domain",
      "value": "malicious-domain.com",
      "to_ids": true,
      "distribution": 1,
      "timestamp": "1640995200",
      "comment": "C2 domain observed in campaign",
      "correlations": {
        "count": 5,
        "confidence_score": 0.92,
        "related_events": ["124", "126", "127"]
      },
      "enrichment": {
        "reputation_score": 0.1,
        "whois_data": {
          "registrar": "Suspicious Registrar Inc",
          "creation_date": "2025-10-30"
        },
        "dns_resolution": ["192.168.1.100", "10.0.0.1"]
      }
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 25,
    "total_count": 1247
  }
}
```

### Create Attribute
```http
POST /attributes
```

**Request Body:**
```json
{
  "event_id": "123",
  "category": "Network activity",
  "type": "ip-dst",
  "value": "192.168.1.100",
  "to_ids": true,
  "distribution": 1,
  "comment": "Malicious IP observed in logs",
  "auto_correlate": true
}
```

**Response:**
```json
{
  "attribute": {
    "id": "789",
    "uuid": "550e8400-e29b-41d4-a716-446655440004",
    "created": true,
    "correlations_found": 3,
    "enrichment_applied": true
  },
  "correlations": [
    {
      "attribute_id": "790",
      "event_id": "124",
      "correlation_type": "ip_overlap",
      "confidence": 0.95
    }
  ]
}
```

## Correlations API

### Get Correlations
```http
GET /correlations/{attribute_id}
```

**Parameters:**
- `attribute_id` (string, required): Attribute ID or UUID
- `correlation_types` (array, optional): Filter by correlation types
- `confidence_threshold` (float, optional): Minimum confidence score (0.0-1.0)
- `max_results` (integer, optional): Maximum results to return (default: 50, max: 200)

**Response:**
```json
{
  "correlations": {
    "source_attribute": {
      "id": "456",
      "type": "domain",
      "value": "malicious-domain.com"
    },
    "related_attributes": [
      {
        "id": "789",
        "event_id": "124",
        "type": "domain",
        "value": "malicious-domain.com",
        "correlation_type": "exact_match",
        "confidence_score": 1.0,
        "temporal_proximity": "2 days"
      },
      {
        "id": "790",
        "event_id": "125",
        "type": "ip-dst",
        "value": "192.168.1.100",
        "correlation_type": "infrastructure_overlap",
        "confidence_score": 0.85,
        "temporal_proximity": "1 week"
      }
    ],
    "threat_intelligence": {
      "campaign_attribution": ["APT29"],
      "technique_mapping": ["T1071.001"],
      "severity_assessment": "high",
      "false_positive_probability": 0.05
    },
    "statistics": {
      "total_correlations": 15,
      "high_confidence": 8,
      "medium_confidence": 5,
      "low_confidence": 2
    }
  },
  "performance": {
    "correlation_time_ms": 234,
    "cache_hit": false
  }
}
```

### Bulk Correlation Analysis
```http
POST /correlations/analyze
```

**Request Body:**
```json
{
  "attributes": [
    {
      "type": "domain",
      "value": "suspicious1.com"
    },
    {
      "type": "ip-dst",
      "value": "10.0.0.1"
    }
  ],
  "analysis_options": {
    "confidence_threshold": 0.7,
    "temporal_window_days": 30,
    "include_attribution": true
  }
}
```

**Response:**
```json
{
  "analysis_results": [
    {
      "input_attribute": {
        "type": "domain",
        "value": "suspicious1.com"
      },
      "correlations_found": 12,
      "highest_confidence": 0.94,
      "campaign_links": ["Operation XYZ"],
      "related_events": ["123", "124", "126"]
    }
  ],
  "batch_statistics": {
    "total_processed": 2,
    "total_correlations": 18,
    "processing_time_ms": 456
  }
}
```

## Organizations API

### List Organizations
```http
GET /organizations
```

**Response:**
```json
{
  "organizations": [
    {
      "id": "1",
      "uuid": "550e8400-e29b-41d4-a716-446655440001",
      "name": "ACME Corporation",
      "description": "Information security team",
      "type": "Corporate",
      "nationality": "US",
      "sector": "Financial Services",
      "created_by": "1",
      "date_created": "1640995200",
      "date_modified": "1640995200",
      "contacts": [
        {
          "type": "email",
          "value": "security@acme.com"
        }
      ],
      "statistics": {
        "events_contributed": 45,
        "attributes_contributed": 1247,
        "sharing_agreements": 12
      }
    }
  ]
}
```

## Taxonomies API

### List Taxonomies
```http
GET /taxonomies
```

**Response:**
```json
{
  "taxonomies": [
    {
      "id": "1",
      "namespace": "tlp",
      "description": "Traffic Light Protocol",
      "version": "1.0",
      "predicates": [
        {
          "value": "white",
          "expanded": "TLP:WHITE",
          "description": "Disclosure is not limited"
        },
        {
          "value": "green",
          "expanded": "TLP:GREEN", 
          "description": "Limited disclosure, restricted to community"
        }
      ]
    }
  ]
}
```

## Search API

### Advanced Search
```http
POST /search
```

**Request Body:**
```json
{
  "query": {
    "type": "advanced",
    "criteria": [
      {
        "field": "attribute.value",
        "operator": "contains",
        "value": "malicious"
      },
      {
        "field": "event.threat_level_id",
        "operator": "in",
        "value": [1, 2]
      }
    ],
    "logic": "AND"
  },
  "options": {
    "include_attributes": true,
    "include_correlations": false,
    "max_results": 100
  }
}
```

**Response:**
```json
{
  "search_results": {
    "events": [...],
    "attributes": [...],
    "correlations": [...]
  },
  "search_metadata": {
    "query_executed": "2025-10-31T09:00:00Z",
    "execution_time_ms": 123,
    "total_results": 42,
    "cache_hit": false
  }
}
```

## Export API

### Export Events
```http
GET /export/events/{format}
```

**Formats:** `json`, `xml`, `csv`, `stix`, `misp-json`

**Parameters:**
- `event_ids` (array, optional): Specific event IDs to export
- `from_date` (string, optional): Export from date
- `to_date` (string, optional): Export to date
- `published_only` (boolean, optional): Only published events
- `include_attributes` (boolean, optional): Include attributes

**Response:** Binary file download or structured data based on format

## Webhooks API

### List Webhooks
```http
GET /webhooks
```

### Create Webhook
```http
POST /webhooks
```

**Request Body:**
```json
{
  "name": "Threat Intelligence Webhook",
  "url": "https://your-system.com/misp-webhook",
  "events": ["event.create", "attribute.create", "correlation.found"],
  "secret": "webhook_secret_key",
  "active": true,
  "ssl_verify": true
}
```

## Error Responses

### Standard Error Format
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Request validation failed",
    "details": {
      "field": "threat_level_id",
      "issue": "Value must be between 1 and 4"
    },
    "request_id": "req_550e8400-e29b-41d4-a716-446655440000"
  },
  "timestamp": "2025-10-31T09:00:00Z"
}
```

### HTTP Status Codes

- `200 OK`: Request successful
- `201 Created`: Resource created successfully
- `400 Bad Request`: Invalid request data
- `401 Unauthorized`: Authentication required
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Resource not found
- `422 Unprocessable Entity`: Validation failed
- `429 Too Many Requests`: Rate limit exceeded
- `500 Internal Server Error`: Server error

### Error Codes

- `AUTHENTICATION_REQUIRED`: Missing or invalid authentication
- `AUTHORIZATION_DENIED`: Insufficient permissions for operation
- `VALIDATION_ERROR`: Request data validation failed
- `RESOURCE_NOT_FOUND`: Requested resource does not exist
- `RATE_LIMIT_EXCEEDED`: API rate limit exceeded
- `CORRELATION_TIMEOUT`: Correlation analysis timed out
- `EXPORT_FAILED`: Data export operation failed
- `WEBHOOK_DELIVERY_FAILED`: Webhook delivery failed

## Performance Characteristics

### Response Time Targets
- **List operations**: <200ms
- **Get single resource**: <100ms
- **Create operations**: <300ms
- **Correlation analysis**: <500ms
- **Complex searches**: <1000ms
- **Export operations**: <2000ms

### Rate Limits
- **Default**: 100 requests/minute per API key
- **Admin operations**: 10 requests/minute
- **Authentication**: 5 attempts/minute
- **Bulk operations**: 10 requests/minute
- **Export operations**: 5 requests/minute

### Caching
- **Event lists**: 5 minutes
- **Event details**: 10 minutes
- **Organization data**: 1 hour
- **Taxonomy data**: 24 hours
- **Correlation results**: 30 minutes

---

**API Version**: 2.4.0 (MISP compatible)  
**Last Updated**: 2025-10-31  
**Authentication**: Required for all endpoints  
**Rate Limiting**: Enforced per API key