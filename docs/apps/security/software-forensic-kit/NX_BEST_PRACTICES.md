# Software Forensic Kit - NX Workspace Integration

This document outlines how the Software Forensic Kit follows NX best practices.

## Project Structure

```
apps/software-forensic-kit-service/           # Main application
├── .env.development                           # Development environment config
├── .env.production                           # Production environment config  
├── .nxignore                                 # NX configuration documentation
├── project.json                              # NX project configuration
├── pom.xml                                   # Maven build configuration
├── Dockerfile                                # Production container
├── Dockerfile.dev                            # Development container
└── src/                                      # Source code

libs/forensic-core/                           # Shared forensic utilities
├── project.json                              # NX project configuration
├── pom.xml                                   # Maven build configuration
└── src/                                      # Shared source code
```

## NX Best Practices Applied

### 1. Proper Tagging Strategy
```json
"tags": [
  "scope:security",      // Functional scope
  "type:service",        // Project type
  "framework:maven",     // Build framework
  "language:java",       // Primary language
  "runtime:jvm",         // Runtime platform
  "domain:forensics"     // Business domain
]
```

### 2. Multiple Configurations
Each target supports multiple configurations:
- **build**: `development`, `production`
- **serve**: `development`, `production`  
- **test**: `coverage`, `integration`
- **analyze**: `help`, `local`, `remote`, `agent`
- **docker**: `production`, `development`

### 3. Proper Caching Strategy
Cached targets for performance:
- `build` - Compilation results
- `test` - Test results
- `lint` - Linting results
- `format:check` - Format validation

### 4. Dependency Management
- **Implicit Dependencies**: Automatic build ordering via `^build`
- **Explicit Dependencies**: Clear target dependencies (`package` depends on `build`)
- **Shared Libraries**: `forensic-core` lib for common utilities

### 5. Output Management
Proper output declarations for caching:
- `{projectRoot}/target` - Build outputs
- `{projectRoot}/target/*.jar` - Package outputs
- `{projectRoot}/target/surefire-reports` - Test reports

### 6. Environment-Specific Configuration
- `.env.development` - Development settings
- `.env.production` - Production settings
- Multiple Dockerfile variants

### 7. Standardized Commands

#### Development Workflow
```bash
# Build the project
npx nx build software-forensic-kit-service

# Run tests with coverage
npx nx test software-forensic-kit-service:coverage

# Lint and format check
npx nx lint software-forensic-kit-service
npx nx format:check software-forensic-kit-service

# Package for distribution
npx nx package software-forensic-kit-service

# Run analysis (various modes)
npx nx analyze software-forensic-kit-service:help
npx nx analyze software-forensic-kit-service:local
npx nx analyze software-forensic-kit-service:remote
```

#### Docker Workflow
```bash
# Build development image
npx nx docker:build software-forensic-kit-service:development

# Run interactive analysis
npx nx docker:run software-forensic-kit-service:interactive

# Run batch analysis
npx nx docker:run software-forensic-kit-service:analysis
```

### 8. Integration with NX Graph
The project integrates properly with NX dependency graph:
- Libraries built before applications
- Proper cache invalidation
- Correct affect detection

### 9. Consistent Tooling
- **Maven** for Java build management
- **Spotless** for code formatting
- **Checkstyle** for code quality
- **JaCoCo** for test coverage
- **Docker** for containerization

### 10. Performance Optimization
- Parallel execution where possible
- Intelligent caching strategies
- Proper resource management
- Environment-specific tuning

## Usage Examples

### Local Development
```bash
# Quick development cycle
npx nx build software-forensic-kit-service:development
npx nx test software-forensic-kit-service
npx nx serve software-forensic-kit-service:development

# Code quality checks
npx nx lint software-forensic-kit-service
npx nx format software-forensic-kit-service
```

### Production Build
```bash
# Production build and package
npx nx build software-forensic-kit-service:production
npx nx package software-forensic-kit-service
npx nx docker:build software-forensic-kit-service:production
```

### Analysis Operations
```bash
# Local JAR analysis
searchFunction="*vulnerable*" jarFilter="./samples" npx nx analyze software-forensic-kit-service:local

# Remote analysis via SSH
sshUser="analyst" sshHost="target.server.com" sshPass="password" searchFunction="*security*" jarFilter="/opt/app/lib" npx nx analyze software-forensic-kit-service:remote

# Java agent instrumentation
targetClass="com.example.Service" targetMethod="processData" targetJar="./app.jar" npx nx analyze software-forensic-kit-service:agent
```

## Integration Points

### With Jane Orchestrator
The service integrates with the main orchestrator through:
- Shared security domain tagging
- Common environment variables
- Standardized API patterns

### With Other Security Services
- Shared utilities via `forensic-core` library
- Common security analysis patterns
- Consistent configuration management

### With CI/CD
- Proper caching for faster builds
- Environment-specific configurations
- Container-ready deployments

This structure ensures the Software Forensic Kit follows NX best practices while maintaining its specialized functionality for binary analysis and security assessment.