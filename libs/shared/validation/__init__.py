"""
Validation utilities for Mental Prosthetic Platform.

Provides unified validation patterns across all 37 integrated tools with:
- Domain-specific validation rules with clear error messages
- Executive function accommodations (progressive hints, clear feedback)
- Security validation (input sanitization, XSS prevention)
- Performance validation (domain-specific thresholds)
- Business logic validation with contextual error messages
"""

import ipaddress
import re
from enum import Enum
from typing import Any, Dict, List, Optional
from urllib.parse import urlparse

from email_validator import EmailNotValidError, validate_email
from pydantic import BaseModel

from ..config import Domain
from ..logging import get_logger


class ValidationLevel(str, Enum):
    """Validation strictness levels."""
    PERMISSIVE = "permissive"  # Allow most input, basic safety only
    NORMAL = "normal"          # Standard validation rules
    STRICT = "strict"          # Enhanced security validation
    PARANOID = "paranoid"      # Maximum security validation


class ValidationError(Exception):
    """Validation error with executive function accommodations."""

    def __init__(
        self,
        field: str,
        message: str,
        user_message: Optional[str] = None,
        suggestions: Optional[List[str]] = None,
        value: Optional[Any] = None
    ):
        self.field = field
        self.message = message
        self.user_message = user_message or message
        self.suggestions = suggestions or []
        self.value = value
        super().__init__(self.user_message)


class ValidationResult(BaseModel):
    """Result of validation with detailed feedback."""

    is_valid: bool
    field: str
    value: Any
    error_message: Optional[str] = None
    user_message: Optional[str] = None
    suggestions: List[str] = []
    warnings: List[str] = []

    # Executive function accommodations
    confidence_score: float = 1.0  # 0.0-1.0 confidence in validation
    progressive_hints: List[str] = []


class BaseValidator:
    """Base validator with executive function accommodations."""

    def __init__(
        self,
        level: ValidationLevel = ValidationLevel.NORMAL,
        enable_suggestions: bool = True,
        enable_progressive_hints: bool = True
    ):
        self.level = level
        self.enable_suggestions = enable_suggestions
        self.enable_progressive_hints = enable_progressive_hints
        self.logger = get_logger(self.__class__.__name__)

    def validate(self, field: str, value: Any) -> ValidationResult:
        """Validate a field value with detailed feedback."""
        try:
            is_valid = self._validate_value(field, value)

            result = ValidationResult(
                is_valid=is_valid,
                field=field,
                value=value
            )

            # Add suggestions if enabled and validation failed
            if not is_valid and self.enable_suggestions:
                result.suggestions = self._generate_suggestions(field, value)

            # Add progressive hints if enabled
            if self.enable_progressive_hints:
                result.progressive_hints = self._generate_progressive_hints(
                    field, value
                )

            return result

        except Exception as e:
            return ValidationResult(
                is_valid=False,
                field=field,
                value=value,
                error_message=str(e),
                user_message=f"Validation failed for {field}: {str(e)}"
            )

    def _validate_value(self, field: str, value: Any) -> bool:
        """Override in subclasses to implement validation logic."""
        return True

    def _generate_suggestions(self, field: str, value: Any) -> List[str]:
        """Override in subclasses to provide helpful suggestions."""
        return []

    def _generate_progressive_hints(self, field: str, value: Any) -> List[str]:
        """Generate progressive hints for executive function support."""
        return []


class StringValidator(BaseValidator):
    """String validation with security and length checks."""

    def __init__(
        self,
        min_length: Optional[int] = None,
        max_length: Optional[int] = None,
        pattern: Optional[str] = None,
        allowed_chars: Optional[str] = None,
        forbidden_chars: Optional[str] = None,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.min_length = min_length
        self.max_length = max_length
        self.pattern = re.compile(pattern) if pattern else None
        self.allowed_chars = set(allowed_chars) if allowed_chars else None
        self.forbidden_chars = set(
            forbidden_chars) if forbidden_chars else None

        # Security patterns
        self.xss_patterns = [
            r'<script.*?>.*?</script>',
            r'javascript:',
            r'on\w+\s*=',
            r'expression\s*\(',
        ]

        self.sql_injection_patterns = [
            r"'.*?'",
            r'".*?"',
            r'union.*select',
            r'drop.*table',
            r'delete.*from',
            r'insert.*into',
        ]

    def _validate_value(self, field: str, value: Any) -> bool:
        """Validate string value."""
        if not isinstance(value, str):
            raise ValidationError(
                field,
                f"Expected string, got {type(value).__name__}",
                f"Please provide text for {field}"
            )

        # Length checks
        if self.min_length is not None and len(value) < self.min_length:
            raise ValidationError(
                field,
                f"String too short: {len(value)} < {self.min_length}",
                f"{field} must be at least {self.min_length} characters long",
                suggestions=[
                    f"Add {self.min_length - len(value)} more characters"]
            )

        if self.max_length is not None and len(value) > self.max_length:
            raise ValidationError(
                field,
                f"String too long: {len(value)} > {self.max_length}",
                f"{field} must be no more than {self.max_length} characters long",
                suggestions=[
                    f"Remove {len(value) - self.max_length} characters"]
            )

        # Pattern check
        if self.pattern and not self.pattern.match(value):
            raise ValidationError(
                field,
                f"String doesn't match required pattern",
                f"{field} format is not valid",
                suggestions=self._generate_pattern_suggestions(value)
            )

        # Character restrictions
        if self.allowed_chars:
            invalid_chars = set(value) - self.allowed_chars
            if invalid_chars:
                raise ValidationError(
                    field,
                    f"Contains forbidden characters: {invalid_chars}",
                    f"{field} contains invalid characters: {', '.join(invalid_chars)}",
                    suggestions=[
                        f"Remove these characters: {', '.join(invalid_chars)}"]
                )

        if self.forbidden_chars:
            found_forbidden = set(value) & self.forbidden_chars
            if found_forbidden:
                raise ValidationError(
                    field,
                    f"Contains forbidden characters: {found_forbidden}",
                    f"{field} contains forbidden characters: {', '.join(found_forbidden)}",
                    suggestions=[
                        f"Remove these characters: {', '.join(found_forbidden)}"]
                )

        # Security checks for strict/paranoid levels
        if self.level in [ValidationLevel.STRICT, ValidationLevel.PARANOID]:
            self._check_security_patterns(field, value)

        return True

    def _check_security_patterns(self, field: str, value: str):
        """Check for security vulnerabilities."""
        value_lower = value.lower()

        # XSS check
        for pattern in self.xss_patterns:
            if re.search(pattern, value_lower, re.IGNORECASE):
                raise ValidationError(
                    field,
                    "Potential XSS attack detected",
                    f"{field} contains potentially dangerous content",
                    suggestions=["Remove any HTML/JavaScript code"]
                )

        # SQL injection check (for paranoid level)
        if self.level == ValidationLevel.PARANOID:
            for pattern in self.sql_injection_patterns:
                if re.search(pattern, value_lower, re.IGNORECASE):
                    raise ValidationError(
                        field,
                        "Potential SQL injection detected",
                        f"{field} contains potentially dangerous SQL patterns",
                        suggestions=["Remove SQL-like commands and quotes"]
                    )

    def _generate_pattern_suggestions(self, value: str) -> List[str]:
        """Generate suggestions based on pattern mismatch."""
        suggestions = []

        # Common pattern fixes
        if self.pattern:
            pattern_str = self.pattern.pattern

            if 'email' in pattern_str.lower() or '@' in pattern_str:
                suggestions.append("Use format: username@domain.com")
            elif 'phone' in pattern_str.lower():
                suggestions.append("Use format: +1-234-567-8900")
            elif 'url' in pattern_str.lower() or 'http' in pattern_str:
                suggestions.append("Use format: https://example.com")
            elif '[a-z]' in pattern_str or '[A-Z]' in pattern_str:
                suggestions.append("Use only letters and numbers")

        return suggestions

    def _generate_progressive_hints(self, field: str, value: Any) -> List[str]:
        """Generate progressive hints for string validation."""
        hints = []

        if not isinstance(value, str):
            hints.append(f"Step 1: Make sure {field} is text")
            return hints

        if self.min_length and len(value) < self.min_length:
            hints.append(
                f"Step 1: Add more characters (need {self.min_length - len(value)} more)")

        if self.pattern:
            hints.append(
                f"Step 2: Check that {field} follows the correct format")

        if self.level in [ValidationLevel.STRICT, ValidationLevel.PARANOID]:
            hints.append("Step 3: Ensure content is safe (no scripts or SQL)")

        return hints


class EmailValidator(BaseValidator):
    """Email validation with deliverability checks."""

    def __init__(self, check_deliverability: bool = False, **kwargs):
        super().__init__(**kwargs)
        self.check_deliverability = check_deliverability

    def _validate_value(self, field: str, value: Any) -> bool:
        """Validate email address."""
        if not isinstance(value, str):
            raise ValidationError(
                field,
                f"Expected string, got {type(value).__name__}",
                f"Please provide an email address for {field}"
            )

        try:
            # Use email-validator library
            valid = validate_email(
                value,
                check_deliverability=self.check_deliverability
            )
            return True

        except EmailNotValidError as e:
            suggestions = []

            # Generate helpful suggestions based on common mistakes
            if '@' not in value:
                suggestions.append("Add '@' symbol (e.g., user@domain.com)")
            elif value.count('@') > 1:
                suggestions.append("Use only one '@' symbol")
            elif '.' not in value.split('@')[-1]:
                suggestions.append("Add domain extension (e.g., .com, .org)")
            elif value.endswith('.'):
                suggestions.append("Remove trailing dot")
            elif ' ' in value:
                suggestions.append("Remove spaces from email address")

            raise ValidationError(
                field,
                str(e),
                f"Please provide a valid email address for {field}",
                suggestions=suggestions
            )

    def _generate_progressive_hints(self, field: str, value: Any) -> List[str]:
        """Generate progressive hints for email validation."""
        hints = []

        if not isinstance(value, str):
            hints.append(f"Step 1: Make sure {field} is text")
            return hints

        hints.append("Step 1: Check format is user@domain.com")

        if self.check_deliverability:
            hints.append("Step 2: Verify the email domain exists")

        hints.append("Step 3: Ensure no extra spaces or special characters")

        return hints


class URLValidator(BaseValidator):
    """URL validation with security checks."""

    def __init__(
        self,
        allowed_schemes: Optional[List[str]] = None,
        allowed_domains: Optional[List[str]] = None,
        forbidden_domains: Optional[List[str]] = None,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.allowed_schemes = allowed_schemes or ['http', 'https']
        self.allowed_domains = allowed_domains
        self.forbidden_domains = forbidden_domains or []

        # Security: dangerous domains/patterns
        self.dangerous_patterns = [
            r'localhost',
            r'127\.0\.0\.1',
            r'0\.0\.0\.0',
            r'192\.168\.',
            r'10\.',
            r'172\.(1[6-9]|2[0-9]|3[0-1])\.',
        ]

    def _validate_value(self, field: str, value: Any) -> bool:
        """Validate URL."""
        if not isinstance(value, str):
            raise ValidationError(
                field,
                f"Expected string, got {type(value).__name__}",
                f"Please provide a URL for {field}"
            )

        try:
            parsed = urlparse(value)
        except Exception as e:
            raise ValidationError(
                field,
                f"Invalid URL format: {str(e)}",
                f"Please provide a valid URL for {field}",
                suggestions=["Use format: https://example.com"]
            )

        # Scheme validation
        if parsed.scheme not in self.allowed_schemes:
            raise ValidationError(
                field,
                f"Scheme '{parsed.scheme}' not allowed",
                f"URL must start with one of: {', '.join(self.allowed_schemes)}",
                suggestions=[
                    f"Change to: {self.allowed_schemes[0]}://{parsed.netloc}{parsed.path}"]
            )

        # Domain validation
        if self.allowed_domains and parsed.netloc not in self.allowed_domains:
            raise ValidationError(
                field,
                f"Domain '{parsed.netloc}' not allowed",
                f"Only these domains are allowed: {', '.join(self.allowed_domains)}"
            )

        if parsed.netloc in self.forbidden_domains:
            raise ValidationError(
                field,
                f"Domain '{parsed.netloc}' is forbidden",
                f"This domain is not allowed: {parsed.netloc}"
            )

        # Security checks for strict/paranoid levels
        if self.level in [ValidationLevel.STRICT, ValidationLevel.PARANOID]:
            self._check_url_security(field, parsed)

        return True

    def _check_url_security(self, field: str, parsed):
        """Check URL for security issues."""
        netloc = parsed.netloc.lower()

        # Check for dangerous domains (local/internal networks)
        for pattern in self.dangerous_patterns:
            if re.search(pattern, netloc):
                if self.level == ValidationLevel.PARANOID:
                    raise ValidationError(
                        field,
                        f"Dangerous domain detected: {netloc}",
                        f"Internal/local URLs are not allowed for security reasons"
                    )
                else:
                    # Just warn for strict level
                    self.logger.warning(f"Potentially dangerous URL: {netloc}")

    def _generate_suggestions(self, field: str, value: Any) -> List[str]:
        """Generate URL suggestions."""
        suggestions = []

        if isinstance(value, str):
            if not value.startswith(('http://', 'https://')):
                suggestions.append(f"Add https:// to the beginning")

            if ' ' in value:
                suggestions.append("Remove spaces from URL")

            if not urlparse(value).netloc:
                suggestions.append("Include domain name (e.g., example.com)")

        return suggestions


class IPAddressValidator(BaseValidator):
    """IP address validation with security checks."""

    def __init__(
        self,
        allow_ipv4: bool = True,
        allow_ipv6: bool = True,
        allow_private: bool = True,
        allow_loopback: bool = False,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.allow_ipv4 = allow_ipv4
        self.allow_ipv6 = allow_ipv6
        self.allow_private = allow_private
        self.allow_loopback = allow_loopback

    def _validate_value(self, field: str, value: Any) -> bool:
        """Validate IP address."""
        if not isinstance(value, str):
            raise ValidationError(
                field,
                f"Expected string, got {type(value).__name__}",
                f"Please provide an IP address for {field}"
            )

        try:
            ip = ipaddress.ip_address(value)
        except ValueError as e:
            suggestions = []

            # Generate helpful suggestions
            if ':' in value and not self.allow_ipv6:
                suggestions.append("Use IPv4 format: 192.168.1.1")
            elif '.' in value and not self.allow_ipv4:
                suggestions.append("Use IPv6 format: 2001:db8::1")
            else:
                suggestions.append("Check IP address format")
                suggestions.append("IPv4 example: 192.168.1.1")
                suggestions.append("IPv6 example: 2001:db8::1")

            raise ValidationError(
                field,
                f"Invalid IP address: {str(e)}",
                f"Please provide a valid IP address for {field}",
                suggestions=suggestions
            )

        # Version checks
        if isinstance(ip, ipaddress.IPv4Address) and not self.allow_ipv4:
            raise ValidationError(
                field,
                "IPv4 addresses not allowed",
                f"Please use IPv6 format for {field}"
            )

        if isinstance(ip, ipaddress.IPv6Address) and not self.allow_ipv6:
            raise ValidationError(
                field,
                "IPv6 addresses not allowed",
                f"Please use IPv4 format for {field}"
            )

        # Security checks
        if not self.allow_private and ip.is_private:
            raise ValidationError(
                field,
                f"Private IP addresses not allowed: {ip}",
                f"Please use a public IP address for {field}"
            )

        if not self.allow_loopback and ip.is_loopback:
            raise ValidationError(
                field,
                f"Loopback addresses not allowed: {ip}",
                f"Please use a non-loopback IP address for {field}"
            )

        return True


class PerformanceValidator(BaseValidator):
    """Performance threshold validation for domain-specific requirements."""

    def __init__(
        self,
        domain: Domain,
        response_time_threshold: Optional[float] = None,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.domain = domain

        # Domain-specific thresholds (seconds)
        default_thresholds = {
            Domain.SECURITY: 1.0,        # <1s for security
            Domain.PRODUCTIVITY: 2.0,    # <2s for productivity
            Domain.TCG: 3.0,             # <3s for TCG
            Domain.INFRASTRUCTURE: 5.0,  # <5s for infrastructure
            Domain.CORE: 1.0             # <1s for core services
        }

        self.threshold = response_time_threshold or default_thresholds.get(
            domain, 5.0)

    def _validate_value(self, field: str, value: Any) -> bool:
        """Validate performance metric."""
        if not isinstance(value, (int, float)):
            raise ValidationError(
                field,
                f"Expected number, got {type(value).__name__}",
                f"Please provide a numeric value for {field}"
            )

        if value < 0:
            raise ValidationError(
                field,
                f"Negative performance values not allowed: {value}",
                f"{field} must be a positive number"
            )

        # Check domain-specific threshold
        if value > self.threshold:
            suggestions = []

            # Domain-specific suggestions
            if self.domain == Domain.SECURITY:
                suggestions.extend([
                    "Security operations must be fast for threat response",
                    "Consider optimizing database queries",
                    "Check if caching can be used"
                ])
            elif self.domain == Domain.PRODUCTIVITY:
                suggestions.extend([
                    "Productivity tools should be responsive for user focus",
                    "Consider breaking down complex operations",
                    "Add progress indicators for longer tasks"
                ])

            raise ValidationError(
                field,
                f"Performance threshold exceeded: {value}s > {self.threshold}s",
                f"{field} is too slow for {self.domain.value} domain "
                f"(took {value:.2f}s, limit is {self.threshold}s)",
                suggestions=suggestions
            )

        return True

    def _generate_progressive_hints(self, field: str, value: Any) -> List[str]:
        """Generate performance optimization hints."""
        hints = []

        if not isinstance(value, (int, float)):
            hints.append(f"Step 1: Make sure {field} is a number")
            return hints

        if value > self.threshold:
            hints.append(
                f"Step 1: Optimize to meet {self.domain.value} domain limit ({self.threshold}s)")
            hints.append("Step 2: Profile code to find bottlenecks")
            hints.append("Step 3: Consider caching or async processing")

        return hints


class ValidationSuite:
    """Complete validation suite for Mental Prosthetic Platform."""

    def __init__(self, level: ValidationLevel = ValidationLevel.NORMAL):
        self.level = level
        self.logger = get_logger(self.__class__.__name__)

        # Pre-configured validators
        self.validators = {
            'string': StringValidator(level=level),
            'email': EmailValidator(level=level),
            'url': URLValidator(level=level),
            'ip_address': IPAddressValidator(level=level),
        }

    def validate_field(
        self,
        field: str,
        value: Any,
        validator_type: str,
        **validator_kwargs
    ) -> ValidationResult:
        """Validate a single field with specified validator."""

        if validator_type not in self.validators:
            # Create custom validator
            validator_classes = {
                'string': StringValidator,
                'email': EmailValidator,
                'url': URLValidator,
                'ip_address': IPAddressValidator,
                'performance': PerformanceValidator,
            }

            if validator_type in validator_classes:
                validator = validator_classes[validator_type](
                    level=self.level,
                    **validator_kwargs
                )
            else:
                raise ValueError(f"Unknown validator type: {validator_type}")
        else:
            validator = self.validators[validator_type]

        return validator.validate(field, value)

    def validate_multiple(
        self,
        validations: Dict[str, Dict[str, Any]]
    ) -> Dict[str, ValidationResult]:
        """Validate multiple fields at once."""
        results = {}

        for field, config in validations.items():
            validator_type = config.pop('type', 'string')
            value = config.pop('value')

            try:
                results[field] = self.validate_field(
                    field, value, validator_type, **config
                )
            except Exception as e:
                results[field] = ValidationResult(
                    is_valid=False,
                    field=field,
                    value=value,
                    error_message=str(e),
                    user_message=f"Validation failed for {field}"
                )

        return results

    def validate_for_domain(
        self,
        domain: Domain,
        data: Dict[str, Any],
        validation_rules: Optional[Dict[str, Dict[str, Any]]] = None
    ) -> Dict[str, ValidationResult]:
        """Validate data for specific domain with appropriate rules."""

        results = {}
        rules = validation_rules or self._get_domain_default_rules(domain)

        for field, rule_config in rules.items():
            if field in data:
                try:
                    results[field] = self.validate_field(
                        field, data[field], **rule_config
                    )
                except Exception as e:
                    results[field] = ValidationResult(
                        is_valid=False,
                        field=field,
                        value=data.get(field),
                        error_message=str(e),
                        user_message=f"Validation failed for {field} in {domain.value} domain"
                    )

        return results

    def _get_domain_default_rules(self, domain: Domain) -> Dict[str, Dict[str, Any]]:
        """Get default validation rules for domain."""

        base_rules = {
            'name': {'validator_type': 'string', 'min_length': 1, 'max_length': 100},
            'description': {'validator_type': 'string', 'max_length': 1000},
            'url': {'validator_type': 'url'},
            'email': {'validator_type': 'email'},
        }

        if domain == Domain.SECURITY:
            # Enhanced security validation
            base_rules.update({
                'api_key': {
                    'validator_type': 'string',
                    'min_length': 16,
                    'pattern': r'^[A-Za-z0-9_-]+$'
                },
                'ip_address': {
                    'validator_type': 'ip_address',
                    'allow_private': False,
                    'allow_loopback': False
                }
            })
        elif domain == Domain.PRODUCTIVITY:
            # Productivity-focused validation
            base_rules.update({
                'workflow_name': {
                    'validator_type': 'string',
                    'min_length': 3,
                    'max_length': 50,
                    'pattern': r'^[A-Za-z0-9_\-\s]+$'
                }
            })
        elif domain == Domain.TCG:
            # Trading card game validation
            base_rules.update({
                'card_name': {
                    'validator_type': 'string',
                    'min_length': 1,
                    'max_length': 100
                },
                'mana_cost': {
                    'validator_type': 'string',
                    'pattern': r'^(\{[WUBRGXYZC0-9]+\})*$'
                }
            })

        return base_rules


# Convenience functions
def validate_string(
    field: str,
    value: str,
    min_length: Optional[int] = None,
    max_length: Optional[int] = None,
    pattern: Optional[str] = None,
    level: ValidationLevel = ValidationLevel.NORMAL
) -> ValidationResult:
    """Quick string validation."""
    validator = StringValidator(
        min_length=min_length,
        max_length=max_length,
        pattern=pattern,
        level=level
    )
    return validator.validate(field, value)


def validate_email(
    field: str,
    value: str,
    check_deliverability: bool = False,
    level: ValidationLevel = ValidationLevel.NORMAL
) -> ValidationResult:
    """Quick email validation."""
    validator = EmailValidator(
        check_deliverability=check_deliverability,
        level=level
    )
    return validator.validate(field, value)


def validate_url(
    field: str,
    value: str,
    allowed_schemes: Optional[List[str]] = None,
    level: ValidationLevel = ValidationLevel.NORMAL
) -> ValidationResult:
    """Quick URL validation."""
    validator = URLValidator(
        allowed_schemes=allowed_schemes,
        level=level
    )
    return validator.validate(field, value)


# Global validation suite instance
default_validator = ValidationSuite()


def validate_for_security_domain(data: Dict[str, Any]) -> Dict[str, ValidationResult]:
    """Validate data for security domain."""
    return default_validator.validate_for_domain(Domain.SECURITY, data)


def validate_for_productivity_domain(data: Dict[str, Any]) -> Dict[str, ValidationResult]:
    """Validate data for productivity domain."""
    return default_validator.validate_for_domain(Domain.PRODUCTIVITY, data)


def validate_for_tcg_domain(data: Dict[str, Any]) -> Dict[str, ValidationResult]:
    """Validate data for TCG domain."""
    return default_validator.validate_for_domain(Domain.TCG, data)


def validate_for_infrastructure_domain(data: Dict[str, Any]) -> Dict[str, ValidationResult]:
    """Validate data for infrastructure domain."""
    return default_validator.validate_for_domain(Domain.INFRASTRUCTURE, data)
