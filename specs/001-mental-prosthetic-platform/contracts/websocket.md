# WebSocket API Contracts

## Overview
Real-time communication protocols for the Mental Prosthetic Platform using WebSocket connections with secure authentication.

## Connection Endpoints

### AI Communication WebSocket
**Endpoint**: `/ws/ai`
**Purpose**: Real-time bidirectional communication with LLM server
**Authentication**: JWT token in connection header

#### Connection Flow
1. Client sends connection request with JWT token
2. Server validates token and establishes WebSocket connection
3. Client can send messages and receive responses in real-time
4. Connection maintains heartbeat for health monitoring

#### Message Types

##### Client to Server

**AI Chat Message**:
```json
{
  "type": "ai_chat",
  "messageId": "uuid",
  "timestamp": "ISO8601",
  "payload": {
    "message": "string",
    "context": {
      "currentTask": "uuid",
      "executiveFunctionType": "Planning|Organization|TimeManagement|WorkingMemory",
      "userState": "focused|distracted|overwhelmed|hyperfocus"
    },
    "expectResponse": true
  }
}
```

**Task Breakdown Request**:
```json
{
  "type": "task_breakdown",
  "messageId": "uuid",
  "timestamp": "ISO8601",
  "payload": {
    "taskId": "uuid",
    "complexity": "Simple|Detailed|Adaptive",
    "currentBlockers": ["string"],
    "timeAvailable": 60
  }
}
```

**Context Update**:
```json
{
  "type": "context_update",
  "messageId": "uuid", 
  "timestamp": "ISO8601",
  "payload": {
    "userState": "focused|distracted|overwhelmed|hyperfocus",
    "currentTool": "string",
    "activeTasks": ["uuid"],
    "environmentalFactors": {
      "timeOfDay": "morning|afternoon|evening|night",
      "workloadLevel": "low|medium|high"
    }
  }
}
```

##### Server to Client

**AI Response**:
```json
{
  "type": "ai_response",
  "messageId": "uuid",
  "replyTo": "uuid",
  "timestamp": "ISO8601",
  "payload": {
    "message": "string",
    "suggestions": ["string"],
    "confidence": 0.95,
    "followUpQuestions": ["string"],
    "actionItems": [{
      "action": "string",
      "priority": "Low|Medium|High|Critical",
      "estimatedTime": 15
    }]
  }
}
```

**Task Breakdown Response**:
```json
{
  "type": "task_breakdown_response",
  "messageId": "uuid",
  "replyTo": "uuid", 
  "timestamp": "ISO8601",
  "payload": {
    "taskId": "uuid",
    "subtasks": [{
      "title": "string",
      "description": "string",
      "estimatedDuration": 30,
      "order": 1,
      "executiveFunctionType": "Planning|Organization|TimeManagement|WorkingMemory",
      "difficulty": "Easy|Medium|Hard"
    }],
    "strategy": "string",
    "tips": ["string"],
    "warningFlags": ["string"]
  }
}
```

**Proactive Reminder**:
```json
{
  "type": "proactive_reminder",
  "messageId": "uuid",
  "timestamp": "ISO8601",
  "payload": {
    "reminderType": "break|task|routine|medication",
    "message": "string",
    "urgency": "Low|Medium|High",
    "dismissible": true,
    "snoozeOptions": [5, 10, 30],
    "relatedTask": "uuid"
  }
}
```

### Synchronization WebSocket
**Endpoint**: `/ws/sync`
**Purpose**: Real-time data synchronization across all integrated tools
**Authentication**: JWT token in connection header

#### Message Types

##### Client to Server

**Sync Request**:
```json
{
  "type": "sync_request",
  "messageId": "uuid",
  "timestamp": "ISO8601",
  "payload": {
    "components": ["frontend", "orchestrator", "tool_adapter"],
    "since": "ISO8601",
    "priority": "Low|Medium|High"
  }
}
```

**Data Change**:
```json
{
  "type": "data_change",
  "messageId": "uuid",
  "timestamp": "ISO8601",
  "payload": {
    "entityType": "Task|UserProfile|IntegratedTool",
    "entityId": "uuid", 
    "operation": "create|update|delete",
    "changes": {
      "field": "newValue"
    },
    "sourceComponent": "string"
  }
}
```

##### Server to Client

**Sync Status**:
```json
{
  "type": "sync_status",
  "messageId": "uuid",
  "timestamp": "ISO8601",
  "payload": {
    "overallStatus": "Synced|Syncing|Error",
    "components": [{
      "name": "string",
      "status": "Online|Offline|Error|Syncing",
      "lastSync": "ISO8601",
      "errorMessage": "string"
    }],
    "pendingChanges": 5
  }
}
```

**Data Sync**:
```json
{
  "type": "data_sync",
  "messageId": "uuid",
  "timestamp": "ISO8601", 
  "payload": {
    "entityType": "Task|UserProfile|IntegratedTool",
    "operation": "create|update|delete",
    "data": {},
    "sourceComponent": "string",
    "version": "string"
  }
}
```

**Sync Error**:
```json
{
  "type": "sync_error",
  "messageId": "uuid",
  "timestamp": "ISO8601",
  "payload": {
    "errorCode": "CONFLICT|TIMEOUT|VALIDATION|NETWORK",
    "message": "string",
    "entityId": "uuid",
    "retryable": true,
    "retryAfter": 30
  }
}
```

## Connection Management

### Authentication
- JWT tokens must be included in the `Authorization` header during WebSocket handshake
- Connections are automatically closed if token expires
- Refresh token mechanism available through REST API

### Heartbeat Protocol
- Client sends ping every 30 seconds: `{"type": "ping", "timestamp": "ISO8601"}`
- Server responds with pong: `{"type": "pong", "timestamp": "ISO8601"}`
- Connection closed if 3 consecutive pings fail

### Error Handling
```json
{
  "type": "error",
  "messageId": "uuid",
  "timestamp": "ISO8601",
  "payload": {
    "errorCode": "AUTHENTICATION|VALIDATION|RATE_LIMIT|INTERNAL",
    "message": "string",
    "details": {},
    "retryable": false
  }
}
```

### Rate Limiting
- AI chat: 60 messages per minute
- Sync requests: 120 per minute  
- Context updates: 10 per minute
- Violations result in temporary connection throttling

### Security Features
- All messages validated against JSON schemas
- Message size limited to 1MB
- Connection monitoring for unusual patterns
- Automatic disconnect for suspicious activity

## Integration with Service Adapters

### Tool-Specific WebSocket Events
Service adapters can publish events through the sync WebSocket:

**Security Tool Event**:
```json
{
  "type": "tool_event",
  "messageId": "uuid",
  "timestamp": "ISO8601",
  "payload": {
    "toolName": "MISP|Nemesis|HELK",
    "eventType": "threat_detected|analysis_complete|alert_triggered",
    "data": {},
    "severity": "Low|Medium|High|Critical",
    "actionRequired": true
  }
}
```

**Productivity Tool Event**:
```json
{
  "type": "tool_event", 
  "messageId": "uuid",
  "timestamp": "ISO8601",
  "payload": {
    "toolName": "n8n|actual|mealie",
    "eventType": "workflow_complete|budget_alert|recipe_added",
    "data": {},
    "userNotification": true
  }
}
```

### Cross-Tool Communication
Tools can communicate through the platform:

```json
{
  "type": "cross_tool_message",
  "messageId": "uuid",
  "timestamp": "ISO8601", 
  "payload": {
    "sourceTool": "string",
    "targetTool": "string",
    "action": "string",
    "data": {},
    "priority": "Low|Medium|High"
  }
}
```

## Client Implementation Guidelines

### Connection Management
1. Establish connections after successful authentication
2. Implement exponential backoff for reconnection attempts
3. Handle graceful degradation when WebSocket unavailable
4. Maintain connection state in application store

### Message Handling
1. Always include messageId for request tracking
2. Implement timeout handling for request-response patterns
3. Queue messages when connection is temporarily unavailable
4. Validate all incoming messages against schemas

### Error Recovery
1. Retry failed messages with exponential backoff
2. Fallback to REST API when WebSocket fails
3. Notify user of connectivity issues
4. Maintain offline capabilities where possible