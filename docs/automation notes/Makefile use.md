# Makefile Usage in Apps Directory

This document catalogs all Makefiles found in the `/apps` directory and their usage patterns.

## Overview

Makefiles are used throughout the apps directory for various automation tasks including building, testing, documentation generation, and service-specific compilation tasks.

## Makefile Locations and Purposes

### Security Services

#### 1. Ghostwriter Service - Documentation Build

**Location:** `/apps/security/ghostwriter-service/DOCS/Makefile`

**Purpose:** Sphinx documentation generation

**Key Targets:**

- `help` - Show available targets
- `clean` - Remove build artifacts
- `html` - Generate HTML documentation
- `pdf` - Generate PDF documentation (via LaTeX)
- `linkcheck` - Validate external links

```bash
# Usage examples:
cd apps/security/ghostwriter-service/DOCS
make html          # Generate HTML docs
make clean         # Clean build directory
make linkcheck     # Check all external links
```

#### 2. APIScout Service - Python Package Management

**Location:** `/apps/security/apiscout-service/scripts/Makefile`

**Purpose:** Python development workflow automation

**Key Targets:**

- `init` - Install requirements
- `package` - Create distribution package
- `publish` - Upload to PyPI
- `pylint` - Run code quality checks
- `test` - Run unit tests
- `test-coverage` - Run tests with coverage report
- `clean` - Remove Python cache files

```bash
# Usage examples:
cd apps/security/apiscout-service/scripts
make init          # Setup development environment
make test-coverage # Run tests with coverage
make package       # Build distribution package
```

#### 3. Meterpreter Service - Native Compilation

**Location:** `/apps/security/meterpreter-service/Makefile`

**Purpose:** Cross-compilation of native libraries and binaries

**Key Features:**

- 32-bit x86 cross-compilation
- Custom CFLAGS for embedded systems
- OpenSSL and libpcap integration
- Bionic libc compilation

```bash
# Usage examples:
cd apps/security/meterpreter-service
make               # Build all targets
make clean         # Clean compiled objects
```

#### 4. Meterpreter Workspace - Multi-directory Build

**Location:** `/apps/security/meterpreter-service/workspace/Makefile`

**Purpose:** Coordinate builds across multiple subdirectories

**Subdirectories:**

- `common` - Shared components
- `metsrv` - Core meterpreter server
- `ext_server_stdapi` - Standard API extension
- `ext_server_sniffer` - Network sniffer extension
- `ext_server_networkpug` - Network plugin extension

```bash
# Usage examples:
cd apps/security/meterpreter-service/workspace
make subdirs       # Build all subdirectories
make clean         # Clean all subdirectories
```

#### 5. MISP Service - PHP Code Quality

**Location:** `/apps/security/misp-service/src/app/Makefile`

**Purpose:** PHP code style and quality checks

**Key Targets:**

- `check-style` - Run PHP CodeSniffer
- `check-cpd` - Run copy/paste detector
- `check-js` - Run JavaScript linting
- `check-all-ci` - Run all CI checks

```bash
# Usage examples:
cd apps/security/misp-service/src/app
make check-style   # Check PHP code style
make check-all-ci  # Run all quality checks
```

#### 6. Brute Ratel Service - BOF Compilation

**Location:** `/apps/security/brute-ratel-service/src/assets/bofs/Makefile`

**Purpose:** Compile Beacon Object Files (BOFs) for Windows

**Key Targets:**

- `samples` - Compile sample BOFs
- `contact_harvester` - Compile contact harvester BOF
- `shadowclone` - Compile shadowclone BOF
- `vainject` - Compile virtual allocation injection BOF

```bash
# Usage examples:
cd apps/security/brute-ratel-service/src/assets/bofs
make samples       # Compile all sample BOFs
make vainject      # Compile specific BOF
```

#### 7. KasmVNC Service - Internationalization

**Location:** `/apps/security/kasmvnc-service/src/kasmweb/po/Makefile`

**Purpose:** Translation and localization management

**Supported Languages:** cs, de, el, es, ja, ko, nl, pl, pt_BR, ru, sv, tr, zh_CN, zh_TW

**Key Targets:**

- `update-po` - Update translation files
- `update-js` - Generate JavaScript locale files
- `update-pot` - Update translation template

```bash
# Usage examples:
cd apps/security/kasmvnc-service/src/kasmweb/po
make update-pot    # Update translation template
make update-js     # Generate locale files
```

#### 8. KasmVNC Service - Icon Generation

**Location:** `/apps/security/kasmvnc-service/src/kasmweb/app/images/icons/Makefile`

**Purpose:** Generate application icons in multiple sizes

**Icon Sizes:** 16x16, 24x24, 32x32, 48x48, 64x64, 72x72, 96x96, 120x120, 144x144, 152x152, 192x192

**Key Features:**

- SVG to PNG conversion using ImageMagick
- Multiple platform support (Android, iPhone, iPad)
- Transparent backgrounds

```bash
# Usage examples:
cd apps/security/kasmvnc-service/src/kasmweb/app/images/icons
make all          # Generate all icon sizes
```

## Common Usage Patterns

### 1. Documentation Generation (Sphinx)

- Used by Ghostwriter service
- Standard Sphinx Makefile pattern
- Supports multiple output formats (HTML, PDF, etc.)

### 2. Python Development Workflow

- Package management and distribution
- Code quality checks (pylint, coverage)
- Test execution and reporting

### 3. Native Code Compilation

- Cross-compilation for different architectures
- Custom compiler flags for embedded systems
- Library integration (OpenSSL, libpcap)

### 4. Multi-directory Coordination

- Recursive make across subdirectories
- Coordinated build and clean operations

### 5. Code Quality Automation

- Style checking (PHP CodeSniffer, JSHint)
- Copy/paste detection
- CI/CD integration

### 6. Asset Generation

- Icon generation from SVG sources
- Multiple resolution support
- Platform-specific variants

### 7. Internationalization Support

- Translation file management
- Locale generation for web applications
- Multi-language support

## Best Practices Observed

1. **Phony Targets:** Most Makefiles properly declare `.PHONY` targets
2. **Help Targets:** Documentation Makefiles include comprehensive help
3. **Clean Targets:** All build Makefiles include clean operations
4. **Ignore Patterns:** CI Makefiles use `.IGNORE` for non-critical failures
5. **Variable Usage:** Complex Makefiles use variables for maintainability
6. **Subdirectory Coordination:** Recursive make for multi-component builds

## Integration with NX Workspace

While these Makefiles exist within the NX workspace, they serve specialized purposes that complement the NX build system:

- **Native Compilation:** NX doesn't handle cross-compilation well
- **Legacy Tools:** Integration with existing toolchains (Sphinx, PHP tools)
- **Specialized Assets:** Icon generation, translation management
- **Security Tools:** BOF compilation, meterpreter builds

The Makefiles handle domain-specific build requirements while NX manages the overall TypeScript/JavaScript ecosystem.

## Summary

The apps directory contains 17 Makefiles across various security services, serving these primary functions:

- **Documentation:** 1 Makefile (Sphinx)
- **Python Development:** 1 Makefile (APIScout)
- **Native Compilation:** 8 Makefiles (Meterpreter, BOFs)
- **Code Quality:** 1 Makefile (MISP PHP)
- **Asset Generation:** 2 Makefiles (KasmVNC icons/i18n)
- **Build Coordination:** 4 Makefiles (Meterpreter subdirs)

These Makefiles complement the NX build system by handling specialized build requirements that fall outside the typical JavaScript/TypeScript ecosystem.

## Root-Level Makefile Integration

The root-level `/Makefile` provides high-level orchestration for the entire monorepo but **does not directly integrate** with the specialized service-level Makefiles documented above. Here's the relationship:

### What the Root Makefile Does

The root Makefile focuses on:

- **NX Orchestration:** Uses `npx nx run-many` for builds, tests, and linting
- **Python Environment:** Installs Python dependencies for core services only:
  - `apps/jane-orchestrator/requirements.txt`
  - `apps/cyber-llm-server/requirements.txt`
  - `apps/mtg-llm-server/requirements.txt`
  - `apps/code-llm-server/requirements.txt`
- **Docker Orchestration:** Manages Docker Compose for the entire stack
- **Infrastructure:** Kubernetes and Terraform commands for deployment
- **General Cleanup:** Removes common build artifacts (dist/, .next/, **pycache**)

### What the Root Makefile Does NOT Do

The root Makefile **does not** integrate with the specialized service Makefiles for:

- **Meterpreter native compilation** (8 Makefiles)
- **BOF compilation** for Brute Ratel
- **Sphinx documentation** for Ghostwriter
- **PHP code quality** checks for MISP
- **Icon generation** for KasmVNC
- **Internationalization** workflows for KasmVNC

### Integration Gap Analysis

This creates a **two-tier build system**:

1. **Tier 1 (Root Makefile):** High-level TypeScript/JavaScript/Python orchestration via NX
2. **Tier 2 (Service Makefiles):** Specialized native compilation, documentation, and asset generation

**Missing Integration Examples:**

```bash
# Root Makefile can do:
make build          # Builds NX-managed services only
make test           # Tests NX-managed services only

# But cannot do:
make build-meterpreter     # Would need to call meterpreter service Makefile
make build-bofs            # Would need to call BOF compilation Makefiles  
make generate-icons        # Would need to call KasmVNC icon generation
make build-docs            # Would need to call Sphinx documentation builds
```

### Potential Improvements

To fully integrate the specialized Makefiles, the root Makefile could add targets like:

```makefile
# Integration targets (not currently implemented)
build-native:
    $(MAKE) -C apps/security/meterpreter-service
    $(MAKE) -C apps/security/brute-ratel-service/src/assets/bofs samples

build-docs:
    $(MAKE) -C apps/security/ghostwriter-service/DOCS html

build-assets:
    $(MAKE) -C apps/security/kasmvnc-service/src/kasmweb/app/images/icons all
    $(MAKE) -C apps/security/kasmvnc-service/src/kasmweb/po update-js

build-all: build build-native build-docs build-assets
```

Currently, developers must manually navigate to service directories to use their specialized Makefiles, creating a fragmented build experience.
