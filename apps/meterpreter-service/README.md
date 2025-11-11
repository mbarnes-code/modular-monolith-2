# Meterpreter Service

[![NX](https://img.shields.io/badge/Built%20with-NX-blue)](https://nx.dev)
[![Security](https://img.shields.io/badge/Domain-Security-red)](https://github.com/rapid7/metasploit-framework)

Meterpreter payload generation service integrated into the modular monolith platform.

## Overview

This service provides Meterpreter payload compilation capabilities within the NX monorepo structure. Meterpreter is an advanced payload that provides interactive shell functionality for penetration testing through the Metasploit Framework.

> **Note**: This is based on the archived Meterpreter repository that was merged into [metasploit-payloads](https://github.com/rapid7/metasploit-payloads).

## Quick Start

```bash
# Setup development environment
npx nx setup meterpreter-service

# Build all architectures
npx nx build meterpreter-service

# Run tests
npx nx test meterpreter-service
```

## Project Structure

```
apps/meterpreter-service/
├── src/                    # Source code (C/C++)
│   ├── client/            # Client-side components
│   ├── common/            # Shared utilities
│   ├── extensions/        # Meterpreter extensions
│   └── server/            # Server-side components
├── workspace/             # Visual Studio build files
├── scripts/               # Build and utility scripts
├── docs/                  # Documentation
├── tests/                 # Test files
└── content/               # Additional content
```

meterpreter >

## Available Commands

### Core Operations

```bash
# Setup development environment (run first)
npx nx setup meterpreter-service

# Build for production
npx nx build meterpreter-service

# Build for specific architectures
npx nx build meterpreter-service --configuration=x86
npx nx build meterpreter-service --configuration=x64

# Build all architectures
npx nx build:all meterpreter-service
```

### Development & Testing

```bash
# Run integration tests
npx nx test meterpreter-service

# Run advanced integration tests
npx nx test:integration meterpreter-service

# Format code (requires clang-format)
npx nx format meterpreter-service

# Lint code (requires clang-format)
npx nx lint meterpreter-service
```

### Maintenance

```bash
# Clean build artifacts
npx nx clean meterpreter-service

# Deep clean (including dependencies)
npx nx clean:all meterpreter-service

# Generate documentation (requires doxygen)
npx nx docs meterpreter-service

# Analyze built payloads
npx nx analyze meterpreter-service

# Install to metasploit framework
npx nx install meterpreter-service
```

## System Requirements

### Windows

- Visual Studio 2013 Express for Desktop or newer
- .NET Framework 4.5.1 or newer
- Git (for submodules)

### Linux/POSIX

**Ubuntu/Debian:**

```bash
apt-get install gcc jam make flex bison gcc-multilib clang-format doxygen
```

**Fedora/RHEL:**

```bash
yum install gcc jam make flex patch bison glibc-devel.i686 libgcc.i686
```

**macOS:**

```bash
brew install gcc make jam flex bison clang-format doxygen
```

## Architecture Support

- **x86**: 32-bit Intel/AMD processors
- **x64**: 64-bit Intel/AMD processors
- **Cross-compilation**: Supported for different target platforms

## Dependencies

The build system automatically downloads required dependencies:

- **OpenSSL 0.9.8za**: Cryptographic functionality
- **libpcap 1.1.1**: Network packet capture
- **Reflective DLL Injection**: Windows payload injection (submodule)

## Integration with Metasploit Framework

Built payloads can be installed directly to a Metasploit Framework installation:

1. Configure `FRAMEWORK_DIR` in `.env`
2. Run `npx nx install meterpreter-service`

This copies compiled payloads to `data/meterpreter/` in the framework directory.

## Extending Meterpreter

Create new extensions by:

1. Adding source to `src/extensions/yourname/`
2. Creating corresponding workspace project in `workspace/ext_server_yourname/`
3. Following the build patterns from existing extensions

See `docs/CONTRIBUTING.md` for detailed extension development guide.

## Security Considerations

- Built payloads are for authorized penetration testing only
- Ensure proper authorization before deployment
- Follow responsible disclosure practices
- Comply with applicable laws and regulations

## Troubleshooting

### Build Issues

```bash
# Check system dependencies
npx nx setup meterpreter-service

# Clean and rebuild
npx nx clean:all meterpreter-service
npx nx build meterpreter-service
```

### Submodule Issues

```bash
# Reset submodules
git submodule deinit --all
npx nx setup meterpreter-service
```

## Documentation

- `docs/NX_README.md`: NX-specific usage guide
- `docs/CONTRIBUTING.md`: Development guidelines
- Original documentation: See sections below for legacy information

## Original Project Context

> **Historical Note**: This service is based on the archived Meterpreter repository that was merged into [metasploit-payloads](https://github.com/rapid7/metasploit-payloads). The integration preserves all original functionality while adding NX monorepo benefits.

---

## Legacy Build Information

The following sections contain the original build documentation for reference:
