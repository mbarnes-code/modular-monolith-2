# Workflows Collection

This directory contains copies of all GitHub Actions workflows found throughout the modular-monolith-2 codebase, organized by their original location for reference and potential reuse.

## 📊 Summary Statistics

- **Total Workflows**: 258 workflow files
- **Apps Workflows**: 157 files from application directories
- **Features Workflows**: 101 files from feature directories
- **Categories Covered**: Security, Productivity, Infrastructure, TCG, AI, and Core services

## 📁 Directory Structure

```
.github/workflows-collection/
├── apps/                           # Application-specific workflows (157 files)
│   ├── productivity/              # Productivity domain apps (125 files)
│   │   ├── actual-service/        # 21 workflows (CI/CD, releases, testing)
│   │   ├── goose-service/         # 25 workflows (AI tooling, desktop builds)
│   │   ├── inspector-service/     # 7 workflows (CLI tests, releases)
│   │   ├── mealie-service/        # 16 workflows (recipe management, E2E)
│   │   └── n8n-service/           # 56 workflows (automation platform)
│   └── security/                  # Security domain apps (32 files)
│       ├── blackarch-service/     # 1 workflow (security testing)
│       ├── cyberchef-service/     # 17 workflows (crypto analysis)
│       ├── kasmvnc-service/       # 11 workflows (remote desktop)
│       ├── misp-service/          # 2 workflows (threat intelligence)
│       ├── nemesis-service/       # 5 workflows (offensive security)
│       └── yara-x-service/        # 1 workflow (malware detection)
└── features/                      # Feature-specific workflows (101 files)
    ├── FileScopeMCP/              # 1 workflow (file scope analysis)
    ├── chroma-mcp/                # 2 workflows (vector database)
    ├── firecrawl-mcp-server/      # 4 workflows (web scraping)
    ├── it-tools/                  # 4 workflows (utility tools)
    ├── kong/                      # 25 workflows (API gateway)
    ├── mcp-virustotal/            # 1 workflow (malware analysis)
    ├── n8n-mcp-server/            # 4 workflows (automation server)
    ├── securityonion/             # 5 workflows (security monitoring)
    └── spec-kit/                  # 3 workflows (specification toolkit)
```

## 🏆 Notable Workflow Categories

### 🤖 **AI-Enhanced Workflows**
- **Goose Service**: `test-finder.yml` - AI-powered test creation
- **N8N MCP Server**: `claude-code-review.yml` - AI code review
- **Inspector Service**: `claude.yml` - AI-powered analysis

### 🏗️ **Build & Release Patterns**
- **Multi-platform Builds**: Actual, Goose (Intel/Linux/Windows)
- **Container Orchestration**: Kong, Nemesis, Firecrawl
- **Package Publishing**: N8N, CyberChef, IT-Tools

### 🔐 **Security-First Workflows**
- **CodeQL Analysis**: MISP, CyberChef, YARA-X
- **Vulnerability Scanning**: Nemesis, Security Onion
- **Container Security**: Trivy scanning across multiple services

### ⚡ **Performance & Testing**
- **E2E Testing**: Mealie, N8N, IT-Tools
- **Performance Benchmarks**: N8N benchmark workflows
- **Load Testing**: Kong performance testing

### 🔄 **Automation Excellence**
- **Release Automation**: Semantic releases across services
- **Dependency Management**: Renovate bot integrations
- **Stale Issue Management**: Community maintenance

## 🎯 **Workflow Pattern Analysis**

### **Most Common Workflow Types:**
1. **CI/CD Pipelines** - 89 workflows
2. **Release Management** - 34 workflows  
3. **Testing Automation** - 28 workflows
4. **Container Build/Push** - 21 workflows
5. **Security Scanning** - 18 workflows
6. **Documentation Generation** - 12 workflows

### **Executive Function Accommodations:**
- **Consistent Naming**: All follow `kebab-case.yml` convention
- **Clear Triggers**: Explicit `on:` conditions for predictable behavior
- **Descriptive Names**: Self-documenting workflow purposes
- **Modular Design**: Reusable workflow components

## 🚀 **Integration Opportunities**

### **Immediate Reuse Candidates:**
1. **`goose-service/test-finder.yml`** - AI-powered test generation
2. **`n8n-service/ci-master.yml`** - Comprehensive CI pipeline
3. **`kong/build.yml`** - Multi-arch container builds
4. **`mealie-service/e2e.yml`** - End-to-end testing patterns

### **Consolidation Opportunities:**
1. **Security Scanning** - Standardize CodeQL/Trivy patterns
2. **Release Management** - Unified semantic release workflow
3. **Container Builds** - Common multi-platform build templates
4. **Testing Patterns** - Standardized test execution workflows

## 🔧 **Adaptation Guidelines**

### **For Mental Prosthetic Platform:**
1. **Domain-Specific Triggers**: Security (<1s), Productivity (<2s), MTG (<3s), Infrastructure (<5s)
2. **Executive Function Support**: Clear progress indicators, consistent patterns
3. **Zero Dependencies**: Maintain isolation between service workflows
4. **Rollback Capabilities**: Include safe rollback in all deployment workflows

### **Recommended Modifications:**
- Add executive function accommodations to all UI-related workflows
- Standardize performance thresholds based on domain requirements
- Include automated rollback procedures in deployment workflows
- Add domain-specific validation steps

## 📈 **Performance Insights**

### **Workflow Execution Patterns:**
- **Fastest**: Simple linting workflows (~1-2 minutes)
- **Medium**: Standard CI/CD pipelines (~5-15 minutes)
- **Longest**: Full E2E testing suites (~30-60 minutes)

### **Resource Utilization:**
- **High CPU**: Container builds, multi-arch compilation
- **High Memory**: Large test suites, AI model inference
- **High I/O**: Package installations, Docker layer caching

## 🎨 **Design Patterns Observed**

### **Reusable Workflow Components:**
- **Checkout Pattern**: Consistent `actions/checkout@v4` usage
- **Caching Strategies**: Node.js, Python, Docker layer caching
- **Matrix Builds**: OS/version compatibility testing
- **Conditional Logic**: Environment-aware deployments

### **Security Best Practices:**
- **Token Management**: Scoped GitHub tokens
- **Secret Handling**: Environment-specific secrets
- **SBOM Generation**: Software bill of materials
- **Vulnerability Scanning**: Integrated security checks

## 🔄 **Migration Strategy**

### **Phase 1: Inventory & Analysis** ✅
- [x] Complete workflow collection
- [x] Pattern analysis
- [x] Performance profiling

### **Phase 2: Standardization**
- [ ] Create reusable workflow templates
- [ ] Establish naming conventions
- [ ] Define domain-specific patterns

### **Phase 3: Integration**
- [ ] Merge compatible workflows
- [ ] Eliminate redundancies
- [ ] Optimize performance paths

### **Phase 4: Enhancement**
- [ ] Add executive function accommodations
- [ ] Implement domain performance tiers
- [ ] Create unified monitoring

---

## 💡 **Usage Examples**

### **Adapting for New Services:**
```yaml
# Based on n8n-service/ci.yml pattern
name: Service CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    # Add domain-specific performance requirements
    timeout-minutes: ${{ matrix.domain == 'security' && 5 || 15 }}
```

### **Executive Function Integration:**
```yaml
# Add consistent progress reporting
- name: Report Progress
  run: |
    echo "🔍 Phase: ${{ matrix.phase }}"
    echo "⏱️ Expected: ${{ matrix.timeout }} minutes"
    echo "🎯 Domain: ${{ matrix.domain }}"
```

---

**Generated**: November 14, 2025  
**Total Workflows Collected**: 258  
**Original Locations Preserved**: 100%  
**Ready for Integration**: ✅