# Meterpreter Service

This is the NX-integrated version of the Meterpreter payload project, originally from Rapid7's Metasploit Framework.

## Overview

Meterpreter is a payload that provides an interactive shell with built-in functionality for penetration testing. This project contains the source code for building Meterpreter payloads for both Windows and POSIX environments.

**Note**: This repository contains the archived version of Meterpreter that was merged into metasploit-payloads. See the original README.md for historical context.

## Available NX Commands

### Building

Build the project (defaults to production):
```bash
npx nx build meterpreter-service
```

Build for development (debug mode):
```bash
npx nx build meterpreter-service --configuration=development
```

Build for specific architectures:
```bash
npx nx build meterpreter-service --configuration=x86
npx nx build meterpreter-service --configuration=x64
```

### Setup

Initialize and update git submodules (required before first build):
```bash
npx nx setup meterpreter-service
```

### Maintenance

Clean build artifacts:
```bash
npx nx clean meterpreter-service
```

Deep clean (removes all generated files):
```bash
npx nx really-clean meterpreter-service
```

### Installation

Install built payloads to metasploit-framework (requires framework_dir configuration):
```bash
npx nx install meterpreter-service
```

## Build Requirements

### Windows
- Visual Studio 2013 Express for Desktop (or paid version)
- .NET Framework 4.5.1
- Git (for submodules)

### POSIX/Linux
- GCC toolchain (build-essential on Ubuntu)
- gcc-multilib (for 64-bit machines building 32-bit)
- jam, wget, flex, bison
- Internet connection (downloads OpenSSL and libpcap during build)

### Ubuntu 14.04+
```bash
apt-get install gcc jam make flex bison gcc-multilib
```

### Fedora 21+
```bash
yum install gcc jam make flex patch bison glibc-devel.i686 libgcc.i686
```

## Project Structure

- `source/` - Core Meterpreter source code
- `workspace/` - Visual Studio workspace and build files
- `output/` - Compiled binaries (created during build)
- `tools/` - Build tools and utilities
- `content/` - Additional content files

## Security Context

This project is part of the security domain tools in the modular monolith platform. It provides:

- Payload generation capabilities
- Post-exploitation functionality
- Extension system for additional capabilities
- Cross-platform compatibility

## Integration Notes

- Tagged with `scope:security`, `type:native`, `framework:make`
- Outputs built to `dist/apps/meterpreter-service`
- No automated testing available (manual testing required)
- Requires manual setup of submodules before first build

## Original Documentation

See `README.md` in the root directory for complete build instructions and technical details from the original Meterpreter project.