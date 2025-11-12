# YARA-X Service - NX Integration

## Overview

This is the YARA-X pattern matching service integrated into the NX workspace. YARA-X is a next-generation YARA pattern matching engine written in Rust.

## Project Structure

The project follows the original YARA-X structure:

- `cli/` - Command line interface (`yr` binary)
- `lib/` - Core YARA-X Rust library
- `capi/` - C API bindings
- `py/` - Python bindings
- `go/` - Go bindings
- `fmt/` - Rule formatting library
- `parser/` - YARA rule parser
- `macros/` - Rust macros
- `proto/`, `proto-json/`, `proto-yaml/` - Protocol buffer definitions
- `site/` - Documentation website (Hugo)
- `docs/` - Documentation files

## Available Commands

### Build Commands
```bash
# Build the entire workspace
nx build yara-x-service

# Build for production
nx build yara-x-service --configuration=production

# Build specific components
nx capi:build yara-x-service    # C API
nx py:build yara-x-service      # Python bindings
```

### Development Commands
```bash
# Run the CLI tool
nx serve yara-x-service

# Show CLI help
nx serve:cli yara-x-service

# Serve documentation site
nx site:serve yara-x-service
```

### Testing Commands
```bash
# Run all tests
nx test yara-x-service

# Run specific test suites
nx test yara-x-service --configuration=unit        # Unit tests only
nx test yara-x-service --configuration=integration # Integration tests
nx test yara-x-service --configuration=cli         # CLI tests
nx test yara-x-service --configuration=coverage    # With coverage

# Run Go tests
nx go:test yara-x-service
```

### Code Quality
```bash
# Lint the code
nx lint yara-x-service

# Format check
nx format yara-x-service

# Format fix
nx format:fix yara-x-service
```

### Installation
```bash
# Install CLI globally
nx install yara-x-service

# Install Python bindings
nx py:install yara-x-service
```

### Docker
```bash
# Build Docker image
nx docker:build yara-x-service

# Run Docker container
nx docker:run yara-x-service
```

### Other Commands
```bash
# Clean build artifacts
nx clean yara-x-service

# Run fuzzer (requires nightly Rust)
nx fuzz yara-x-service

# Build documentation site
nx site:build yara-x-service
```

## Integration with Jane Orchestrator

This service is integrated with the security domain and can be used by:

- `security-service` - Main security service orchestration
- `jane-orchestrator` - Central orchestration service

## Dependencies

### Rust
- Rust 1.70+ (stable)
- Cargo

### Optional Dependencies
- Hugo (for documentation site)
- Python 3.8+ (for Python bindings)
- Go 1.19+ (for Go bindings)
- Nightly Rust (for fuzzing)

## Usage Examples

### CLI Usage
```bash
# Compile YARA rules
nx serve yara-x-service -- compile rules.yar -o rules.yarc

# Scan files
nx serve yara-x-service -- scan rules.yarc /path/to/files

# Format YARA rules
nx serve yara-x-service -- fmt rules.yar
```

### Library Usage in Rust
```rust
use yara_x;

let rules = yara_x::compile(r#"
    rule example {
        strings:
            $a = "hello world"
        condition:
            $a
    }
"#)?;

let mut scanner = rules.scanner();
let results = scanner.scan("hello world".as_bytes())?;
```

## Configuration

YARA-X can be configured using a `.yara-x.toml` file in the user's home directory. See the [configuration documentation](site/content/docs/cli/config.md) for details.

## Performance

YARA-X uses WebAssembly for secure and efficient rule execution. Performance benchmarks and optimizations are available in the original documentation.

## Migration Notes

This project was migrated from `features/yara-x` to `apps/yara-x-service` to integrate with the NX workspace system. All original functionality has been preserved.

## Security Domain Integration

As part of the security domain, this service provides:

- Pattern matching capabilities for malware detection
- Rule compilation and validation
- Integration with other security tools in the workspace
- C API for integration with legacy tools
- Python bindings for scripting and automation

## Links

- [Original YARA-X Repository](https://github.com/VirusTotal/yara-x)
- [YARA-X Documentation](https://virustotal.github.io/yara-x/)
- [Rust Crate Documentation](https://docs.rs/yara-x/latest/)