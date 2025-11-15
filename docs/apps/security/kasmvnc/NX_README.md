# KasmVNC Service - NX Integration

## Overview

KasmVNC provides remote web-based access to a Desktop or application. This is the NX-integrated version of the KasmVNC project, allowing easy development and deployment within the Jane Orchestrator ecosystem.

## Quick Start

### 1. Initial Setup
```bash
# Initialize submodules and install dependencies
npx nx setup kasmvnc-service
```

### 2. Build KasmVNC
```bash
# Build the main KasmVNC server
npx nx build kasmvnc-service

# Or build with Docker
npx nx build:docker kasmvnc-service
```

### 3. Build Web Interface
```bash
# Install web dependencies
npx nx web:install kasmvnc-service

# Build web interface
npx nx web:build kasmvnc-service
```

### 4. Run KasmVNC
```bash
# Run in Docker container (recommended)
npx nx serve kasmvnc-service

# Or run development container with shell access
npx nx serve:dev kasmvnc-service
```

### 5. Access the Service
- Web interface: `http://localhost:6901`
- SSL interface: `https://localhost:8443`

## Available NX Commands

### Build Commands
- `npx nx build kasmvnc-service` - Build KasmVNC server from source
- `npx nx build:docker kasmvnc-service` - Build Docker development image
- `npx nx build:deb kasmvnc-service` - Build Debian package
- `npx nx build:rpm kasmvnc-service` - Build RPM package
- `npx nx build:apk kasmvnc-service` - Build Alpine package
- `npx nx build:tarball kasmvnc-service` - Build source tarball

### Web Interface Commands
- `npx nx web:install kasmvnc-service` - Install web dependencies
- `npx nx web:build kasmvnc-service` - Build web interface
- `npx nx web:serve kasmvnc-service` - Serve web interface for development

### Development Commands
- `npx nx serve kasmvnc-service` - Run KasmVNC in Docker container
- `npx nx serve:dev kasmvnc-service` - Run development container with shell
- `npx nx test kasmvnc-service` - Run functional tests
- `npx nx setup kasmvnc-service` - Initialize project (submodules + dependencies)

### Maintenance Commands
- `npx nx init-submodules kasmvnc-service` - Initialize/update git submodules
- `npx nx clean kasmvnc-service` - Clean build artifacts

## Architecture

KasmVNC consists of several components:

1. **VNC Server** - C++ based VNC server with modern web features
2. **Web Interface** - React/JavaScript based noVNC client (kasmweb submodule)
3. **Build System** - CMake based build system with Docker containerization
4. **Package System** - Multi-format package generation (DEB, RPM, APK, tarball)

## Development Workflow

### Prerequisites
- Docker (for containerized builds)
- Git (for submodule management)
- Python 3 (for build scripts)

### Building from Source

1. **Initialize submodules**:
   ```bash
   npx nx init-submodules kasmvnc-service
   ```

2. **Build in Docker** (recommended):
   ```bash
   npx nx build:docker kasmvnc-service
   npx nx serve:dev kasmvnc-service
   
   # Inside container:
   cd kasmweb && npm install && npm run build
   builder/build.sh
   ```

3. **Run KasmVNC**:
   ```bash
   # Inside container:
   /src/xorg.build/bin/Xvnc -interface 0.0.0.0 -PublicIP 127.0.0.1 -disableBasicAuth -RectThreads 0 -Log *:stdout:100 -httpd /src/kasmweb/dist -sslOnly 0 -SecurityTypes None -websocketPort 6901 -FreeKeyMappings :1 &
   /usr/bin/xfce4-session --display :1
   ```

### Web Development

For UI changes, use the development web server:

1. **Start KasmVNC server**:
   ```bash
   npx nx serve:dev kasmvnc-service
   # Inside container, run KasmVNC as above
   ```

2. **Start web development server**:
   ```bash
   # In another terminal or container shell:
   npx nx web:serve kasmvnc-service
   ```

This provides hot-reload capabilities for web interface changes.

## Integration with Jane Orchestrator

The KasmVNC service is tagged as:
- `domain:infrastructure` - Infrastructure management tool
- `scope:desktop` - Desktop/remote access functionality
- `technology:vnc` - VNC protocol implementation
- `technology:docker` - Docker containerization support
- `technology:cpp` - C++ core implementation
- `technology:web` - Web-based interface

## Configuration

KasmVNC uses YAML configuration files:
- **Global**: `/etc/kasmvnc/kasmvnc.yaml` (server-wide settings)
- **User**: `~/.vnc/kasmvnc.yaml` (user-specific overrides)

See the main [KasmVNC documentation](https://www.kasmweb.com/kasmvnc/docs/latest/index.html) for detailed configuration options.

## Security Notes

- KasmVNC requires SSL certificates (self-signed included for development)
- Users must be added to the `ssl-cert` group on Debian/Ubuntu systems
- Multi-user support with API-based permissions management
- Data Loss Prevention features available

## Troubleshooting

### Common Issues

1. **Docker permission errors**: Ensure your user is in the docker group
2. **Submodule issues**: Run `npx nx init-submodules kasmvnc-service` to reset
3. **Build failures**: Check that all dependencies are installed in the container
4. **Web interface not loading**: Ensure web build completed successfully

### Getting Help

- Check the main [KasmVNC Documentation](https://www.kasmweb.com/kasmvnc/docs/latest/index.html)
- Review build logs in the NX output
- Inspect Docker container logs for runtime issues

## License

See [LICENSE.TXT](./LICENSE.TXT) and [ACKNOWLEDGEMENTS.md](./ACKNOWLEDGEMENTS.md) for licensing information.