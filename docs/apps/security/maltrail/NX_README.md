# Maltrail Service - NX Integration

This is the NX-integrated version of the Maltrail malicious traffic detection system.

## Overview

Maltrail is a malicious traffic detection system, utilizing publicly available (black)lists containing malicious and/or generally suspicious trails, along with static trails compiled from various AV reports and custom user defined lists.

## Project Structure

```
apps/maltrail-service/
├── core/                 # Core Maltrail functionality
├── plugins/              # Plugin system
├── trails/               # Trail definitions and feeds
├── html/                 # Web interface
├── docker/               # Docker configuration
├── tests/                # Test files
├── server.py             # Main server application
├── sensor.py             # Sensor application
├── maltrail.conf         # Configuration file
├── requirements.txt      # Python dependencies
└── project.json          # NX project configuration
```

## Available Commands

### Development
- `nx serve maltrail-service` - Start the Maltrail server
- `nx serve:sensor maltrail-service` - Start the Maltrail sensor
- `nx test maltrail-service` - Run tests
- `nx lint maltrail-service` - Run linting

### Deployment
- `nx build maltrail-service` - Build the service
- `nx docker:build maltrail-service` - Build Docker image
- `nx docker:run maltrail-service` - Run with Docker Compose
- `nx docker:stop maltrail-service` - Stop Docker containers

### Setup
- `nx install maltrail-service` - Install Python dependencies

## Configuration

The main configuration is in `maltrail.conf`. Key settings include:

- HTTP server settings
- Sensor configuration
- Trail sources and feeds
- Logging configuration

## Integration with Jane Platform

This service integrates with the Jane platform as part of the security domain, providing:

- Malicious traffic detection
- Real-time threat monitoring
- Web-based dashboard
- API endpoints for integration

## Original Documentation

For detailed Maltrail documentation, see the original README.md file in this directory.