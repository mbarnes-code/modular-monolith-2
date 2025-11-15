# MISP API Documentation

**Version**: 1.0.0  
**MISP Version**: 2.5.22  
**PyMISP Version**: 2.5.17.1  
**Generated**: 2025-10-31T16:00:00Z

## Overview

This API provides access to the MISP (Malware Information Sharing Platform) 
threat intelligence data and functionality. The API maintains compatibility 
with the original MISP REST API while providing modern OpenAPI/Swagger 
specifications.

## Authentication

The API supports two authentication methods:

1. **Authorization Header**: `Authorization: Bearer <api-key>`
2. **X-MISP-AuthKey Header**: `X-MISP-AuthKey: <api-key>`

## Response Formats

The API supports multiple response formats:

- **JSON** (default): `Accept: application/json`
- **XML**: `Accept: application/xml` or append `.xml` to endpoint
- **CSV**: `Accept: text/csv` or append `.csv` to endpoint

## Compatibility Layer

The API includes a multi-target compatibility layer that supports:

- **Web Mode**: Browser-based access with CORS headers
- **Node.js Mode**: Server-side Node.js optimized responses
- **Legacy Mode**: Original CakePHP API format compatibility
- **Modern Mode**: Standard REST API format

## API Endpoints

### Attributes

#### Add MISP Attribute

**Method**: `POST`  
**Path**: `/attributes/add/{event_id}`

POST a MISP Attribute JSON to this API to create an Attribute.

**URL Parameters**:

| Parameter | Type | Description |
|-----------|------|-------------|
| event_id | integer | Event ID to add attribute to |

**Required Parameters**:

| Parameter | Type | Description |
|-----------|------|-------------|
| value | string | Attribute value |
| type | string | The type of the attribute |

**Optional Parameters**:

| Parameter | Type | Description |
|-----------|------|-------------|
| category | string |  |
| to_ids | integer | State of the to_ids flag |
| uuid | string |  |
| distribution | integer |  |
| sharing_group_id | integer |  |
| timestamp | integer |  |
| comment | string |  |
| data | string | Base64 encoded file contents |
| encrypt | integer |  |
| first_seen | string |  |
| last_seen | string |  |

---

#### Edit MISP Attribute

**Method**: `POST`  
**Path**: `/attributes/edit/{attribute_id}`

POST a MISP Attribute JSON to update. Timestamp must be newer if set.

**URL Parameters**:

| Parameter | Type | Description |
|-----------|------|-------------|
| attribute_id | integer | Attribute ID to edit |

---

#### Search MISP Attributes

**Method**: `POST`  
**Path**: `/attributes/restSearch`

Search MISP using filter parameters. Supports pagination via page and limit.

**Required Parameters**:

| Parameter | Type | Description |
|-----------|------|-------------|
| returnFormat | string |  |

---

### Events

#### Add MISP Event

**Method**: `POST`  
**Path**: `/events/add`

Create new MISP event

---

#### Edit MISP Event

**Method**: `POST`  
**Path**: `/events/edit/{event_id}`

Update existing MISP event

---

#### Search MISP Events

**Method**: `POST`  
**Path**: `/events/restSearch`

Search events with filter parameters

---

### Organisations

#### List Organizations

**Method**: `GET`  
**Path**: `/organisations`

Get list of MISP organizations

---

### Tags

#### List Tags

**Method**: `GET`  
**Path**: `/tags`

Get list of MISP tags

---

### Galaxies

#### List Galaxies

**Method**: `GET`  
**Path**: `/galaxies`

Get list of MISP galaxies

---

## Data Models

### MISPAttribute

Core MISP attribute data structure with threat intelligence indicators.

```json
{
  "id": 123,
  "event_id": 456,
  "category": "Network activity",
  "type": "ip-dst",
  "value": "192.168.1.1",
  "to_ids": true,
  "uuid": "550e8400-e29b-41d4-a716-446655440000",
  "timestamp": 1635724800,
  "distribution": 3,
  "comment": "Malicious IP address",
  "first_seen": "2021-11-01T12:00:00Z",
  "last_seen": "2021-11-01T18:00:00Z"
}
```

### MISPEvent

MISP event containing threat intelligence information and attributes.

```json
{
  "id": 456,
  "orgc_id": 1,
  "org_id": 1,
  "date": "2021-11-01",
  "threat_level_id": 3,
  "info": "Malware campaign targeting financial institutions",
  "published": true,
  "uuid": "550e8400-e29b-41d4-a716-446655440001",
  "analysis": 1,
  "distribution": 3,
  "timestamp": 1635724800
}
```

## Error Handling

The API returns standard HTTP status codes:

- **200**: Success
- **400**: Bad Request - Invalid parameters
- **401**: Unauthorized - Invalid API key
- **403**: Forbidden - Insufficient permissions
- **404**: Not Found - Resource not found
- **500**: Internal Server Error

Error responses include details in JSON format:

```json
{
  "error": "Validation failed",
  "message": "Required field 'type' is missing",
  "timestamp": "2021-11-01T12:00:00Z"
}
```

## Legacy Compatibility

The API maintains full compatibility with original MISP CakePHP endpoints:

- URL extensions (`.json`, `.xml`, `.csv`) are supported
- Original parameter names and formats are preserved
- Response structure matches original MISP API
- Authentication methods are fully compatible

## Rate Limiting

API requests are subject to rate limiting:

- 1000 requests per hour per API key
- Burst limit of 100 requests per minute
- Rate limit headers included in all responses

## Versioning

The API uses semantic versioning with backward compatibility guarantees:

- **v1.x**: Current stable version
- **v2.x**: Future major version (when available)
- Deprecation notices provided 6 months before breaking changes