# APIScout Service - NX Integration

This is the NX-integrated version of APIScout, a library for Windows API usage recovery and similarity assessment with focus on memory dumps.

## Project Structure

```
apps/apiscout-service/
├── src/apiscout/           # Main APIScout library
├── tests/                  # Test files
├── infrastructure/docker/  # Docker configuration
├── *.py                    # Command-line tools
├── GhidraScout.java       # Ghidra plugin
├── dbs/                   # Example databases
└── project.json           # NX project configuration
```

## Available NX Commands

### Core Services
- `nx serve apiscout-service` - Run main scout.py
- `nx serve:collect apiscout-service` - Run collect.py (database builder)
- `nx serve:match apiscout-service` - Run match.py (vector matching)
- `nx serve:export apiscout-service` - Run export.py (ApiQR diagrams)
- `nx serve:update apiscout-service` - Run update.py (Malpedia sync)

### Development
- `nx test apiscout-service` - Run tests
- `nx test:coverage apiscout-service` - Run tests with coverage
- `nx lint apiscout-service` - Check code style
- `nx lint:fix apiscout-service` - Fix code style issues
- `nx build apiscout-service` - Build the package
- `nx install apiscout-service` - Install in development mode

### Docker
- `nx docker:build apiscout-service` - Build Docker image
- `nx docker:run apiscout-service` - Run with Docker Compose
- `nx docker:stop apiscout-service` - Stop Docker services

## Command-Line Tools

### Scout (Main Tool)
```bash
cd apps/apiscout-service
python scout.py <memory_dump> <database>
```

### Database Builder
```bash
cd apps/apiscout-service
python collect.py <dll_directory> <output_db>
```

### Vector Matching
```bash
cd apps/apiscout-service
python match.py <vector_file> <database>
```

### ApiQR Export
```bash
cd apps/apiscout-service
python export.py <vector_file> <output_image>
```

### IDA Pro Plugin
Copy `ida_scout.py` to your IDA Pro plugins directory for GUI integration.

### Ghidra Plugin
Import `GhidraScout.java` into Ghidra for reverse engineering integration.

## Dependencies

Core dependencies are defined in `requirements.txt`:
- numpy (numerical computations)
- Pillow (image processing for ApiQR)
- lief (PE file parsing)
- requests (HTTP requests for updates)

Development dependencies in `pyproject.toml`:
- pytest (testing framework)
- black (code formatting)
- isort (import sorting)
- flake8 (linting)
- mypy (type checking)

## Integration with Jane Platform

This service is integrated into the broader Jane mental prosthetic platform:

1. **Security Domain**: APIScout provides malware analysis capabilities
2. **Executive Function Support**: CLI tools accessible through unified interface
3. **Data Pipeline**: Can feed results to other security analysis tools
4. **Docker Integration**: Containerized for consistent deployment

## Original Documentation

See the main `README.md` for complete APIScout documentation and usage examples.

## Migration Status

✅ **Complete** - All files migrated from `features/apiscout/` to NX project structure
✅ **NX Configuration** - Project targets and commands configured
✅ **Docker Support** - Dockerfile and compose configuration added
✅ **Development Tools** - Linting, formatting, and testing configured
✅ **Python Package** - Modern pyproject.toml setup

## Performance Requirements

As part of the Security domain:
- **Target Response Time**: <1s (security analysis criticality)
- **Memory Efficiency**: Optimized for large dump analysis
- **Batch Processing**: Support for multiple file processing
- **Integration Ready**: API endpoints for Jane orchestrator integration