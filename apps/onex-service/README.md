# Onex Service

A modern TypeScript/Node.js API wrapper for the Onex hacking tools installer and package manager.

## Overview

Onex is originally a shell script-based hacking tools installer for Termux and other Linux distributions that can install **370+ Kali Linux hacking tools**. This service provides a modern REST API interface while preserving all the original functionality.

## Features

- **370+ Security Tools**: Access to a comprehensive library of ethical hacking and penetration testing tools
- **Modern REST API**: TypeScript/Node.js API with Express.js framework
- **Tool Management**: Install, search, and manage security tools programmatically
- **Category Organization**: Tools organized by categories (Information Gathering, Web Hacking, etc.)
- **Real-time Status**: Check installation status of tools
- **Cross-Platform**: Works on Linux distributions and Termux (Android)

## API Endpoints

### Tools
- `GET /api/onex/tools` - List all available tools
- `GET /api/onex/tools/:name` - Get tool information and installation status
- `POST /api/onex/tools/:name/install` - Install a specific tool
- `GET /api/onex/tools/:name/status` - Check if tool is installed

### Categories
- `GET /api/onex/categories` - List all tool categories
- `GET /api/onex/categories/:category/tools` - Get tools by category

### Search & Discovery
- `GET /api/onex/search?q=<query>` - Search tools by name
- `GET /api/onex/stats` - Get statistics about tools and categories

### System
- `POST /api/onex/update` - Update the onex database
- `GET /api/onex/health` - Health check endpoint

## Tool Categories

- **Information Gathering**: Network reconnaissance and enumeration tools
- **Vulnerability Scanner**: Security assessment and vulnerability scanning
- **Exploitation Tools**: Penetration testing and exploitation frameworks
- **Wireless Testing**: WiFi security testing and wireless network analysis
- **Forensics Tools**: Digital forensics and incident response
- **Web Hacking**: Web application security testing
- **Stress Testing**: Load testing and DoS testing tools
- **Sniffing & Spoofing**: Network traffic analysis and manipulation
- **Password Attacks**: Password cracking and brute-force tools
- **Maintaining Access**: Post-exploitation and persistence tools

## Example Usage

### List all tools
```bash
curl http://localhost:3000/api/onex/tools
```

### Search for tools
```bash
curl http://localhost:3000/api/onex/search?q=nmap
```

### Install a tool
```bash
curl -X POST http://localhost:3000/api/onex/tools/nmap/install
```

### Check tool status
```bash
curl http://localhost:3000/api/onex/tools/nmap/status
```

## Development

### Start the service
```bash
npx nx serve onex-service
```

### Build the service
```bash
npx nx build onex-service
```

### Run tests
```bash
npx nx test onex-service
```

## Original Onex Features

This service preserves all original onex functionality:

- **CLI Mode**: Programmatic access to all CLI commands
- **Package Management**: Support for multiple package managers (apt, yum, pkg, etc.)
- **Installation Methods**: Git clone, curl, wget, and package manager installations
- **Dependency Management**: Automatic dependency resolution and installation
- **Multi-Platform**: Support for Linux, Termux, and other Unix-like systems

## Security Notice

⚠️ **Important**: This tool is designed for educational purposes, ethical hacking, and authorized security testing only. Users are responsible for complying with applicable laws and regulations. Always obtain proper authorization before using these tools on systems you do not own.

## License

This project maintains the original Onex license and adds modern API capabilities.

## Architecture Integration

This service is part of the larger Mental Prosthetic Platform and integrates with:
- **Jane Orchestrator**: Main backend coordination
- **Security Service**: Broader security tooling ecosystem  
- **Jane UI**: Frontend interface for tool management