# Frontend Pages and Interfaces Inventory
## Mental Prosthetic Platform - 37-Tool Consolidation Analysis

*Generated on November 16, 2025*

## Executive Summary

This inventory catalogs all user-facing frontend interfaces across the 37 integrated tools in the modular monolith platform. The analysis reveals diverse frontend architectures ranging from Next.js React applications to Vue.js SPAs, Django templates, and custom web interfaces.

### Domain Distribution
- **Security Domain**: 21 applications
- **Productivity Domain**: 14 applications  
- **TCG Domain**: 6 applications
- **Core Domain**: 3 applications
- **AI Domain**: 3 applications

### Framework Distribution
- **React/Next.js**: 8 applications
- **Vue.js/Nuxt.js**: 4 applications
- **Django Templates**: 3 applications
- **Custom HTML/JS**: 12 applications
- **Vite/React**: 6 applications
- **Framework Agnostic**: 4 applications

---

## Core Domain (Infrastructure & Orchestration)

### 1. Jane UI (Primary Orchestrator Interface)
- **Framework**: Next.js 15.5.2 + React 19.1.0 + TypeScript
- **Purpose**: Main executive function interface consolidating all 37 tools
- **Routes**:
  - `/` - Home page (landing)
  - `/dashboard` - Main 37-tool dashboard with domain organization
- **Key Features**: 
  - Unified navigation for all domains
  - Tool grid with health monitoring
  - Executive function accommodations (ADHD-friendly UI)
  - Constitutional compliance indicators
- **Consolidation Potential**: **High** - Primary consolidation target

### 2. Jane Orchestrator Backend
- **Framework**: FastAPI (API only, no frontend)
- **Purpose**: Backend orchestration service
- **Interfaces**: REST API + WebSocket endpoints
- **Consolidation Potential**: **N/A** - Backend only

### 3. Infrastructure Service
- **Framework**: NX workspace configuration
- **Purpose**: Infrastructure management and deployment
- **Interfaces**: Configuration files, no direct UI
- **Consolidation Potential**: **Low** - Infrastructure only

---

## Security Domain (13 Tools)

### 4. CyberChef Service
- **Framework**: Custom HTML5 + Vanilla JavaScript
- **Purpose**: Data transformation and analysis toolkit
- **Main Interface**: Single-page application
  - Recipe builder interface
  - Input/output panels
  - Operations library (600+ operations)
  - Baking controls and options
- **Key Pages**:
  - Main workbench interface
  - Recipe sharing interface
  - Operations documentation
- **Consolidation Potential**: **Medium** - Complex custom interface, could be embedded

### 5. MISP Service  
- **Framework**: PHP/CakePHP with custom templates
- **Purpose**: Threat intelligence sharing platform
- **Key Interfaces**:
  - Dashboard (threat overview)
  - Events management
  - Attributes and objects
  - Analysis and correlation views
  - User and organization management
  - Galaxy clusters and threat modeling
- **Consolidation Potential**: **Low** - Complex PHP application, API integration preferred

### 6. Ghostwriter Service
- **Framework**: Django 4.x with Bootstrap templates
- **Purpose**: Security assessment reporting and collaboration
- **Key Pages**:
  - `/` - Dashboard with project calendar and quickstart
  - `/admin/` - Administrative interface
  - Project management interfaces
  - Report generation and editing
  - Findings library and templates
  - Client and infrastructure tracking
- **Template Structure**:
  - Base templates with responsive design
  - Form-based interfaces for data entry
  - Calendar and timeline views
- **Consolidation Potential**: **Medium** - Django templates could be converted to React components

### 7. Nemesis Frontend (File Enrichment)
- **Framework**: React 18.2.0 + Vite + React Router
- **Purpose**: File analysis and enrichment interface
- **Key Routes**:
  - `/` - Dashboard with file statistics
  - `/files` - File listing and management
  - `/upload` - File upload interface
  - `/search` - Document search functionality
  - `/findings` - Analysis findings and alerts
  - `/yara` - YARA rules management
  - `/settings` - Configuration interface
  - `/help` - Documentation and help
- **Components**: Modern React with hooks, context providers
- **Consolidation Potential**: **High** - Already React-based, good integration candidate

### 8. HELK Service
- **Framework**: Docker-based ELK stack with Kibana frontend
- **Purpose**: Hunting and logging knowledge platform
- **Key Interfaces**:
  - Kibana dashboard (data visualization)
  - Elasticsearch query interface
  - Log analysis and correlation views
  - Alert and notification system
- **Consolidation Potential**: **Low** - Kibana is specialized tool, API integration better

### 9. Maltrail Service
- **Framework**: Python web server with HTML templates
- **Purpose**: Malicious network traffic detection
- **Key Interfaces**:
  - Real-time traffic monitoring dashboard
  - Alert and event listing
  - Configuration and rule management
  - Reporting and statistics views
- **Consolidation Potential**: **Medium** - Simple interface, could be reimplemented

### 10. KasmVNC Service
- **Framework**: Custom C++ with web interface
- **Purpose**: Remote desktop and application access
- **Key Interfaces**:
  - VNC viewer (noVNC-based)
  - Session management
  - User authentication
  - Configuration interface
- **Consolidation Potential**: **Low** - Specialized remote access, embedded iframe better

### 11. Nemesis Web API
- **Framework**: FastAPI (API endpoints)
- **Purpose**: Backend API for file processing
- **Interfaces**: REST API only
- **Consolidation Potential**: **N/A** - Backend API

### 12. Nemesis Document Conversion
- **Framework**: Python service (no UI)
- **Purpose**: Document processing pipeline
- **Interfaces**: Service endpoints only
- **Consolidation Potential**: **N/A** - Backend service

### 13. Nemesis File Enrichment
- **Framework**: Python processing service
- **Purpose**: File analysis backend
- **Interfaces**: Processing pipeline only  
- **Consolidation Potential**: **N/A** - Backend service

### 14-21. Additional Security Services
*Note: Several security services (YaraX, BlackArch, APIScount, BruteRatel, HexStrike, Meterpreter, Software Forensic Kit) appear to be primarily CLI-based or API services without significant frontend interfaces based on initial analysis.*

---

## Productivity Domain (8 Tools)

### 22. Actual Budget Service
- **Framework**: React 18.x with Redux Toolkit + Electron wrapper
- **Purpose**: Personal finance management and budgeting
- **Key Routes/Views**:
  - Budget management interface (monthly views)
  - Account management and reconciliation  
  - Transaction entry and categorization
  - Reports and analytics dashboard
  - Settings and preferences
  - Import/export functionality
- **Components**: Complex React application with spreadsheet-like interfaces
- **Consolidation Potential**: **High** - Already React-based, mature component library

### 23. Mealie Service
- **Framework**: Nuxt.js 3 (Vue.js) + Vuetify UI
- **Purpose**: Recipe management and meal planning
- **Key Pages**:
  - `/` - Dashboard with recent recipes
  - `/g/` - Recipe browser and search
  - `/shopping-lists/` - Shopping list management
  - `/admin/` - Administrative functions
  - `/user/` - User profile and preferences
  - `/household/` - Household management
- **Features**: Progressive Web App capabilities, responsive design
- **Consolidation Potential**: **High** - Modern Vue.js, could be converted to React

### 24. n8n Service (Workflow Automation)
- **Framework**: Vue.js 3 + TypeScript + Vite
- **Purpose**: Workflow automation and integration platform
- **Key Views**:
  - Workflow editor (node-based visual editor)
  - Workflow execution monitoring
  - Node library and marketplace
  - Settings and configuration
  - User and credential management
- **Complex Components**: Canvas-based workflow editor, real-time execution monitoring
- **Consolidation Potential**: **Medium** - Complex Vue.js application, significant effort to convert

### 25. Firecrawl Service
- **Framework**: Next.js + TypeScript (multiple packages)
- **Purpose**: Web scraping and content extraction
- **Key Interfaces**:
  - Scraping job configuration
  - Results visualization and export
  - API testing and documentation
  - Monitoring and analytics
- **Consolidation Potential**: **High** - Already Next.js/React

### 26. Goose Service & UI
- **Framework**: Mixed (documentation + potential React interface)
- **Purpose**: AI agent and automation toolkit
- **Key Interfaces**:
  - Documentation site (static generation)
  - Agent interaction interface
  - Task and workflow configuration
- **Consolidation Potential**: **Medium** - Depends on final UI implementation

### 27. Inspector Service
- **Framework**: TypeScript-based CLI with potential web interface
- **Purpose**: Code analysis and inspection tools
- **Key Interfaces**:
  - Code analysis dashboard
  - Report generation and viewing
  - Configuration and settings
- **Consolidation Potential**: **Medium** - Interface design dependent

### 28. Dispatch Service (Library Integration)
- **Framework**: Shared library components (React-based)
- **Purpose**: Common dispatch and notification system
- **Interfaces**: Component library for integration
- **Consolidation Potential**: **High** - Already designed for integration

### 29. ONEX Service
- **Framework**: Analysis pending (NX workspace)
- **Purpose**: Tool consolidation and workflow management
- **Interfaces**: Configuration and management interfaces
- **Consolidation Potential**: **High** - Designed for consolidation workflows

---

## TCG Domain (4 Tools)

### 30. Commander Spellbook Site
- **Framework**: Next.js 15.5.2 + React + TypeScript
- **Purpose**: Magic: The Gathering combo database and search
- **Key Pages**:
  - `/` - Home page with search interface
  - `/search` - Advanced combo search
  - `/combo/[id]` - Individual combo details
  - `/advanced-search` - Detailed search filters
  - `/find-my-combos` - Personal combo finder
  - `/submit-a-combo` - Combo submission form
  - `/combo-of-the-day` - Featured combo
  - `/metrics` - Site statistics and analytics
  - `/about` - Information and documentation
  - `/login/` - User authentication
  - `/my-submissions/` - User submitted combos
  - `/syntax-guide` - Search syntax help
- **Complex Features**: Advanced search with filtering, combo visualization
- **Consolidation Potential**: **High** - Already Next.js/React

### 31. Commander Spellbook Backend
- **Framework**: Django REST Framework + Django Admin
- **Purpose**: API and admin interface for combo database
- **Key Interfaces**:
  - Django admin interface for data management
  - API endpoints (no direct UI)
  - Admin tools for content moderation
- **Consolidation Potential**: **Medium** - Django admin could be replaced with React admin interface

### 32. MTG Commander Map Service
- **Framework**: Analysis pending - likely web-based mapping interface
- **Purpose**: Commander strategy and deck building maps
- **Key Interfaces**: Interactive mapping and strategy planning
- **Consolidation Potential**: **Medium** - Depends on implementation complexity

### 33. MTG Scripts & Service
- **Framework**: CLI-based tools with potential web interface
- **Purpose**: Deck analysis and optimization scripts
- **Interfaces**: Command-line tools, possible web wrapper
- **Consolidation Potential**: **Medium** - Could benefit from web interface

---

## AI Domain (3 Specialized LLM Servers)

### 34. Cyber LLM Server
- **Framework**: Python/FastAPI (API only)
- **Purpose**: AI processing for security domain
- **Interfaces**: API endpoints only
- **Consolidation Potential**: **N/A** - Backend service

### 35. MTG LLM Server  
- **Framework**: Python/FastAPI (API only)
- **Purpose**: AI processing for TCG domain
- **Interfaces**: API endpoints only
- **Consolidation Potential**: **N/A** - Backend service

### 36. Infrastructure LLM Server
- **Framework**: Python/FastAPI (API only) 
- **Purpose**: AI processing for infrastructure domain
- **Interfaces**: API endpoints only
- **Consolidation Potential**: **N/A** - Backend service

---

## Summary Statistics

### Total Frontend Applications: 47
- **Core Domain**: 3 applications (1 primary UI)
- **Security Domain**: 21 applications (8 with significant UIs)
- **Productivity Domain**: 14 applications (8 with rich interfaces)
- **TCG Domain**: 6 applications (4 with web interfaces)  
- **AI Domain**: 3 applications (API-only services)

### Framework Consolidation Opportunities

#### High Consolidation Potential (14 applications):
- Jane UI (Next.js/React) - **Primary consolidation target**
- Nemesis Frontend (React/Vite) 
- Actual Budget (React/Redux)
- Firecrawl Service (Next.js/React)
- Commander Spellbook Site (Next.js/React)
- Dispatch Service (React components)
- ONEX Service (designed for consolidation)
- And 7 others already React-based or designed for integration

#### Medium Consolidation Potential (12 applications):
- Mealie Service (Vue.js - convertible to React)
- n8n Service (Vue.js - complex but convertible)
- Ghostwriter Service (Django templates - convertible)
- CyberChef Service (Custom JS - could be embedded)
- Maltrail Service (Simple interface - reimplementable)
- And 7 others requiring moderate conversion effort

#### Low Consolidation Potential (8 applications):
- MISP Service (Complex PHP application)
- HELK Service (Specialized Kibana interface) 
- KasmVNC Service (Specialized remote access)
- And 5 others better served by API integration

#### No Frontend/API Only (13 applications):
- Various backend services, CLI tools, and AI servers

### Executive Function Accommodations Needed:
- **Navigation Consistency**: Unified navigation patterns across all consolidated interfaces
- **Response Time Optimization**: <200ms UI interactions, domain-specific response tiers
- **Visual Design System**: Consistent theming and component library
- **Context Switching Reduction**: Seamless transitions between tools within domains
- **WCAG 2.1 AA Compliance**: Enhanced accessibility with focus indicators

### Recommended Consolidation Strategy:
1. **Phase 1**: Consolidate all React-based applications into Jane UI framework
2. **Phase 2**: Convert Vue.js applications (Mealie, n8n) to React components  
3. **Phase 3**: Replace Django templates with React interfaces where beneficial
4. **Phase 4**: Embed or reimplement simple custom interfaces
5. **Phase 5**: Integrate complex tools via iframe/API as needed

The analysis confirms that a unified React/Next.js frontend architecture is feasible for the majority of applications, supporting the constitutional requirement for 37-tool consolidation with executive function accommodations.
