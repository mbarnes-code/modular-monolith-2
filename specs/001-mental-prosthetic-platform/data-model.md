# Data Model: Mental Prosthetic Platform

**Date**: 2025-10-18  
**Purpose**: Define unified data structures for integrated executive function tools

## Core Entities

### User Profile
Represents the ADHD/autism user and their executive function preferences.

**Attributes**:
- `id`: UUID - Primary identifier
- `email`: String - User email for authentication
- `displayName`: String - Preferred display name
- `adhdSettings`: Object - ADHD-specific preferences
  - `reminderFrequency`: Enum - Never, Low, Medium, High
  - `taskBreakdownPreference`: Enum - Simple, Detailed, Adaptive
  - `focusSessionLength`: Integer - Minutes (default: 25)
- `autismSettings`: Object - Autism-specific preferences
  - `sensoryMode`: Enum - Minimal, Standard, Rich
  - `routineReminders`: Boolean - Enable routine notifications
  - `communicationStyle`: Enum - Direct, Structured, Adaptive
- `aiPersonality`: Object - AI interaction preferences
  - `communicationStyle`: String - Learned adaptive style
  - `reminderTone`: Enum - Gentle, Direct, Encouraging
  - `proactiveLevel`: Enum - Low, Medium, High
- `createdAt`: DateTime
- `lastActiveAt`: DateTime

**Relationships**:
- Has many `UnifiedSession`
- Has many `Task`
- Has one `AIContext`

### Integrated Tool
Represents individual executive function applications and their integration status.

**Attributes**:
- `id`: UUID - Primary identifier
- `name`: String - Tool name (e.g., "MISP", "n8n", "commander-spellbook")
- `domain`: Enum - Security, Productivity, MTG, Infrastructure
- `originalPath`: String - Original path in features/ directory
- `integrationStatus`: Enum - Pending, InProgress, Completed, Failed
- `businessLogicPreserved`: Boolean - Verification flag
- `adapterModule`: String - Path to service adapter
- `uiComponents`: Array<String> - List of UI component paths
- `dependencies`: Array<UUID> - Other tools this depends on
- `dataSchema`: Object - Tool-specific data structure
- `apiEndpoints`: Array<Object> - Available API endpoints
- `capabilities`: Array<String> - What the tool can do
- `migrationDate`: DateTime - When integration was completed

**Relationships**:
- Belongs to `UserProfile`
- Has many `Task` (cross-tool relationships)
- Has one `SyncState`

### AI Context
Manages the LLM's understanding of user patterns and preferences.

**Attributes**:
- `userId`: UUID - Foreign key to UserProfile
- `interactionHistory`: Array<Object> - Previous AI conversations
- `taskPatterns`: Object - Learned user task patterns
- `reminderSchedules`: Array<Object> - Active reminders
- `personalizationData`: Object - Adaptive learning data
- `communicationStyle`: String - Current learned style
- `successfulStrategies`: Array<Object> - What has worked for the user
- `lastLLMSync`: DateTime - Last sync with LLM server
- `contextVersion`: String - For compatibility tracking

**Relationships**:
- Belongs to `UserProfile`
- Related to all `Task` through context analysis

### Task
Unified representation of activities across all integrated tools.

**Attributes**:
- `id`: UUID - Primary identifier
- `userId`: UUID - Foreign key to UserProfile
- `title`: String - Task title
- `description`: Text - Detailed description
- `status`: Enum - Todo, InProgress, Completed, Cancelled
- `priority`: Enum - Low, Medium, High, Critical
- `dueDate`: DateTime - Optional due date
- `estimatedDuration`: Integer - Minutes
- `actualDuration`: Integer - Actual time spent
- `sourceToolId`: UUID - Foreign key to IntegratedTool
- `aiBreakdown`: Array<Object> - AI-generated subtasks
- `dependencies`: Array<UUID> - Other tasks this depends on
- `tags`: Array<String> - User-defined tags
- `executiveFunctionType`: Enum - Planning, Organization, TimeManagement, WorkingMemory
- `completionStrategy`: Object - AI-suggested approach
- `createdAt`: DateTime
- `updatedAt`: DateTime

**Relationships**:
- Belongs to `UserProfile`
- Belongs to `IntegratedTool`
- Has many `Task` (dependencies)
- Related to `AIContext`

### Unified Session
Manages single sign-on across all integrated tools.

**Attributes**:
- `id`: UUID - Primary identifier
- `userId`: UUID - Foreign key to UserProfile
- `sessionToken`: String - JWT token
- `refreshToken`: String - For token renewal
- `activeTools`: Array<UUID> - Currently accessed tools
- `lastActivity`: DateTime - Last user interaction
- `deviceInfo`: Object - Device and browser information
- `location`: String - Geographic location (if enabled)
- `expiresAt`: DateTime - Session expiration
- `isRemoteAccess`: Boolean - Whether accessed remotely

**Relationships**:
- Belongs to `UserProfile`
- Related to multiple `IntegratedTool`

### Sync State
Tracks real-time synchronization status between components.

**Attributes**:
- `id`: UUID - Primary identifier
- `componentType`: Enum - Frontend, Orchestrator, LLMServer, Tool
- `componentId`: String - Identifier for the component
- `lastSyncAt`: DateTime - Last successful sync
- `syncStatus`: Enum - Synced, Pending, Failed, Offline
- `errorMessage`: String - If sync failed
- `dataVersion`: String - Version of synced data
- `websocketConnectionId`: String - Active WebSocket connection
- `retryCount`: Integer - Failed sync attempts
- `nextRetryAt`: DateTime - When to retry sync

**Relationships**:
- May belong to `IntegratedTool`
- Related to `UserProfile`

## Domain-Specific Extensions

### Security Domain Extensions
Additional fields for security tools (MISP, Nemesis, HELK, etc.):

**ThreatIndicator** (extends Task):
- `iocType`: Enum - IP, Domain, Hash, URL
- `severity`: Enum - Low, Medium, High, Critical
- `confidence`: Float - 0.0 to 1.0
- `source`: String - Origin of indicator

**SecurityEvent** (extends Task):
- `eventType`: String - Type of security event
- `affectedSystems`: Array<String>
- `mitigation`: Text - Response actions taken

### Productivity Domain Extensions
Additional fields for productivity tools (n8n, actual, mealie, etc.):

**WorkflowTask** (extends Task):
- `workflowId`: String - n8n workflow identifier
- `automationTrigger`: String - What triggers this task
- `inputData`: Object - Workflow input parameters

**BudgetItem** (extends Task):
- `amount`: Decimal - Financial amount
- `category`: String - Budget category
- `account`: String - Associated account

### MTG Domain Extensions
Additional fields for Magic: The Gathering tools:

**ComboTask** (extends Task):
- `cards`: Array<Object> - Cards involved in combo
- `colors`: Array<String> - Mana colors required
- `manaCost`: String - Total mana cost
- `complexity`: Enum - Simple, Medium, Complex

## Data Relationships

### Cross-Tool Data Flow
Tasks can reference data from multiple tools:
- Security alerts can trigger workflow automations
- Budget changes can create security monitoring tasks
- MTG deck building can integrate with general task management

### AI Context Integration
The AI Context entity maintains relationships with all other entities to provide:
- Personalized task breakdowns based on user patterns
- Proactive reminders based on historical data
- Cross-tool insights and suggestions

### Migration Tracking
Each IntegratedTool tracks its migration status to ensure:
- Complete business logic preservation
- Successful data migration from features/ directory
- Proper cleanup of original project files

## Validation Rules

### User Profile Constraints
- Email must be unique and valid format
- Settings objects must contain all required fields
- AI personality settings must be within defined enums

### Task Constraints
- Must belong to a valid user and tool
- Dependencies cannot create cycles
- Duration estimates must be positive integers
- Status transitions must follow defined workflow

### Session Management
- Only one active session per user per device
- Sessions must expire within 24 hours for security
- Remote access sessions have additional validation

### Data Consistency
- All foreign keys must reference valid entities
- Sync states must be updated within 5 seconds of changes
- AI context must be refreshed every 24 hours