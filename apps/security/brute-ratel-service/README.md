# Brute Ratel C4 Community Kit Service

This NX service contains scripts, configurations and deprecated payload loaders for Brute Ratel C4 (<https://bruteratel.com/>). This is a security toolkit integrated into the modular monolith platform for mental prosthetic tools.

## Overview

This service provides a web API to access and manage the Brute Ratel C4 Community Kit components:

- **Adhoc Scripts**: Python and shell scripts for various security operations
- **BOFs (Beacon Object Files)**: Compiled C code for Cobalt Strike/Brute Ratel operations
- **Deprecated**: Legacy payload loaders (not part of latest BRc4 releases)
- **Patch EnvExit**: Environment exit patching utilities

## Usage

### Development

```bash
# Serve the development server
npx nx serve brute-ratel-service

# Build the service
npx nx build brute-ratel-service

# Run tests
npx nx test brute-ratel-service

# Make scripts executable (run once after setup)
npx nx setup brute-ratel-service

# Build BOF files
npx nx build:bofs brute-ratel-service

# Clean BOF build artifacts
npx nx clean:bofs brute-ratel-service
```

### API Endpoints

- `GET /api` - Service information and available endpoints
- `GET /api/toolkit-info` - Detailed toolkit information
- `GET /adhoc_scripts/*` - Access adhoc scripts
- `GET /bofs/*` - Access BOF files
- `GET /deprecated/*` - Access deprecated payloaders
- `GET /patch_envexit/*` - Access patch utilities

### Security Notice

⚠️ **Warning**: This toolkit contains security research tools and should only be used in authorized testing environments. Ensure compliance with local laws and regulations.

## Directory Structure

```text
├── adhoc_scripts/          # Python and shell utilities
│   ├── badgerNotifier.py   # Badger notification script
│   ├── genssl.sh          # SSL certificate generation
│   ├── install.sh         # Installation script
│   ├── openssl_server.sh  # OpenSSL server setup
│   └── shellcode_loader_samples/  # Shellcode loading examples
├── bofs/                  # Beacon Object Files (C code)
│   ├── Makefile           # Build configuration
│   ├── *.c                # BOF source files
│   └── obj/               # Compiled objects
├── deprecated/            # Legacy components
│   ├── *.ps1              # PowerShell templates
│   └── *.yara             # YARA rules
└── patch_envexit/         # Environment patching
    ├── *.cs               # C# utilities
    └── compile.bat        # Windows compilation script
```

## Integration

This service is part of the Security Domain in the modular monolith platform, providing specialized offensive security capabilities alongside other security tools like CyberChef, HELK, Maltrail, and others.
