#!/usr/bin/env python3
"""
Spec-Kit Validation System
Implements universal-first validation with opt-in enhancements
"""

import re
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import yaml


class ValidationLevel(Enum):
    """Validation strictness levels"""
    PERMISSIVE = "permissive"    # 40+ score, relaxed requirements
    STANDARD = "standard"        # 60+ score, balanced requirements (default)
    STRICT = "strict"           # 80+ score, comprehensive requirements
    ENTERPRISE = "enterprise"    # 95+ score, exhaustive requirements


class ValidationResult(Enum):
    """Validation result types"""
    PASS = "pass"
    WARNING = "warning"
    ERROR = "error"
    INFO = "info"


@dataclass
class ValidationIssue:
    """Individual validation issue"""
    result_type: ValidationResult
    section: str
    message: str
    line_number: Optional[int] = None
    suggestion: Optional[str] = None


@dataclass
class ValidationReport:
    """Complete validation report"""
    score: float
    total_sections: int
    passed_sections: int
    issues: List[ValidationIssue]
    level: ValidationLevel
    threshold_met: bool


class TechnicalPatternDetector:
    """Recognizes legitimate technical content vs placeholders"""

    # Universal technical patterns (domain-agnostic)
    LEGITIMATE_PATTERNS = {
        # Structured identifiers (CVE-2024-1234, RFC-9000, etc.)
        'structured_identifiers': r'^[A-Z]{2,6}[-:][A-Z0-9\-\.]{2,}$',

        # Hex patterns and binary data
        'hex_data': r'\{[0-9A-Fa-f\s\?]{4,}\}',
        'hex_literal': r'0x[0-9A-Fa-f]+',
        'binary_escape': r'\\x[0-9A-Fa-f]{2}',

        # JSON and structured config
        'json_object': r'\{[^{}]*"[^"]*"[^{}]*:[^{}]*\}',
        'json_array': r'\[[^[\]]*\{[^{}]*\}[^[\]]*\]',

        # Environment variables and system references
        'env_variables': r'\$\{[A-Z_][A-Z0-9_]*\}',
        'shell_variables': r'\$[A-Z_][A-Z0-9_]*',

        # File system paths
        'file_paths': r'[/\\][\w\-\.\/\\]+\.\w+',
        'relative_paths': r'[\w\-]+[/\\][\w\-\.\/\\]+',

        # API and network
        'api_endpoints': r'/api/[v\d/\w\-{}]*',
        'http_methods': r'(GET|POST|PUT|DELETE|PATCH)\s+/',
        'urls': r'https?://[^\s]+',

        # CLI and command patterns
        'cli_args': r'--[\w-]+',
        'command_line': r'^\w+\s+[-\w\s]+$',

        # Database and schema
        'sql_fields': r'[a-z_]+\.[a-z_]+',
        'db_fields': r'[a-z_]+_[a-z_]+',

        # Financial and business
        'currency': r'\$[\d,]+\.?\d*',
        'percentages': r'\d+%',
        'dates': r'\d{4}-\d{2}-\d{2}',
        'quarters': r'Q[1-4]\s+\d{4}',

        # Technical specifications
        'version_numbers': r'v?\d+\.\d+\.\d+',
        'port_numbers': r':\d{2,5}',
        'ip_addresses': r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}',

        # Code and syntax patterns
        'function_calls': r'\w+\([^)]*\)',
        'imports': r'(import|from)\s+[\w\.]+',

        # Domain-specific but universal patterns
        'regex_patterns': r'[\^\$\[\]\\\/\.\*\+\?\{\}\|]+',
        'markup_tags': r'<[^>]+>',
    }

    # Contextual patterns (require surrounding context)
    CONTEXTUAL_PATTERNS = {
        # TODO/TBD with explanation (legitimate)
        'contextual_todo': r'TODO:\s+[A-Za-z].{10,}',
        'contextual_tbd': r'TBD:\s+[A-Za-z].{10,}',
        'explained_na': r'N/A\s*[-:]\s*[A-Za-z].{5,}',
    }

    # Actual placeholders to flag
    PLACEHOLDER_PATTERNS = {
        # Generic template variables
        'template_vars': r'\{[a-z_][a-z0-9_]*\}',
        'bracket_placeholders': r'\[[A-Z][A-Z\s]*\]',

        # Bare TODO/TBD without explanation
        'bare_todo': r'^TODO\s*$',
        'bare_tbd': r'^TBD\s*$',

        # Explicit placeholder markers
        'explicit_placeholders': r'\[?(PLACEHOLDER|REPLACE|YOUR|FILL|ADD).*?\]?',
        'template_markers': r'\{.*?template.*?\}',

        # Generic prompts
        'generic_prompts': r'\[.*?(here|name|details|value).*?\]',
    }

    def is_legitimate_technical_content(self, text: str) -> Tuple[bool, str]:
        """Check if text is legitimate technical content"""
        text = text.strip()

        # Check for honest N/A responses
        if re.match(r'^N/A\s*$', text, re.IGNORECASE):
            return True, "Honest N/A response"

        if re.match(r'^(None|Not applicable)\s*$', text, re.IGNORECASE):
            return True, "Explicit not applicable"

        # Check contextual patterns first (need explanation)
        for pattern_name, pattern in self.CONTEXTUAL_PATTERNS.items():
            if re.search(pattern, text, re.IGNORECASE | re.MULTILINE):
                return True, f"Contextual content: {pattern_name}"

        # Check legitimate technical patterns
        for pattern_name, pattern in self.LEGITIMATE_PATTERNS.items():
            if re.search(pattern, text, re.IGNORECASE):
                return True, f"Technical pattern: {pattern_name}"

        # Check for placeholder patterns (but be more selective)
        # Only flag as placeholder if it matches placeholder patterns AND doesn't match legitimate patterns
        placeholder_matches = []
        for pattern_name, pattern in self.PLACEHOLDER_PATTERNS.items():
            if re.search(pattern, text, re.IGNORECASE):
                placeholder_matches.append(pattern_name)

        # If we found placeholder patterns, check if they're actually legitimate
        if placeholder_matches:
            # Special cases: some patterns can be legitimate in context
            if 'template_vars' in placeholder_matches:
                # {variable} can be legitimate in technical contexts
                if any(re.search(pattern, text) for pattern in [
                    # Environment variables like {API_KEY}
                    r'\{[A-Z_][A-Z0-9_]*\}',
                    r'\{[a-z]+_[a-z]+\}',     # DB fields like {user_id}
                    r'\{[0-9A-Fa-f\s\?]+\}',  # Hex patterns
                ]):
                    return True, "Technical variable pattern"

            # If it's a bare TODO/TBD without context, flag it
            if text.strip().upper() in ['TODO', 'TBD', '[TODO]', '[TBD]']:
                return False, f"Placeholder detected: bare {text.strip()}"

            # If it has explanation/context, it's legitimate
            if len(text.split()) >= 5:  # Has some explanation
                return True, "Content with explanation"

        # If no patterns match, consider substantial content as legitimate
        if len(text.split()) >= 3:  # At least 3 words
            return True, "Substantial content"

        return False, "Insufficient content"

    def analyze_content_quality(self, content: str) -> Dict:
        """Analyze overall content quality"""
        lines = content.split('\n')
        total_lines = len(lines)

        legitimate_lines = 0
        placeholder_lines = 0
        empty_lines = 0

        issues = []

        for i, line in enumerate(lines, 1):
            line = line.strip()
            if not line:
                empty_lines += 1
                continue

            is_legit, reason = self.is_legitimate_technical_content(line)
            if is_legit:
                legitimate_lines += 1
            else:
                placeholder_lines += 1
                issues.append({
                    'line': i,
                    'content': line[:50] + "..." if len(line) > 50 else line,
                    'reason': reason
                })

        content_lines = total_lines - empty_lines
        quality_ratio = legitimate_lines / content_lines if content_lines > 0 else 0

        return {
            'total_lines': total_lines,
            'content_lines': content_lines,
            'legitimate_lines': legitimate_lines,
            'placeholder_lines': placeholder_lines,
            'empty_lines': empty_lines,
            'quality_ratio': quality_ratio,
            'issues': issues
        }


class ValidationConfig:
    """Validation configuration with opt-in enhancements"""

    DEFAULT_CONFIG = {
        'validation': {
            'quality_threshold': 60,
            'allow_na_responses': True,
            'technical_pattern_recognition': True,
            'level': 'standard'
        },
        'project': {
            'type': 'universal'
        },
        'advanced': {
            'domain_detection': False,
            'confidence_threshold': 0.75,
            'custom_patterns': []
        }
    }

    def __init__(self, config_path: Optional[Path] = None):
        self.config = self.DEFAULT_CONFIG.copy()

        if config_path and config_path.exists():
            try:
                with open(config_path, 'r') as f:
                    user_config = yaml.safe_load(f)
                self._merge_config(user_config)
            except Exception as e:
                print(
                    f"Warning: Could not load config from {config_path}: {e}")

    def _merge_config(self, user_config: dict):
        """Merge user config with defaults"""
        for section, settings in user_config.items():
            if section in self.config:
                self.config[section].update(settings)
            else:
                self.config[section] = settings

    def get_validation_level(self) -> ValidationLevel:
        """Get validation strictness level"""
        level_str = self.config['validation']['level']
        try:
            return ValidationLevel(level_str)
        except ValueError:
            return ValidationLevel.STANDARD

    def get_quality_threshold(self) -> float:
        """Get quality score threshold"""
        return self.config['validation']['quality_threshold']

    def allows_na_responses(self) -> bool:
        """Check if N/A responses are allowed"""
        return self.config['validation']['allow_na_responses']

    def uses_technical_patterns(self) -> bool:
        """Check if technical pattern recognition is enabled"""
        return self.config['validation']['technical_pattern_recognition']


class AnalysisValidator:
    """Main analysis validation system"""

    # Universal section requirements (domain-agnostic)
    UNIVERSAL_SECTIONS = {
        1: {"name": "Project Identity & Context", "required": True, "weight": 10},
        2: {"name": "Technical Architecture", "required": True, "weight": 15},
        12: {"name": "Success Criteria", "required": True, "weight": 10},
    }

    # Conditionally important sections (may be N/A for some project types)
    CONDITIONAL_SECTIONS = {
        3: {"name": "Business Logic", "weight": 15, "na_acceptable": "CLI tools, libraries"},
        4: {"name": "API Architecture", "weight": 10, "na_acceptable": "Non-API projects"},
        5: {"name": "External Integrations", "weight": 10, "na_acceptable": "Standalone tools"},
        6: {"name": "Frontend Architecture", "weight": 10, "na_acceptable": "Backend-only, CLI tools"},
        7: {"name": "Testing & Quality", "weight": 10, "na_acceptable": "Early prototypes"},
        8: {"name": "Performance", "weight": 10, "na_acceptable": "Simple utilities"},
        9: {"name": "Security & Compliance", "weight": 10, "na_acceptable": "Local-only tools"},
        10: {"name": "Deployment & Operations", "weight": 5, "na_acceptable": "Development tools"},
        11: {"name": "Migration Assessment", "weight": 5, "na_acceptable": "Greenfield projects"},
    }

    def __init__(self, config: ValidationConfig):
        self.config = config
        self.pattern_detector = TechnicalPatternDetector()

    def validate_analysis_file(self, file_path: Path) -> ValidationReport:
        """Validate a project analysis file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return self.validate_analysis_content(content)
        except Exception as e:
            return ValidationReport(
                score=0.0,
                total_sections=0,
                passed_sections=0,
                issues=[ValidationIssue(
                    ValidationResult.ERROR, "File", f"Could not read file: {e}")],
                level=self.config.get_validation_level(),
                threshold_met=False
            )

    def validate_analysis_content(self, content: str) -> ValidationReport:
        """Validate analysis content string"""
        sections = self._extract_sections(content)
        issues = []
        section_scores = {}

        level = self.config.get_validation_level()
        threshold = self._get_threshold_for_level(level)

        # Validate universal sections (always required)
        for section_id, section_info in self.UNIVERSAL_SECTIONS.items():
            score = self._validate_section(
                section_id,
                section_info,
                sections.get(section_id, ""),
                required=True
            )
            section_scores[section_id] = score

            if score['issues']:
                issues.extend(score['issues'])

        # Validate conditional sections (may be N/A)
        for section_id, section_info in self.CONDITIONAL_SECTIONS.items():
            score = self._validate_section(
                section_id,
                section_info,
                sections.get(section_id, ""),
                required=False
            )
            section_scores[section_id] = score

            if score['issues']:
                issues.extend(score['issues'])

        # Calculate overall score
        total_possible = sum(info['weight'] for info in {
                             **self.UNIVERSAL_SECTIONS, **self.CONDITIONAL_SECTIONS}.values())
        earned_score = sum(score['score'] * info['weight'] for section_id, score in section_scores.items()
                           for info in [{**self.UNIVERSAL_SECTIONS, **self.CONDITIONAL_SECTIONS}[section_id]])

        final_score = (earned_score / total_possible) * \
            100 if total_possible > 0 else 0

        passed_sections = sum(
            1 for score in section_scores.values() if score['score'] >= 0.6)
        total_sections = len(section_scores)

        threshold_met = final_score >= threshold

        return ValidationReport(
            score=final_score,
            total_sections=total_sections,
            passed_sections=passed_sections,
            issues=issues,
            level=level,
            threshold_met=threshold_met
        )

    def _extract_sections(self, content: str) -> Dict[int, str]:
        """Extract sections from markdown content"""
        sections = {}
        current_section = None
        current_content = []

        lines = content.split('\n')

        for line in lines:
            # Look for section headers (## Section N: or ### N.N)
            section_match = re.match(r'^##\s+(?:Section\s+)?(\d+)[:.]', line)
            if section_match:
                # Save previous section
                if current_section is not None:
                    sections[current_section] = '\n'.join(current_content)

                # Start new section
                current_section = int(section_match.group(1))
                current_content = []
                continue

            # Look for numbered sections (### N.N)
            subsection_match = re.match(r'^###\s+(\d+)\.', line)
            if subsection_match:
                section_num = int(subsection_match.group(1))
                if current_section != section_num:
                    # Save previous section
                    if current_section is not None:
                        sections[current_section] = '\n'.join(current_content)

                    # Start new section
                    current_section = section_num
                    current_content = []
                continue

            # Add line to current section
            if current_section is not None:
                current_content.append(line)

        # Save final section
        if current_section is not None:
            sections[current_section] = '\n'.join(current_content)

        return sections

    def _validate_section(self, section_id: int, section_info: Dict, content: str, required: bool) -> Dict:
        """Validate individual section"""
        issues = []
        content = content.strip()

        if not content:
            if required:
                issues.append(ValidationIssue(
                    ValidationResult.ERROR,
                    f"Section {section_id}",
                    f"Required section '{section_info['name']}' is missing or empty"
                ))
                return {'score': 0.0, 'issues': issues}
            else:
                issues.append(ValidationIssue(
                    ValidationResult.WARNING,
                    f"Section {section_id}",
                    f"Optional section '{section_info['name']}' is empty"
                ))
                return {'score': 0.5, 'issues': issues}

        # Check for N/A responses
        if re.match(r'^N/A\s*', content, re.IGNORECASE):
            if self.config.allows_na_responses() and not required:
                # Check if N/A has explanation
                na_match = re.match(
                    r'^N/A\s*[-:]\s*(.+)', content, re.IGNORECASE | re.DOTALL)
                if na_match and len(na_match.group(1).strip()) > 10:
                    issues.append(ValidationIssue(
                        ValidationResult.INFO,
                        f"Section {section_id}",
                        f"Section marked N/A with explanation: {na_match.group(1)[:50]}..."
                    ))
                    # Good N/A response
                    return {'score': 0.8, 'issues': issues}
                else:
                    issues.append(ValidationIssue(
                        ValidationResult.WARNING,
                        f"Section {section_id}",
                        "N/A response should include brief explanation"
                    ))
                    # Acceptable but could be better
                    return {'score': 0.6, 'issues': issues}
            else:
                issues.append(ValidationIssue(
                    ValidationResult.ERROR,
                    f"Section {section_id}",
                    f"N/A not acceptable for required section '{section_info['name']}'"
                ))
                return {'score': 0.2, 'issues': issues}

        # Analyze content quality using technical pattern recognition
        if self.config.uses_technical_patterns():
            quality_analysis = self.pattern_detector.analyze_content_quality(
                content)

            # Flag significant placeholder content
            # Less than 40% legitimate content
            if quality_analysis['quality_ratio'] < 0.4:
                # Show first 3 issues
                for issue in quality_analysis['issues'][:3]:
                    issues.append(ValidationIssue(
                        ValidationResult.WARNING,
                        f"Section {section_id}",
                        f"Line {issue['line']}: {issue['reason']} - '{issue['content']}'"
                    ))

            # Score based on content quality
            # Slight boost for good content
            base_score = min(quality_analysis['quality_ratio'] * 1.2, 1.0)

            # Length consideration
            word_count = len(content.split())
            if word_count < 10:
                base_score *= 0.7  # Penalty for very short content
            elif word_count > 50:
                # Bonus for comprehensive content
                base_score = min(base_score * 1.1, 1.0)
        else:
            # Basic validation without pattern recognition
            word_count = len(content.split())
            if word_count < 5:
                base_score = 0.3
                issues.append(ValidationIssue(
                    ValidationResult.WARNING,
                    f"Section {section_id}",
                    "Section appears too brief for thorough analysis"
                ))
            elif word_count < 20:
                base_score = 0.7
            else:
                base_score = 1.0

        return {'score': base_score, 'issues': issues}

    def _get_threshold_for_level(self, level: ValidationLevel) -> float:
        """Get score threshold for validation level"""
        thresholds = {
            ValidationLevel.PERMISSIVE: 40.0,
            ValidationLevel.STANDARD: self.config.get_quality_threshold(),
            ValidationLevel.STRICT: 80.0,
            ValidationLevel.ENTERPRISE: 95.0
        }
        return thresholds.get(level, 60.0)


def create_default_config_file(config_path: Path):
    """Create default configuration file"""
    config_content = """# Spec-Kit Validation Configuration
# Universal-first approach with opt-in enhancements

project:
  type: universal  # Default: never assume domain unless explicitly set

validation:
  quality_threshold: 60              # Practical threshold (40-95 range)
  allow_na_responses: true           # Accept N/A for inapplicable sections
  technical_pattern_recognition: true # Recognize legitimate technical content
  level: standard                    # permissive|standard|strict|enterprise

# Advanced features (explicit opt-in only)
advanced:
  domain_detection: false            # Must be explicitly enabled
  confidence_threshold: 0.75         # High bar for auto-classification
  custom_patterns: []                # User-defined pattern extensions

# Usage examples:
# specify validate                           # Use defaults
# specify validate --level=strict           # Override strictness
# specify validate --threshold=80           # Override threshold
# specify validate --config=custom.yaml    # Use custom config
"""

    config_path.parent.mkdir(parents=True, exist_ok=True)
    with open(config_path, 'w') as f:
        f.write(config_content)


if __name__ == "__main__":
    # Example usage and testing
    config = ValidationConfig()
    validator = AnalysisValidator(config)

    # Test with sample content
    sample_content = """
# Project Analysis: Sample Project

## 1. Project Identity & Context

**System Name**: Sample System
**Primary Function**: Demonstrates validation patterns
**Technology Stack**: Python, FastAPI, PostgreSQL

## 2. Technical Architecture

```yaml
Architecture: Microservices
Database: PostgreSQL 14
Backend: Python 3.11 + FastAPI
```

## 3. Business Logic

N/A - This is a CLI library with no business workflows

## 4. API Architecture

**Endpoints**:
- GET /api/v1/health: Health check endpoint
- POST /api/v1/data: {"status": "ok", "data": []}

## 12. Success Criteria

- [ ] 100% feature parity maintained
- [ ] Response times within 200ms
- [ ] Zero data loss during migration
"""

    report = validator.validate_analysis_content(sample_content)
    print(f"Validation Score: {report.score:.1f}/100")
    print(f"Threshold Met: {report.threshold_met}")
    print(f"Sections Passed: {report.passed_sections}/{report.total_sections}")

    if report.issues:
        print("\nIssues found:")
        for issue in report.issues:
            print(
                f"  {issue.result_type.value.upper()}: {issue.section} - {issue.message}")
