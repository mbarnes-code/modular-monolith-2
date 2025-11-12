# BlackArch Service# BlackArch Service



A RESTful API service for the BlackArch Linux repository, providing access to 4,599+ penetration testing tools.A Node.js service for managing and accessing BlackArch Linux tools and packages.



## Architecture## Overview



This service follows NX best practices with a clean separation of concerns:This service provides API access to the BlackArch Linux penetration testing distribution. BlackArch contains over 2,800 security tools organized by category for penetration testing, forensics, reverse engineering, and network analysis.



```## Features

src/

├── app/- **Tool Management**: Access to BlackArch tool repository

│   ├── config/          # Configuration management- **Group Organization**: Tools categorized by functionality

│   ├── controllers/     # HTTP request handlers- **Package Information**: Detailed package metadata and build scripts

│   ├── routes/          # API route definitions- **Static File Serving**: Direct access to BlackArch repository files

│   └── services/        # Business logic

├── environments/        # Environment-specific settings## API Endpoints

├── assets/             # Static assets (BlackArch repository)

└── main.ts             # Application entry point- `GET /` - Service information and available endpoints

```- `GET /tools` - List available tools and packages

- `GET /groups` - List tool groups and categories

## Shared Libraries- `GET /blackarch/*` - Static files from BlackArch repository



The service uses shared libraries for type safety and code reuse:## BlackArch Repository Structure



- `libs/blackarch` - Common types and interfaces for BlackArch domainThe service includes the complete BlackArch repository with:



## API Endpoints- **packages/**: 2,800+ security tool packages with PKGBUILD files

- **scripts/**: Package management and build scripts

### Base URL: `/api/blackarch`- **lists/**: Tool organization files (groups, official packages, etc.)

- **docs/**: Documentation and development guides

| Method | Endpoint | Description |- **travis/**: CI/CD configuration

|--------|----------|-------------|

| GET | `/health` | Health check |## Development

| GET | `/stats` | Repository statistics |

| GET | `/packages` | List packages (paginated) |### Running the Service

| GET | `/packages/search?q={query}` | Search packages |

| GET | `/packages/{name}` | Get specific package |```bash

| GET | `/groups` | List package groups |# Development mode

npx nx serve blackarch-service

### Query Parameters

# Production build

**Pagination**:npx nx build blackarch-service

- `page` (default: 1)

- `limit` (default: 50)# Run tests

npx nx test blackarch-service

**Filtering**:```

- `group` - Filter packages by group

### Environment Variables

## Environment Configuration

- `HOST`: Server host (default: localhost)

### Development- `PORT`: Server port (default: 3000)

- Port: 3000 (configurable via `PORT` env var)

- Host: localhost## BlackArch Integration

- Logging: debug level

- Max search results: 1000This service integrates with:



### Production- **Package Management**: Arch Linux pacman compatibility

- Port: 3000 (configurable via `PORT` env var)  - **Build Systems**: PKGBUILD-based package building

- Host: 0.0.0.0- **Security Tools**: Direct access to penetration testing utilities

- Logging: info level- **Tool Categories**: Web apps, forensics, exploitation, analysis, etc.

- Max search results: 100

## Security Tools Categories

## Usage

BlackArch organizes tools into categories:

### Development

```bash- Web Application Security

npx nx serve blackarch-service- Network Analysis

```- Forensics

- Reverse Engineering

### Testing- Exploitation

```bash- Cryptography

npx nx test blackarch-service- Social Engineering

```- And many more...



### Building## License

```bash

npx nx build blackarch-serviceBlackArch Linux is released under the BSD-3-Clause license. See the COPYING file for details.

```

## Disclaimer

## Data Source

BlackArch Linux is intended for ethical hacking, penetration testing, and security research only. Use it only on systems you own or have permission to test.
The service loads package information from PKGBUILD files in the BlackArch repository structure. Package data includes:

- Name, version, release
- Description and URL
- License and architecture
- Dependencies and groups
- File path

## Error Handling

The API returns consistent error responses:

```json
{
  "success": false,
  "error": "Error message"
}
```

HTTP status codes:

- 200: Success
- 400: Bad Request (missing parameters)
- 404: Not Found (package doesn't exist)
- 500: Internal Server Error

## Performance

- Repository loaded once at startup
- In-memory search and filtering
- Configurable pagination limits
- Smart path resolution for different deployment environments