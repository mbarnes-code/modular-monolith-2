# Dispatch Database Library

Database models, migrations, and data access layer for the Dispatch incident management ecosystem.

## Overview

`dispatch-database` is a comprehensive database library that provides all data persistence functionality for Dispatch-related projects. This library follows NX best practices by centralizing database concerns into a reusable, well-tested module.

## Architecture

This library provides complete database functionality for the Dispatch ecosystem:

### **Core Components**

- **Database** (`database/`): Connection management and session handling
- **Models** (`models/`): SQLAlchemy ORM models for all entities
- **Migrations** (`migrations/`): Alembic database migration scripts
- **Schemas** (`schemas/`): Pydantic schemas for API serialization

### **Design Principles**

- **Single Source of Truth**: All database schemas defined here
- **Migration Management**: Proper version control for database changes
- **Performance Optimized**: Efficient queries and proper indexing
- **Type Safety**: Full type hints and Pydantic integration

## Usage

### Installing in your NX project

Add to your project's dependencies in `project.json`:

```json
{
  "targets": {
    "build": {
      "dependsOn": ["^build"],
      "options": {
        "dependencies": ["dispatch-database", "dispatch-core"]
      }
    }
  }
}
```

### Database Connection

```python
from dispatch_database.data.database import (
    get_db,
    get_session,
    init_db,
    create_tables
)

# Initialize database
init_db()

# Get database session
with get_session() as session:
    # Your database operations here
    pass

# FastAPI dependency injection
@app.get("/incidents")
def get_incidents(db: Session = Depends(get_db)):
    return db.query(Incident).all()
```

### Model Usage

```python
# Import models
from dispatch_database.data.models import (
    Incident,
    Task,
    Individual,
    Service,
    Team,
    IncidentType,
    IncidentPriority
)

# Query operations
incidents = session.query(Incident).filter(
    Incident.status == IncidentStatus.ACTIVE
).all()

# Create new incident
new_incident = Incident(
    title="System Outage",
    description="Database connection issues",
    status=IncidentStatus.ACTIVE,
    priority=IncidentPriority.HIGH
)
session.add(new_incident)
session.commit()
```

## Database Schema

### **Core Entities**

#### Incident Management
- `Incident`: Core incident entity with status, priority, timeline
- `IncidentType`: Categorization of incident types
- `IncidentPriority`: Priority levels for incidents
- `Event`: Timeline events for incident tracking

#### Task Management  
- `Task`: Individual tasks associated with incidents
- `TaskStatus`: Task completion states
- `TaskAssignment`: Assignment of tasks to individuals

#### People and Organizations
- `Individual`: Person entities (responders, reporters, etc.)
- `Team`: Organizational teams
- `Service`: Systems and services involved in incidents
- `Contact`: Contact information and methods

#### Communication
- `Conversation`: Communication threads (Slack, email, etc.)
- `Document`: Associated documentation and runbooks
- `Notification`: Alert and notification records

### **Database Relationships**

```mermaid
erDiagram
    Incident ||--o{ Task : contains
    Incident ||--o{ Event : timeline
    Incident }o--|| IncidentType : classified_as
    Incident }o--|| IncidentPriority : has_priority
    Task }o--|| Individual : assigned_to
    Individual }o--|| Team : member_of
    Service ||--o{ Incident : affects
```

## Migrations

### Running Migrations

```bash
# NX commands
npx nx migrations-upgrade dispatch-database   # Apply migrations
npx nx migrations-downgrade dispatch-database # Rollback migrations

# Direct alembic commands
cd libs/dispatch-database
alembic upgrade head                          # Apply all migrations
alembic downgrade -1                          # Rollback one migration
alembic revision --autogenerate -m "description"  # Create new migration
```

### Migration Management

The library uses Alembic for database migrations:

- **Location**: `src/data/migrations/`
- **Configuration**: `alembic.ini` and `src/data/migrations/env.py`
- **Auto-generation**: Detects model changes automatically
- **Version Control**: All migrations tracked in Git

### Creating New Migrations

```bash
# After modifying models
cd libs/dispatch-database
alembic revision --autogenerate -m "Add new incident fields"

# Review generated migration file
# Edit if needed for complex changes
# Test migration
alembic upgrade head
```

## Model Reference

### **Incident Model**

```python
class Incident(DispatchModel):
    __tablename__ = "incident"
    
    # Core fields
    title: str
    description: str
    status: IncidentStatus
    priority: IncidentPriority
    
    # Timestamps
    reported_at: datetime
    started_at: Optional[datetime]
    ended_at: Optional[datetime]
    
    # Relationships
    tasks: List["Task"] = relationship("Task", back_populates="incident")
    events: List["Event"] = relationship("Event", back_populates="incident")
    incident_type: "IncidentType" = relationship("IncidentType")
    
    # Participants
    commander: Optional["Individual"] = relationship("Individual", foreign_keys=[commander_id])
    reporter: Optional["Individual"] = relationship("Individual", foreign_keys=[reporter_id])
    participants: List["Individual"] = relationship("Individual", secondary=incident_participants)
```

### **Task Model**

```python
class Task(DispatchModel):
    __tablename__ = "task"
    
    # Core fields
    description: str
    status: TaskStatus = TaskStatus.OPEN
    priority: TaskPriority = TaskPriority.MEDIUM
    
    # Assignment
    assignee: Optional["Individual"] = relationship("Individual")
    incident: "Incident" = relationship("Incident", back_populates="tasks")
    
    # Timing
    due_at: Optional[datetime]
    completed_at: Optional[datetime]
```

## Development

### NX Commands

```bash
# Testing
npx nx test dispatch-database             # Run unit tests  
npx nx test-cov dispatch-database        # Run tests with coverage

# Code Quality
npx nx lint dispatch-database            # Run linting
npx nx lint-fix dispatch-database        # Fix linting issues
npx nx format dispatch-database          # Format code
npx nx type-check dispatch-database      # Type checking

# Building
npx nx build dispatch-database           # Build library
```

### Adding New Models

1. **Create Model**: Add to appropriate module in `src/data/`
2. **Import**: Add to `src/data/models/__init__.py`
3. **Migration**: Generate with `alembic revision --autogenerate`
4. **Test**: Add comprehensive model tests
5. **Document**: Update this README with model reference

### Testing Database Models

```python
# Example model test
def test_incident_creation(db_session):
    incident = Incident(
        title="Test Incident",
        description="Test Description",
        status=IncidentStatus.ACTIVE,
        priority=IncidentPriority.HIGH
    )
    
    db_session.add(incident)
    db_session.commit()
    
    assert incident.id is not None
    assert incident.title == "Test Incident"
    assert incident.status == IncidentStatus.ACTIVE
```

## Dependencies

### Runtime Dependencies

- `sqlalchemy`: ORM and database toolkit
- `alembic`: Database migration management
- `psycopg2-binary`: PostgreSQL adapter
- `pydantic`: Data validation and serialization
- `dispatch-core`: Shared types and utilities

### Development Dependencies

- `pytest`: Testing framework
- `pytest-asyncio`: Async testing support
- `factory-boy`: Test data generation
- `mypy`: Type checking
- `ruff`: Linting and formatting

## Configuration

### Database Settings

```python
# Environment variables
DATABASE_URL=postgresql://user:password@localhost/dispatch
DATABASE_ECHO=false  # Set to true for SQL logging

# Connection pooling
SQLALCHEMY_POOL_SIZE=10
SQLALCHEMY_MAX_OVERFLOW=20
SQLALCHEMY_POOL_TIMEOUT=30
```

### Alembic Configuration

```ini
# alembic.ini
[alembic]
script_location = src/data/migrations
sqlalchemy.url = postgresql://user:password@localhost/dispatch

[logging]
level = INFO
```

## Migration Notes

This library was extracted from the main `dispatch-service` to follow NX best practices:

- **Before**: Database code mixed with application logic
- **After**: Clean separation with dedicated data access layer  
- **Benefits**: Better testability, reusable across services, clear data contracts

## Related Libraries

- **dispatch-core**: Core utilities and types (dependency)
- **dispatch-service**: Main application service (depends on dispatch-database)

## Project Tags

- `type:library` - Database library
- `domain:data-access` - Data persistence domain
- `scope:shared` - Cross-project database layer