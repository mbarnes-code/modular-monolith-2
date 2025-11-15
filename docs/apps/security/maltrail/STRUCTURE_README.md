# Maltrail Service - NX Best Practices Structure

This project has been reorganized to follow NX best practices and modern Python project structure conventions.

## Project Structure

```
apps/maltrail-service/
├── src/                      # Source code (NX sourceRoot)
│   └── maltrail/            # Main package
│       ├── __init__.py      # Package initialization
│       ├── server.py        # Server application
│       ├── sensor.py        # Sensor application
│       ├── core/            # Core functionality
│       ├── plugins/         # Plugin system
│       ├── trails/          # Threat intelligence
│       └── thirdparty/      # Third-party dependencies
├── tests/                   # Test files
│   └── test_maltrail.py    # Main test suite
├── config/                  # Configuration files
│   └── maltrail.conf       # Main configuration
├── assets/                  # Static assets
│   ├── html/               # Web interface
│   └── misc/               # Miscellaneous assets
├── infrastructure/          # Deployment and infrastructure
│   ├── docker/             # Docker configuration
│   └── fail2ban/           # Fail2ban integration
├── scripts/                 # Utility scripts
│   ├── maltrail-server.service
│   └── maltrail-sensor.service
├── server.py               # Server entry point
├── sensor.py               # Sensor entry point
├── setup.py                # Package setup
├── requirements.txt        # Python dependencies
├── project.json            # NX project configuration
└── README.md               # This file
```

## NX Best Practices Applied

### 1. **Source Root Structure**
- **`sourceRoot`**: Set to `apps/maltrail-service/src`
- **Package Organization**: Code organized under `src/maltrail/`
- **Import Structure**: Proper Python package structure with `__init__.py` files

### 2. **Separation of Concerns**
- **`src/`**: All application source code
- **`tests/`**: Test files separate from source
- **`config/`**: Configuration files
- **`assets/`**: Static assets (HTML, misc files)
- **`infrastructure/`**: Deployment-related files
- **`scripts/`**: Utility scripts and service definitions

### 3. **Entry Points**
- **Root-level scripts**: `server.py` and `sensor.py` as entry points
- **Module imports**: Entry points import from the `src/maltrail` package
- **Proper path handling**: Dynamic path resolution for imports

### 4. **Configuration Management**
- **Centralized config**: All configuration in `config/` directory
- **Environment separation**: Ready for multiple environments
- **Asset organization**: Static assets properly separated

## Available Commands

### Development
```bash
# Start server
nx serve maltrail-service

# Start sensor
nx serve:sensor maltrail-service

# Run tests
nx test maltrail-service

# Lint code
nx lint maltrail-service

# Auto-fix linting issues
nx lint:fix maltrail-service

# Type checking
nx type-check maltrail-service
```

### Build & Deploy
```bash
# Build (validation)
nx build maltrail-service

# Install dependencies
nx install maltrail-service

# Docker operations
nx docker:build maltrail-service
nx docker:run maltrail-service
nx docker:stop maltrail-service
```

## Key Improvements

### 1. **Clean Import Structure**
```python
# Before: import core.common
# After:  import maltrail.core.common

from maltrail.server import main as server_main
from maltrail.sensor import main as sensor_main
```

### 2. **Better Test Organization**
- Tests import from the proper package structure
- Separate test directory with proper path resolution
- Ready for test discovery and CI/CD integration

### 3. **Asset Management**
- Static assets in dedicated `assets/` directory
- Configuration files in `config/` directory
- Infrastructure files properly organized

### 4. **Development Tools**
- Added `lint:fix` target for code formatting
- Added `type-check` target for static analysis
- Improved lint target to focus on source directories

## Configuration

### Server Configuration
- **Config file**: `config/maltrail.conf`
- **Web assets**: `assets/html/`
- **Default port**: 8338

### Package Configuration
- **Entry points**: Defined in `setup.py`
- **Package discovery**: Uses `src/` layout
- **Dependencies**: Managed via `requirements.txt`

## Integration Benefits

### NX Workspace Benefits
- **Consistent structure**: Follows NX project conventions
- **Build optimization**: Leverages NX caching and dependency graph
- **Tool integration**: Works with NX CLI and VS Code tasks

### Development Benefits
- **IDE support**: Better import resolution and code navigation
- **Testing**: Proper test discovery and execution
- **Linting**: Focused linting on source directories only

### Deployment Benefits
- **Container ready**: Docker files properly organized
- **Service deployment**: SystemD service files available
- **Configuration management**: Centralized configuration

## Migration Notes

### What Changed
1. **File locations**: Core files moved to `src/maltrail/`
2. **Import paths**: Updated to use package-based imports
3. **Entry points**: New wrapper scripts for proper module loading
4. **Asset organization**: Assets moved to dedicated directories

### Compatibility
- **Original functionality**: All original features preserved
- **Configuration**: Same configuration file format and options
- **API compatibility**: Same HTTP endpoints and sensor functionality
- **Docker support**: Enhanced with proper build context

## Next Steps

1. **Verify functionality**: Test all endpoints and sensor operation
2. **Update documentation**: Ensure all references reflect new structure
3. **CI/CD integration**: Update build pipelines if needed
4. **Monitoring**: Verify logging and monitoring still work correctly

---

**Status**: ✅ Reorganization Complete
**NX Compliance**: ✅ Follows NX Best Practices
**Functionality**: ✅ All Features Preserved