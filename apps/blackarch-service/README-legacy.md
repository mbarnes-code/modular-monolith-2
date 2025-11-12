# BlackArch Service

A Node.js service for managing and accessing BlackArch Linux tools and packages.

## Overview

This service provides API access to the BlackArch Linux penetration testing distribution. BlackArch contains over 2,800 security tools organized by category for penetration testing, forensics, reverse engineering, and network analysis.

## Features

- **Tool Management**: Access to BlackArch tool repository
- **Group Organization**: Tools categorized by functionality
- **Package Information**: Detailed package metadata and build scripts
- **Static File Serving**: Direct access to BlackArch repository files

## API Endpoints

- `GET /` - Service information and available endpoints
- `GET /tools` - List available tools and packages
- `GET /groups` - List tool groups and categories
- `GET /blackarch/*` - Static files from BlackArch repository

## BlackArch Repository Structure

The service includes the complete BlackArch repository with:

- **packages/**: 2,800+ security tool packages with PKGBUILD files
- **scripts/**: Package management and build scripts
- **lists/**: Tool organization files (groups, official packages, etc.)
- **docs/**: Documentation and development guides
- **travis/**: CI/CD configuration

## Development

### Running the Service

```bash
# Development mode
npx nx serve blackarch-service

# Production build
npx nx build blackarch-service

# Run tests
npx nx test blackarch-service
```

### Environment Variables

- `HOST`: Server host (default: localhost)
- `PORT`: Server port (default: 3000)

## BlackArch Integration

This service integrates with:

- **Package Management**: Arch Linux pacman compatibility
- **Build Systems**: PKGBUILD-based package building
- **Security Tools**: Direct access to penetration testing utilities
- **Tool Categories**: Web apps, forensics, exploitation, analysis, etc.

## Security Tools Categories

BlackArch organizes tools into categories:

- Web Application Security
- Network Analysis
- Forensics
- Reverse Engineering
- Exploitation
- Cryptography
- Social Engineering
- And many more...

## License

BlackArch Linux is released under the BSD-3-Clause license. See the COPYING file for details.

## Disclaimer

BlackArch Linux is intended for ethical hacking, penetration testing, and security research only. Use it only on systems you own or have permission to test.