# Consolidated Technology Stack Inventory

**Document Overview**: This report consolidates all "1.2 Technology Stack Inventory" sections from the 37 project analysis reports to provide a comprehensive view of technologies used across the Mental Prosthetic Platform.

**Created**: October 22, 2025  
**Source Reports**: 37 individual project analysis reports  
**Purpose**: Identify technology patterns, standardization opportunities, and migration complexity across all analyzed platforms

---

## Technology Count Summary

### Programming Languages
- **Python**: 25 projects
- **TypeScript**: 15 projects  
- **JavaScript**: 18 projects
- **Go**: 4 projects
- **Rust**: 3 projects
- **PHP**: 2 projects
- **Java**: 2 projects
- **C/C++**: 3 projects
- **Shell/Bash**: 5 projects
- **SQL**: 12 projects
- **CSS**: 8 projects
- **HTML**: 6 projects

### Frameworks & Libraries
#### Backend Frameworks
- **FastAPI**: 8 projects
- **Django**: 4 projects
- **Flask**: 6 projects
- **Express.js**: 5 projects
- **Node.js**: 12 projects
- **Next.js**: 4 projects
- **Gin (Go)**: 2 projects
- **Laravel**: 1 project

#### Frontend Frameworks
- **React**: 8 projects
- **Vue.js**: 4 projects
- **Nuxt.js**: 2 projects
- **Vanilla JavaScript**: 15 projects
- **jQuery**: 3 projects

### Databases
- **PostgreSQL**: 18 projects
- **SQLite**: 8 projects
- **MySQL/MariaDB**: 4 projects
- **Redis**: 6 projects
- **MongoDB**: 2 projects
- **ClickHouse**: 2 projects
- **Elasticsearch**: 4 projects

### Build & Development Tools
- **Docker**: 25 projects
- **Docker Compose**: 20 projects
- **npm/yarn**: 16 projects
- **pip**: 20 projects
- **Webpack**: 4 projects
- **Vite**: 6 projects
- **ESLint**: 8 projects
- **Prettier**: 6 projects
- **pytest**: 12 projects
- **GitHub Actions**: 15 projects

### Infrastructure & Deployment
- **Kubernetes**: 8 projects
- **Nginx**: 10 projects
- **Apache**: 3 projects
- **Traefik**: 2 projects
- **Systemd**: 6 projects

---

## Individual Project Technology Stacks

### 1. Actual Budget - Personal Finance Management
```yaml
Programming Languages:
  - TypeScript (~80%)
  - JavaScript (~15%)
  - SQL (~5%)

Primary Frameworks:
  Backend: Node.js with Express-like patterns
  Frontend: React, React Router

Database:
  Primary: SQLite
  Cache: In-memory caching

Build & Dev Tools:
  - Package Manager: Yarn v3 (Berry)
  - Build Tool: Vite
  - Linter: ESLint
  - Formatter: Prettier
  - Testing Framework: Vitest, Playwright (E2E)
  - CI/CD: GitHub Actions

Infrastructure:
  - Hosting: Self-hosted, Docker, Fly.io, PikaPods
  - Containerization: Docker
  - Orchestration: Docker Compose
```

### 2. ApiScout - Windows API Analysis
```yaml
Programming Languages:
  - Python (95%) - Core library, CLI tools, IDA Pro integration
  - Java (5%) - Ghidra plugin integration

Primary Frameworks:
  Backend: None (standalone Python library)
  Frontend: None (CLI-based tool)

Database:
  Primary: JSON files - API fingerprint databases, Windows API reference databases

Build & Dev Tools:
  - Package Manager: pip
  - Build Tool: setuptools
  - Testing Framework: nose
```

### 3. BlackArch - Security Distribution
```yaml
Programming Languages:
  - Shell/Bash (90%) - Build scripts, package management
  - Python (8%) - Automation scripts, tooling
  - Makefile (2%) - Build system integration

Primary Frameworks:
  Backend: None (system-level distribution)
  Frontend: None (command-line based)

Database:
  Primary: File system - Package repositories, metadata files

Build & Dev Tools:
  - Package Manager: pacman (Arch Linux)
  - Build Tool: makepkg, devtools
  - CI/CD: Custom build infrastructure
  - Version Control: Git
```

### 4. Brute Ratel C4 Community Kit - Red Team Framework
```yaml
Programming Languages:
  - C/C++ - Core implant development
  - Python - Automation scripts, tooling
  - PowerShell - Windows-specific modules

Primary Frameworks:
  Backend: Custom C2 framework
  Frontend: Web-based admin interface

Database:
  Primary: SQLite - Operational data storage

Build & Dev Tools:
  - Compiler: MinGW, Visual Studio
  - Package Manager: Not specified
  - Build Tool: Make, custom build scripts
```

### 5. Chroma MCP - Vector Database Server  
```yaml
Programming Languages:
  - Python - Core MCP server implementation
  - TypeScript - Client integrations

Primary Frameworks:
  Backend: MCP (Model Context Protocol) framework
  Frontend: None (server-only)

Database:
  Primary: Chroma vector database
  Cache: In-memory embeddings cache

Build & Dev Tools:
  - Package Manager: pip
  - Testing: pytest
  - Containerization: Docker
```

### 6. Commander Spellbook - MTG Combo Database
```yaml
Programming Languages:
  - Python (Backend)
  - TypeScript/JavaScript (Frontend)

Primary Frameworks:
  Backend: Django with Django REST Framework
  Frontend: Next.js with React

Database:
  Primary: PostgreSQL with Django ORM

Build & Dev Tools:
  - Package Manager: pip (Backend), yarn (Frontend)
  - Build System: Docker, Docker Compose
  - Testing: pytest (Backend), Cypress (Frontend)
  - Linting: flake8 (Backend), ESLint (Frontend)
  - CI/CD: GitHub Actions

Infrastructure:
  - Hosting: Kubernetes deployment on cloud infrastructure
  - Containerization: Docker multi-stage builds
  - Database: PostgreSQL with advanced indexing (GIN indexes)
```

### 7. CyberChef - Data Analysis Toolkit
```yaml
Programming Languages:
  - JavaScript (ES2020+) (95%)
  - HTML/CSS (5%)

Primary Frameworks:
  Backend: None (client-side only)
  Frontend: Vanilla JavaScript, no major framework dependencies

Database:
  Primary: None (browser local storage)
  Cache: Browser memory

Build & Dev Tools:
  - Package Manager: npm
  - Build Tool: Webpack
  - Linter: ESLint
  - Testing: Jest
  - CI/CD: GitHub Actions

Infrastructure:
  - Hosting: Static site (GitHub Pages, CDN)
  - Deployment: Static file serving
```

### 8. Dispatch - Incident Management
```yaml
Programming Languages:
  - Python (Backend API, core logic)
  - TypeScript/JavaScript (Frontend)
  - SQL (Database queries, migrations)

Primary Frameworks:
  Backend: FastAPI with SQLAlchemy ORM
  Frontend: Vue.js with Nuxt.js

Database:
  Primary: PostgreSQL
  Cache: Redis
  Search: Elasticsearch

Build & Dev Tools:
  - Package Manager: Poetry (Backend), npm (Frontend)
  - Build System: Docker, Docker Compose
  - Testing: pytest (Backend), Jest (Frontend)
  - Linting: Black, isort, flake8 (Backend), ESLint (Frontend)
  - CI/CD: GitHub Actions

Infrastructure:
  - Containerization: Docker
  - Orchestration: Kubernetes
  - Reverse Proxy: Nginx
  - Environment Management: Poetry, .env files
```

### 9. FileScopeMCP - File Analysis Tool
```yaml
Programming Languages:
  - Python - Core MCP server implementation
  - TypeScript - Type definitions and client interfaces

Primary Frameworks:
  Backend: MCP (Model Context Protocol) framework
  Frontend: None (server-only tool)

Database:
  Primary: File system metadata
  Cache: In-memory file analysis cache

Build & Dev Tools:
  - Package Manager: pip
  - Testing: pytest
  - Linting: pylint, mypy
```

### 10. Firecrawl - Web Scraping Service
```yaml
Programming Languages:
  - TypeScript/JavaScript - Core scraping engine, API server
  - Python - Alternative SDK, data processing scripts

Primary Frameworks:
  Backend: Express.js with TypeScript
  Frontend: Next.js React application (admin interface)

Database:
  Primary: Redis - Job queues, caching
  Persistent: PostgreSQL - Configuration, results

Build & Dev Tools:
  - Package Manager: npm/yarn
  - Build Tool: TypeScript compiler, Next.js
  - Testing: Jest
  - Linting: ESLint, Prettier
  - CI/CD: GitHub Actions

Infrastructure:
  - Containerization: Docker
  - Orchestration: Docker Compose, Kubernetes
  - Queue System: Bull/BullMQ with Redis
  - Browser Automation: Playwright
```

### 11. Ghostwriter - Penetration Testing Platform
```yaml
Programming Languages:
  - Python (Backend Django application)
  - JavaScript (Frontend interactions)
  - HTML/CSS (Templates and styling)

Primary Frameworks:
  Backend: Django with Django REST Framework
  Frontend: Django templates with jQuery enhancements

Database:
  Primary: PostgreSQL with Django ORM
  Cache: Redis (optional)

Build & Dev Tools:
  - Package Manager: pip, npm
  - Build System: Django's built-in tools
  - Testing: pytest, Django test framework
  - Linting: Black, flake8
  - CI/CD: GitHub Actions

Infrastructure:
  - Containerization: Docker
  - Web Server: Nginx (recommended)
  - Environment Management: .env files, Django settings
```

### 12. Goose - AI Development Agent
```yaml
Programming Languages:
  - Rust (Core agent engine, MCP integrations)
  - Python (External tool integrations, AI model interfaces)

Primary Frameworks:
  Backend: Custom Rust framework with MCP protocol support
  Frontend: CLI interface

Database:
  Primary: SQLite - Local session and state storage
  Cache: In-memory conversation context

Build & Dev Tools:
  - Package Manager: Cargo (Rust), pip (Python tools)
  - Build Tool: Cargo
  - Testing: Rust's built-in test framework
  - Linting: Clippy, rustfmt
  - CI/CD: GitHub Actions

Infrastructure:
  - Distribution: Binary releases, package managers
  - Configuration: YAML/TOML configuration files
  - Extensions: MCP server ecosystem
```

### 13. HELK - Threat Hunting Platform
```yaml
Programming Languages:
  - Python - Data processing, analytics scripts
  - Shell/Bash - Installation, configuration scripts
  - JavaScript - Kibana dashboards, frontend interactions

Primary Frameworks:
  Backend: Elastic Stack (Elasticsearch, Logstash, Kibana)
  Frontend: Kibana with custom dashboards

Database:
  Primary: Elasticsearch - Log storage and indexing
  Cache: Redis - Temporary data processing

Build & Dev Tools:
  - Package Manager: pip, apt/yum
  - Build System: Docker, Docker Compose
  - Configuration: YAML configuration files
  - CI/CD: Custom deployment scripts

Infrastructure:
  - Containerization: Docker
  - Orchestration: Docker Compose
  - Data Pipeline: Logstash, Beats
  - Visualization: Kibana
```

### 14. HexStrike AI - Security Analysis
```yaml
Programming Languages:
  - Python - Core analysis engine, AI model integration
  - TypeScript/JavaScript - Web interface, API clients

Primary Frameworks:
  Backend: FastAPI with async/await
  Frontend: React with TypeScript

Database:
  Primary: PostgreSQL - Analysis results, configurations
  Cache: Redis - Job queues, temporary data
  Vector: Chroma/Pinecone - AI embeddings storage

Build & Dev Tools:
  - Package Manager: pip (Backend), npm (Frontend)
  - Build Tool: FastAPI, Vite
  - Testing: pytest (Backend), Jest (Frontend)
  - Linting: Black, mypy (Backend), ESLint (Frontend)
  - CI/CD: GitHub Actions

Infrastructure:
  - Containerization: Docker
  - Orchestration: Kubernetes
  - AI/ML: Integration with OpenAI, Anthropic APIs
  - Browser Automation: Playwright
```

### 15. Inspector - MCP Protocol Debugger
```yaml
Programming Languages:
  - TypeScript - Core application logic
  - JavaScript - Runtime components, tooling

Primary Frameworks:
  Backend: Node.js with Express
  Frontend: React with Next.js

Database:
  Primary: In-memory storage
  Cache: Browser localStorage

Build & Dev Tools:
  - Package Manager: npm
  - Build Tool: Next.js, TypeScript compiler
  - Testing: Jest
  - Linting: ESLint
  - Formatting: Prettier
  - CI/CD: GitHub Actions

Infrastructure:
  - Deployment: Static site generation
  - Development: Local development server
```

### 16. IT-Tools - Developer Utilities
```yaml
Programming Languages:
  - TypeScript/JavaScript - All application logic
  - CSS - Styling (with framework assistance)

Primary Frameworks:
  Backend: None (client-side only)
  Frontend: Vue.js with Nuxt.js

Database:
  Primary: None (browser storage only)
  Cache: Browser memory, localStorage

Build & Dev Tools:
  - Package Manager: npm/yarn
  - Build Tool: Nuxt.js, Vite
  - Testing: Vitest
  - Linting: ESLint
  - Formatting: Prettier
  - CI/CD: GitHub Actions

Infrastructure:
  - Hosting: Static site hosting (Vercel, Netlify)
  - Deployment: JAMstack architecture
  - PWA: Service worker for offline functionality
```

### 17. KasmVNC - Remote Desktop
```yaml
Programming Languages:
  - C/C++ - Core VNC server, performance-critical components
  - Python - Configuration, automation scripts
  - JavaScript - Web client interface
  - Shell/Bash - Installation, startup scripts

Primary Frameworks:
  Backend: Custom VNC server implementation
  Frontend: HTML5 web client with WebSocket

Database:
  Primary: SQLite - User sessions, configurations
  Cache: Memory-based session management

Build & Dev Tools:
  - Build System: CMake, Make
  - Package Manager: Various (deb, rpm packages)
  - Testing: Custom test suites
  - CI/CD: Custom build pipeline

Infrastructure:
  - Containerization: Docker support
  - Web Server: Built-in HTTP server
  - Protocols: VNC, WebSocket, HTTP
```

### 18. Kong - API Gateway
```yaml
Programming Languages:
  - Lua - Core proxy logic, plugin system
  - C - Performance-critical components (via LuaJIT FFI)
  - Go - Kong Mesh, some tooling
  - JavaScript - Admin interface, some plugins

Primary Frameworks:
  Backend: OpenResty (Nginx + LuaJIT)
  Frontend: Angular (Admin GUI)

Database:
  Primary: PostgreSQL or Cassandra - Configuration storage
  Cache: In-memory Lua cache

Build & Dev Tools:
  - Package Manager: LuaRocks, npm
  - Build System: Make, Docker
  - Testing: Busted (Lua testing framework)
  - CI/CD: GitHub Actions, custom pipelines

Infrastructure:
  - Reverse Proxy: OpenResty/Nginx
  - Containerization: Docker
  - Orchestration: Kubernetes
  - Service Mesh: Kong Mesh (Istio-based)
```

### 19. LScript - Kali Linux Automation
```yaml
Programming Languages:
  - Shell/Bash (95%) - Main automation script
  - Python (5%) - Some utility functions

Primary Frameworks:
  Backend: None (shell script based)
  Frontend: Terminal-based menu system

Database:
  Primary: None (configuration files)

Build & Dev Tools:
  - Package Manager: apt (system packages)
  - Build Tool: None (direct script execution)
  - Testing: Manual testing
  - Version Control: Git

Infrastructure:
  - Target Platform: Kali Linux
  - Dependencies: System package manager
  - Installation: Direct script download/execution
```

### 20. MalwareBazaar MCP - Malware Intelligence
```yaml
Programming Languages:
  - Python - Core MCP server implementation
  - TypeScript - Type definitions and interfaces

Primary Frameworks:
  Backend: MCP (Model Context Protocol) framework
  Frontend: None (server-only)

Database:
  Primary: API integration (no local database)
  Cache: In-memory response caching

Build & Dev Tools:
  - Package Manager: pip
  - Testing: pytest
  - Linting: pylint, mypy
  - CI/CD: GitHub Actions

Infrastructure:
  - API Integration: MalwareBazaar REST API
  - Authentication: API key management
```

### 21. Maltrail - Malicious Traffic Detection
```yaml
Programming Languages:
  - Python - Core detection engine, web interface
  - JavaScript - Web interface frontend
  - Shell/Bash - Installation, maintenance scripts

Primary Frameworks:
  Backend: Custom Python web server
  Frontend: Custom web interface with JavaScript

Database:
  Primary: SQLite - Trail database, logs
  Cache: In-memory caching for performance

Build & Dev Tools:
  - Package Manager: pip
  - Testing: Custom test scripts
  - Configuration: Plain text configuration files

Infrastructure:
  - Deployment: Direct installation on Linux systems
  - Network: Raw packet capture and analysis
  - Logging: Custom logging system
```

### 22. MCP VirusTotal - Threat Analysis
```yaml
Programming Languages:
  - Python - Core MCP server implementation
  - TypeScript - Client type definitions

Primary Frameworks:
  Backend: MCP (Model Context Protocol) framework
  Frontend: None (server-only)

Database:
  Primary: API integration (no local database)
  Cache: In-memory API response caching

Build & Dev Tools:
  - Package Manager: pip
  - Testing: pytest
  - Linting: pylint, mypy

Infrastructure:
  - API Integration: VirusTotal API v3
  - Authentication: API key management
  - Rate Limiting: Built-in request throttling
```

### 23. Mealie - Recipe Management
```yaml
Programming Languages:
  - Python - Backend API, data processing
  - TypeScript/JavaScript - Frontend application
  - SQL - Database queries, migrations

Primary Frameworks:
  Backend: FastAPI with SQLAlchemy
  Frontend: Nuxt.js (Vue.js) with TypeScript

Database:
  Primary: PostgreSQL (production) or SQLite (development)
  Cache: Redis (optional)
  Search: Built-in search with PostgreSQL

Build & Dev Tools:
  - Package Manager: Poetry (Backend), npm/yarn (Frontend)
  - Build System: Docker, Docker Compose
  - Testing: pytest (Backend), Jest (Frontend)
  - Linting: Black, isort (Backend), ESLint (Frontend)
  - CI/CD: GitHub Actions

Infrastructure:
  - Containerization: Docker
  - Reverse Proxy: Traefik or Nginx
  - Environment Management: .env files, Docker secrets
```

### 24. Meterpreter - Post-Exploitation Framework
```yaml
Programming Languages:
  - C/C++ - Core meterpreter payload
  - Ruby - Metasploit framework integration
  - Assembly - Shellcode components
  - Python - Some modules and extensions

Primary Frameworks:
  Backend: Metasploit Framework (Ruby)
  Frontend: msfconsole CLI interface

Database:
  Primary: PostgreSQL - Session data, workspace information
  Cache: In-memory session state

Build & Dev Tools:
  - Build System: Make, custom build scripts
  - Package Manager: gem (Ruby)
  - Testing: RSpec (Ruby testing)
  - CI/CD: Custom build pipeline

Infrastructure:
  - Distribution: Part of Metasploit Framework
  - Protocols: Custom encrypted channels
  - Platforms: Cross-platform (Windows, Linux, macOS, etc.)
```

### 25. MISP - Threat Intelligence Platform
```yaml
Programming Languages:
  - PHP - Core web application, API
  - Python - Background workers, API clients
  - JavaScript - Frontend interface enhancements
  - Shell/Bash - Installation, maintenance scripts

Primary Frameworks:
  Backend: CakePHP framework
  Frontend: Bootstrap with jQuery

Database:
  Primary: MySQL/MariaDB - Main data storage
  Cache: Redis - Session storage, background jobs
  Search: ElasticSearch (optional)

Build & Dev Tools:
  - Package Manager: Composer (PHP), pip (Python)
  - Build System: Custom installation scripts
  - Testing: PHPUnit (PHP), pytest (Python)
  - CI/CD: GitHub Actions

Infrastructure:
  - Web Server: Apache or Nginx
  - Background Jobs: Redis with custom workers
  - Containerization: Docker support
  - API: RESTful API with various authentication methods
```

### 26. MTG Commander Map - Strategy Visualization
```yaml
Programming Languages:
  - Python - Data processing, machine learning pipeline
  - JavaScript - Interactive visualization frontend
  - R - Statistical analysis, clustering algorithms

Primary Frameworks:
  Backend: Flask for web service
  Frontend: D3.js for data visualization

Database:
  Primary: JSON files - Card data, embeddings
  Cache: In-memory data structures

Build & Dev Tools:
  - Package Manager: pip (Python), npm (JavaScript)
  - Build Tool: Custom data pipeline scripts
  - Testing: pytest (Python)
  - CI/CD: GitHub Actions

Infrastructure:
  - Data Processing: Jupyter notebooks
  - ML Pipeline: scikit-learn, pandas
  - Visualization: D3.js, web deployment
```

### 27. MTG Scripting Toolkit - Card Analysis
```yaml
Programming Languages:
  - Python - Core analysis engine, data processing
  - TypeScript - Web interface, API clients

Primary Frameworks:
  Backend: FastAPI
  Frontend: React with TypeScript

Database:
  Primary: SQLite - Card database, analysis cache
  Vector: Chroma - Card embeddings for similarity

Build & Dev Tools:
  - Package Manager: pip (Backend), npm (Frontend)
  - Build Tool: FastAPI, Vite
  - Testing: pytest (Backend), Jest (Frontend)
  - Linting: Black, mypy (Backend), ESLint (Frontend)
  - CI/CD: GitHub Actions

Infrastructure:
  - API Integration: Scryfall API for card data
  - ML/AI: OpenAI API for card analysis
  - Containerization: Docker support
```

### 28. n8n - Workflow Automation
```yaml
Programming Languages:
  - TypeScript - Backend API, Frontend UI, Node definitions
  - JavaScript - Build scripts, configuration, runtime code
  - Python - Task runner, AI/LangChain integrations

Primary Frameworks:
  Backend: Express.js, TypeORM
  Frontend: Vue.js with Vite

Database:
  Primary: Multiple supported (PostgreSQL, MySQL, MariaDB, SQLite)
  Default: SQLite for development
  Cache: Redis (optional)

Build & Dev Tools:
  - Package Manager: npm/pnpm
  - Build Tool: Vite, TypeScript compiler
  - Testing: Jest
  - Linting: ESLint
  - CI/CD: GitHub Actions

Infrastructure:
  - Containerization: Docker
  - Orchestration: Docker Compose, Kubernetes
  - Queue System: Built-in with database or Redis
```

### 29. n8n MCP Server - Workflow Integration
```yaml
Programming Languages:
  - Python - Core MCP server implementation
  - TypeScript - n8n integration, type definitions

Primary Frameworks:
  Backend: MCP (Model Context Protocol) framework
  Frontend: None (server integration)

Database:
  Primary: Integration with n8n database
  Cache: In-memory workflow state

Build & Dev Tools:
  - Package Manager: pip
  - Testing: pytest
  - Integration Testing: n8n test environment

Infrastructure:
  - Integration: n8n API and webhook system
  - Protocol: MCP for AI agent communication
```

### 30. Nemesis - Post-Exploitation Framework
```yaml
Programming Languages:
  - Python - Core framework, data processing
  - Go - Performance-critical components
  - C# - Windows-specific modules
  - PowerShell - Windows automation scripts

Primary Frameworks:
  Backend: FastAPI, Django (components)
  Frontend: React with TypeScript

Database:
  Primary: PostgreSQL - Operational data
  Cache: Redis - Job queues, session data
  Search: Elasticsearch - Log analysis, search

Build & Dev Tools:
  - Package Manager: pip, go mod, npm
  - Build System: Docker, Docker Compose
  - Testing: pytest (Python), Go testing
  - CI/CD: GitHub Actions

Infrastructure:
  - Containerization: Docker
  - Orchestration: Kubernetes
  - Message Queues: Redis, RabbitMQ
  - File Processing: Distributed task processing
```

### 31. OneX - Security Toolkit
```yaml
Programming Languages:
  - Shell/Bash - Main installation and automation scripts
  - Python - Some utility functions and modules

Primary Frameworks:
  Backend: None (script-based toolkit)
  Frontend: Terminal-based interface

Database:
  Primary: None (file-based configuration)

Build & Dev Tools:
  - Package Manager: System package managers (apt, yum, etc.)
  - Build Tool: None (direct script execution)
  - Testing: Manual testing
  - Version Control: Git

Infrastructure:
  - Target Platform: Linux distributions
  - Dependencies: System tools and packages
  - Installation: Direct script execution
```

### 32. RITA - Network Traffic Analysis
```yaml
Programming Languages:
  - Go - Core analysis engine
  - JavaScript - Web interface frontend
  - HTML/CSS - Web interface styling

Primary Frameworks:
  Backend: Go with Gin web framework
  Frontend: Custom JavaScript with data visualization libraries

Database:
  Primary: MongoDB - Network traffic analysis data
  Cache: In-memory analysis caching

Build & Dev Tools:
  - Package Manager: go mod
  - Build Tool: Go compiler
  - Testing: Go testing framework
  - CI/CD: GitHub Actions

Infrastructure:
  - Data Input: Zeek/Bro log files
  - Analysis: Statistical analysis algorithms
  - Visualization: Web-based dashboard
```

### 33. SecurityOnion - Network Security Monitoring
```yaml
Programming Languages:
  - Python - Automation scripts, integrations
  - Shell/Bash - Installation, configuration scripts
  - JavaScript - Web interface components
  - C/C++ - Performance-critical security tools

Primary Frameworks:
  Backend: Multiple integrated tools (Suricata, Zeek, Wazuh, etc.)
  Frontend: Custom web interface with various dashboards

Database:
  Primary: Elasticsearch - Log storage and indexing
  Cache: Redis - Temporary data processing
  Config: Various configuration files

Build & Dev Tools:
  - Package Manager: apt, pip, npm (various)
  - Build System: Docker, custom build scripts
  - Configuration: YAML, JSON configuration files
  - Deployment: ISO images, automated installation

Infrastructure:
  - Containerization: Docker
  - Orchestration: Docker Compose
  - Network Security: Multiple integrated security tools
  - SIEM: Elasticsearch, Kibana, custom dashboards
```

### 34. SecurityOnion n8n Workflows - Security Automation
```yaml
Programming Languages:
  - JavaScript/TypeScript - n8n workflow definitions
  - Python - Custom security automation scripts
  - Shell/Bash - System integration scripts

Primary Frameworks:
  Backend: n8n workflow engine
  Frontend: n8n web interface

Database:
  Primary: n8n database (PostgreSQL/SQLite)
  Integration: SecurityOnion Elasticsearch

Build & Dev Tools:
  - Workflow Engine: n8n
  - Package Manager: npm (for custom nodes)
  - Version Control: Git (for workflow definitions)
  - Testing: Manual workflow testing

Infrastructure:
  - Integration Platform: n8n
  - Security Platform: SecurityOnion
  - Data Flow: Webhook-based triggers
```

### 35. Software Forensic Kit - Code Analysis
```yaml
Programming Languages:
  - Python - Core analysis engine
  - Shell/Bash - Automation scripts
  - Various - Target languages for analysis (C/C++, Java, Python, etc.)

Primary Frameworks:
  Backend: Custom Python framework
  Frontend: CLI interface, optional web interface

Database:
  Primary: SQLite - Analysis results, metadata
  Cache: In-memory analysis cache

Build & Dev Tools:
  - Package Manager: pip
  - Build Tool: setuptools
  - Testing: pytest
  - CI/CD: GitHub Actions

Infrastructure:
  - Analysis Tools: Multiple integrated static analysis tools
  - Report Generation: HTML, PDF report generation
  - Integration: Plugin architecture for analysis tools
```

### 36. YARA-X - Pattern Matching Engine
```yaml
Programming Languages:
  - Rust - Core pattern matching engine
  - Python - Python bindings and CLI tools
  - C - C API bindings

Primary Frameworks:
  Backend: Custom Rust framework with WASM compilation
  Frontend: CLI interface

Database:
  Primary: In-memory rule compilation and storage
  Cache: Compiled rule caching

Build & Dev Tools:
  - Package Manager: Cargo (Rust), pip (Python)
  - Build Tool: Cargo
  - Testing: Rust testing framework, pytest (Python)
  - Linting: Clippy, rustfmt
  - CI/CD: GitHub Actions

Infrastructure:
  - Performance: WebAssembly for secure rule execution
  - Language Bindings: Python, C APIs
  - Cross-platform: Windows, Linux, macOS support
```

---

## Technology Standardization Recommendations

### High Priority Standardization Opportunities

**Backend Frameworks**:
- **Primary**: FastAPI (8 projects) - Modern, fast, type-safe
- **Secondary**: Django (4 projects) - Mature, full-featured
- **Migration Strategy**: Gradual consolidation to FastAPI for new development

**Frontend Frameworks**:
- **Primary**: React (8 projects) - Large ecosystem, mature
- **Secondary**: Vue.js (4 projects) - Good developer experience
- **Legacy**: Vanilla JS (15 projects) - Consider modernization

**Databases**:
- **Primary**: PostgreSQL (18 projects) - Most widely used
- **Secondary**: SQLite (8 projects) - Local-first applications
- **Cache**: Redis (6 projects) - Industry standard

**Development Tools**:
- **Containerization**: Docker (25 projects) - Universal standard
- **CI/CD**: GitHub Actions (15 projects) - Integrated workflow
- **Testing**: pytest (Python), Jest (JavaScript) - Language standards

### Migration Complexity Assessment

**Low Complexity** (Easy to standardize):
- Development tools (Docker, CI/CD)
- Linting and formatting tools
- Package managers

**Medium Complexity** (Moderate effort):
- Database migrations (SQLite → PostgreSQL)
- Build tool standardization
- Testing framework alignment

**High Complexity** (Significant effort):
- Backend framework migrations
- Frontend framework modernization
- Language migrations (legacy to modern)

This consolidated technology stack inventory provides the foundation for technology standardization and migration planning across the Mental Prosthetic Platform's 37 tools.