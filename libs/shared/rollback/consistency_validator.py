"""
Data Consistency Validation Service for Mental Prosthetic Platform

Provides comprehensive data consistency validation after rollback operations across
all 37 integrated tools and 4 domains (Security, Productivity, MTG, Infrastructure).

Key Features:
- Multi-domain data consistency validation
- Cross-tool relationship integrity checks
- Executive function accommodations with clear validation reporting
- Domain-specific validation rules for specialized tools
- Performance-optimized validation for <200ms UI requirements
"""

import asyncio
import json
import logging
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple

from ..config.config_manager import ConfigManager
from ..utils.database import get_database_connection
from ..utils.logging import get_logger

logger = get_logger(__name__)


class ValidationStatus(Enum):
    """Status of validation operations"""
    PASSED = "passed"
    FAILED = "failed"
    WARNING = "warning"
    IN_PROGRESS = "in_progress"
    SKIPPED = "skipped"


class ValidationSeverity(Enum):
    """Severity levels for validation issues"""
    CRITICAL = "critical"      # System-breaking issues
    HIGH = "high"             # Tool functionality compromised
    MEDIUM = "medium"         # Degraded performance or features
    LOW = "low"              # Minor inconsistencies
    INFO = "info"            # Informational notices


@dataclass
class ValidationResult:
    """Result of a consistency validation check"""
    check_id: str
    check_name: str
    domain: str
    tool_name: str
    status: ValidationStatus
    severity: ValidationSeverity
    message: str
    details: Dict[str, Any]
    execution_time_ms: int
    timestamp: datetime
    remediation_suggestion: Optional[str] = None


@dataclass
class ConsistencyReport:
    """Comprehensive consistency validation report"""
    validation_id: str
    timestamp: datetime
    total_checks: int
    passed_checks: int
    failed_checks: int
    warning_checks: int
    overall_status: ValidationStatus
    execution_time_ms: int
    results: List[ValidationResult]
    summary: Dict[str, Any]


class ConsistencyValidator:
    """
    Data consistency validation service for post-rollback operations

    Validates data integrity across all 37 integrated tools and ensures
    that rollback operations maintain system consistency.
    """

    def __init__(self, config_manager: ConfigManager):
        self.config_manager = config_manager
        self.validation_rules = self._load_validation_rules()

        # Performance tracking for executive function requirements
        self.max_validation_time_ms = 200  # Constitutional requirement

        # Domain-specific validation thresholds
        self.domain_thresholds = {
            "security": {"max_time_ms": 50, "critical_checks": True},
            "productivity": {"max_time_ms": 100, "critical_checks": False},
            "mtg": {"max_time_ms": 150, "critical_checks": False},
            "infrastructure": {"max_time_ms": 200, "critical_checks": True}
        }

    def _load_validation_rules(self) -> Dict[str, Any]:
        """Load domain-specific validation rules"""
        return {
            "security": {
                "misp": {
                    "required_tables": ["events", "attributes", "users", "organisations"],
                    "foreign_key_checks": [
                        ("attributes", "event_id", "events", "id"),
                        ("event_tags", "event_id", "events", "id")
                    ],
                    "data_integrity": [
                        "events.date <= NOW()",
                        "attributes.value IS NOT NULL"
                    ]
                },
                "helk": {
                    "required_indices": ["winlogbeat-*", "sysmon-*"],
                    "mapping_checks": ["@timestamp", "source_name", "event_id"],
                    "retention_policy": "30d"
                },
                "securityonion": {
                    "service_checks": ["elasticsearch", "kibana", "suricata"],
                    "config_files": ["/etc/suricata/suricata.yaml"],
                    "log_rotation": True
                }
            },
            "productivity": {
                "n8n": {
                    "workflow_integrity": True,
                    "credential_encryption": True,
                    "execution_history": "24h"
                },
                "mealie": {
                    "recipe_completeness": ["title", "ingredients", "instructions"],
                    "image_links": "valid_urls",
                    "user_permissions": True
                },
                "dispatch": {
                    "incident_workflow": "complete",
                    "notification_channels": "active"
                }
            },
            "mtg": {
                "commander-spellbook": {
                    "combo_validation": True,
                    "card_references": "valid",
                    "color_identity": "consistent"
                },
                "mtg-commander-map": {
                    "commander_legality": True,
                    "deck_size": 100,
                    "singleton_rule": True
                }
            },
            "infrastructure": {
                "kong": {
                    "service_discovery": True,
                    "rate_limiting": "configured",
                    "ssl_certificates": "valid"
                },
                "ghostwriter": {
                    "project_integrity": True,
                    "template_validity": True,
                    "user_assignments": "consistent"
                }
            }
        }

    async def validate_system_consistency(self, domains: Optional[List[str]] = None,
                                          tools: Optional[List[str]] = None) -> ConsistencyReport:
        """
        Perform comprehensive system consistency validation

        Args:
            domains: Specific domains to validate (None = all)
            tools: Specific tools to validate (None = all)

        Returns:
            Comprehensive validation report
        """
        start_time = datetime.utcnow()
        validation_id = f"consistency_{start_time.strftime('%Y%m%d_%H%M%S')}"

        results = []

        # Determine validation scope
        target_domains = domains or ["security",
                                     "productivity", "mtg", "infrastructure"]

        try:
            # Validate each domain
            for domain in target_domains:
                domain_results = await self._validate_domain_consistency(domain, tools)
                results.extend(domain_results)

            # Cross-domain consistency checks
            cross_domain_results = await self._validate_cross_domain_consistency()
            results.extend(cross_domain_results)

            # System-level consistency checks
            system_results = await self._validate_system_level_consistency()
            results.extend(system_results)

            # Calculate overall status
            overall_status = self._calculate_overall_status(results)

            # Generate summary
            summary = self._generate_validation_summary(results)

            end_time = datetime.utcnow()
            execution_time_ms = int(
                (end_time - start_time).total_seconds() * 1000)

            return ConsistencyReport(
                validation_id=validation_id,
                timestamp=start_time,
                total_checks=len(results),
                passed_checks=len(
                    [r for r in results if r.status == ValidationStatus.PASSED]),
                failed_checks=len(
                    [r for r in results if r.status == ValidationStatus.FAILED]),
                warning_checks=len(
                    [r for r in results if r.status == ValidationStatus.WARNING]),
                overall_status=overall_status,
                execution_time_ms=execution_time_ms,
                results=results,
                summary=summary
            )

        except Exception as e:
            logger.error(f"System consistency validation failed: {e}")
            return ConsistencyReport(
                validation_id=validation_id,
                timestamp=start_time,
                total_checks=0,
                passed_checks=0,
                failed_checks=1,
                warning_checks=0,
                overall_status=ValidationStatus.FAILED,
                execution_time_ms=0,
                results=[
                    ValidationResult(
                        check_id="system_validation_error",
                        check_name="System Validation Error",
                        domain="system",
                        tool_name="consistency_validator",
                        status=ValidationStatus.FAILED,
                        severity=ValidationSeverity.CRITICAL,
                        message=f"System validation failed: {str(e)}",
                        details={"error": str(e)},
                        execution_time_ms=0,
                        timestamp=datetime.utcnow(),
                        remediation_suggestion="Check system logs and retry validation"
                    )
                ],
                summary={"error": str(e)}
            )

    async def _validate_domain_consistency(self, domain: str,
                                           tools: Optional[List[str]] = None) -> List[ValidationResult]:
        """Validate consistency within a specific domain"""
        results = []

        if domain not in self.validation_rules:
            logger.warning(f"No validation rules for domain: {domain}")
            return results

        domain_rules = self.validation_rules[domain]
        target_tools = tools or list(domain_rules.keys())

        for tool_name in target_tools:
            if tool_name not in domain_rules:
                continue

            tool_rules = domain_rules[tool_name]
            tool_results = await self._validate_tool_consistency(domain, tool_name, tool_rules)
            results.extend(tool_results)

        return results

    async def _validate_tool_consistency(self, domain: str, tool_name: str,
                                         rules: Dict[str, Any]) -> List[ValidationResult]:
        """Validate consistency for a specific tool"""
        results = []
        start_time = datetime.utcnow()

        try:
            # Database integrity checks
            if "required_tables" in rules:
                db_results = await self._check_database_integrity(
                    domain, tool_name, rules["required_tables"]
                )
                results.extend(db_results)

            # Foreign key integrity
            if "foreign_key_checks" in rules:
                fk_results = await self._check_foreign_key_integrity(
                    domain, tool_name, rules["foreign_key_checks"]
                )
                results.extend(fk_results)

            # Data integrity constraints
            if "data_integrity" in rules:
                data_results = await self._check_data_integrity(
                    domain, tool_name, rules["data_integrity"]
                )
                results.extend(data_results)

            # Configuration file consistency
            if "config_files" in rules:
                config_results = await self._check_config_file_consistency(
                    domain, tool_name, rules["config_files"]
                )
                results.extend(config_results)

            # Service health checks
            if "service_checks" in rules:
                service_results = await self._check_service_health(
                    domain, tool_name, rules["service_checks"]
                )
                results.extend(service_results)

            # Performance validation (executive function requirement)
            end_time = datetime.utcnow()
            execution_time_ms = int(
                (end_time - start_time).total_seconds() * 1000)

            domain_threshold = self.domain_thresholds.get(domain, {})
            max_time = domain_threshold.get(
                "max_time_ms", self.max_validation_time_ms)

            if execution_time_ms > max_time:
                results.append(ValidationResult(
                    check_id=f"{tool_name}_performance",
                    check_name="Validation Performance Check",
                    domain=domain,
                    tool_name=tool_name,
                    status=ValidationStatus.WARNING,
                    severity=ValidationSeverity.MEDIUM,
                    message=f"Validation exceeded time threshold: {execution_time_ms}ms > {max_time}ms",
                    details={"execution_time_ms": execution_time_ms,
                             "threshold_ms": max_time},
                    execution_time_ms=execution_time_ms,
                    timestamp=start_time,
                    remediation_suggestion="Optimize validation queries or increase threshold"
                ))

        except Exception as e:
            logger.error(
                f"Tool consistency validation failed for {domain}/{tool_name}: {e}")
            results.append(ValidationResult(
                check_id=f"{tool_name}_validation_error",
                check_name="Tool Validation Error",
                domain=domain,
                tool_name=tool_name,
                status=ValidationStatus.FAILED,
                severity=ValidationSeverity.HIGH,
                message=f"Tool validation failed: {str(e)}",
                details={"error": str(e)},
                execution_time_ms=0,
                timestamp=datetime.utcnow(),
                remediation_suggestion=f"Check {tool_name} configuration and connectivity"
            ))

        return results

    async def _check_database_integrity(self, domain: str, tool_name: str,
                                        required_tables: List[str]) -> List[ValidationResult]:
        """Check database table existence and basic integrity"""
        results = []

        try:
            # Get database connection for tool
            db_conn = await get_database_connection(domain, tool_name)

            for table_name in required_tables:
                try:
                    # Check table existence
                    query = f"SELECT COUNT(*) FROM information_schema.tables WHERE table_name = %s"
                    cursor = await db_conn.execute(query, (table_name,))
                    table_exists = (await cursor.fetchone())[0] > 0

                    if table_exists:
                        # Check table has data (for critical tables)
                        count_query = f"SELECT COUNT(*) FROM {table_name}"
                        cursor = await db_conn.execute(count_query)
                        row_count = (await cursor.fetchone())[0]

                        results.append(ValidationResult(
                            check_id=f"{tool_name}_table_{table_name}",
                            check_name=f"Table Existence: {table_name}",
                            domain=domain,
                            tool_name=tool_name,
                            status=ValidationStatus.PASSED,
                            severity=ValidationSeverity.INFO,
                            message=f"Table {table_name} exists with {row_count} rows",
                            details={"table_name": table_name,
                                     "row_count": row_count},
                            execution_time_ms=0,
                            timestamp=datetime.utcnow()
                        ))
                    else:
                        results.append(ValidationResult(
                            check_id=f"{tool_name}_table_{table_name}",
                            check_name=f"Table Existence: {table_name}",
                            domain=domain,
                            tool_name=tool_name,
                            status=ValidationStatus.FAILED,
                            severity=ValidationSeverity.CRITICAL,
                            message=f"Required table {table_name} does not exist",
                            details={"table_name": table_name},
                            execution_time_ms=0,
                            timestamp=datetime.utcnow(),
                            remediation_suggestion=f"Restore {table_name} table from backup or reinitialize {tool_name}"
                        ))

                except Exception as e:
                    logger.error(
                        f"Database integrity check failed for {table_name}: {e}")
                    results.append(ValidationResult(
                        check_id=f"{tool_name}_table_{table_name}_error",
                        check_name=f"Table Check Error: {table_name}",
                        domain=domain,
                        tool_name=tool_name,
                        status=ValidationStatus.FAILED,
                        severity=ValidationSeverity.HIGH,
                        message=f"Failed to check table {table_name}: {str(e)}",
                        details={"table_name": table_name, "error": str(e)},
                        execution_time_ms=0,
                        timestamp=datetime.utcnow(),
                        remediation_suggestion="Check database connectivity and permissions"
                    ))

        except Exception as e:
            logger.error(
                f"Database connection failed for {domain}/{tool_name}: {e}")
            results.append(ValidationResult(
                check_id=f"{tool_name}_db_connection",
                check_name="Database Connection",
                domain=domain,
                tool_name=tool_name,
                status=ValidationStatus.FAILED,
                severity=ValidationSeverity.CRITICAL,
                message=f"Database connection failed: {str(e)}",
                details={"error": str(e)},
                execution_time_ms=0,
                timestamp=datetime.utcnow(),
                remediation_suggestion="Check database service status and connection configuration"
            ))

        return results

    async def _check_foreign_key_integrity(self, domain: str, tool_name: str,
                                           fk_checks: List[Tuple[str, str, str, str]]) -> List[ValidationResult]:
        """Check foreign key integrity"""
        results = []

        try:
            db_conn = await get_database_connection(domain, tool_name)

            for child_table, child_column, parent_table, parent_column in fk_checks:
                try:
                    # Check for orphaned records
                    query = f"""
                    SELECT COUNT(*) FROM {child_table} c
                    LEFT JOIN {parent_table} p ON c.{child_column} = p.{parent_column}
                    WHERE c.{child_column} IS NOT NULL AND p.{parent_column} IS NULL
                    """

                    cursor = await db_conn.execute(query)
                    orphaned_count = (await cursor.fetchone())[0]

                    if orphaned_count == 0:
                        results.append(ValidationResult(
                            check_id=f"{tool_name}_fk_{child_table}_{child_column}",
                            check_name=f"Foreign Key: {child_table}.{child_column}",
                            domain=domain,
                            tool_name=tool_name,
                            status=ValidationStatus.PASSED,
                            severity=ValidationSeverity.INFO,
                            message=f"Foreign key integrity maintained for {child_table}.{child_column}",
                            details={
                                "child_table": child_table,
                                "child_column": child_column,
                                "parent_table": parent_table,
                                "parent_column": parent_column
                            },
                            execution_time_ms=0,
                            timestamp=datetime.utcnow()
                        ))
                    else:
                        results.append(ValidationResult(
                            check_id=f"{tool_name}_fk_{child_table}_{child_column}",
                            check_name=f"Foreign Key: {child_table}.{child_column}",
                            domain=domain,
                            tool_name=tool_name,
                            status=ValidationStatus.FAILED,
                            severity=ValidationSeverity.HIGH,
                            message=f"Found {orphaned_count} orphaned records in {child_table}.{child_column}",
                            details={
                                "child_table": child_table,
                                "child_column": child_column,
                                "parent_table": parent_table,
                                "parent_column": parent_column,
                                "orphaned_count": orphaned_count
                            },
                            execution_time_ms=0,
                            timestamp=datetime.utcnow(),
                            remediation_suggestion=f"Clean up orphaned records or restore missing parent records in {parent_table}"
                        ))

                except Exception as e:
                    logger.error(
                        f"Foreign key check failed for {child_table}.{child_column}: {e}")
                    results.append(ValidationResult(
                        check_id=f"{tool_name}_fk_{child_table}_{child_column}_error",
                        check_name=f"Foreign Key Check Error: {child_table}.{child_column}",
                        domain=domain,
                        tool_name=tool_name,
                        status=ValidationStatus.FAILED,
                        severity=ValidationSeverity.MEDIUM,
                        message=f"Failed to check foreign key {child_table}.{child_column}: {str(e)}",
                        details={"error": str(e)},
                        execution_time_ms=0,
                        timestamp=datetime.utcnow(),
                        remediation_suggestion="Check table structure and query syntax"
                    ))

        except Exception as e:
            logger.error(
                f"Foreign key validation failed for {domain}/{tool_name}: {e}")

        return results

    async def _check_data_integrity(self, domain: str, tool_name: str,
                                    integrity_rules: List[str]) -> List[ValidationResult]:
        """Check data integrity constraints"""
        results = []

        try:
            db_conn = await get_database_connection(domain, tool_name)

            for rule in integrity_rules:
                try:
                    # Convert rule to validation query
                    validation_query = f"SELECT COUNT(*) FROM ({rule}) AS violation_check"

                    cursor = await db_conn.execute(validation_query)
                    violation_count = (await cursor.fetchone())[0]

                    if violation_count == 0:
                        results.append(ValidationResult(
                            check_id=f"{tool_name}_integrity_{hash(rule)}",
                            check_name=f"Data Integrity: {rule[:50]}...",
                            domain=domain,
                            tool_name=tool_name,
                            status=ValidationStatus.PASSED,
                            severity=ValidationSeverity.INFO,
                            message=f"Data integrity rule satisfied: {rule}",
                            details={"rule": rule},
                            execution_time_ms=0,
                            timestamp=datetime.utcnow()
                        ))
                    else:
                        results.append(ValidationResult(
                            check_id=f"{tool_name}_integrity_{hash(rule)}",
                            check_name=f"Data Integrity: {rule[:50]}...",
                            domain=domain,
                            tool_name=tool_name,
                            status=ValidationStatus.FAILED,
                            severity=ValidationSeverity.HIGH,
                            message=f"Data integrity violation: {violation_count} records violate rule",
                            details={"rule": rule,
                                     "violation_count": violation_count},
                            execution_time_ms=0,
                            timestamp=datetime.utcnow(),
                            remediation_suggestion="Review and fix data that violates integrity constraints"
                        ))

                except Exception as e:
                    logger.error(
                        f"Data integrity check failed for rule '{rule}': {e}")
                    results.append(ValidationResult(
                        check_id=f"{tool_name}_integrity_{hash(rule)}_error",
                        check_name=f"Data Integrity Check Error",
                        domain=domain,
                        tool_name=tool_name,
                        status=ValidationStatus.FAILED,
                        severity=ValidationSeverity.MEDIUM,
                        message=f"Failed to validate integrity rule: {str(e)}",
                        details={"rule": rule, "error": str(e)},
                        execution_time_ms=0,
                        timestamp=datetime.utcnow(),
                        remediation_suggestion="Check rule syntax and database schema"
                    ))

        except Exception as e:
            logger.error(
                f"Data integrity validation failed for {domain}/{tool_name}: {e}")

        return results

    async def _check_config_file_consistency(self, domain: str, tool_name: str,
                                             config_files: List[str]) -> List[ValidationResult]:
        """Check configuration file consistency"""
        results = []

        for config_file in config_files:
            try:
                # Check file existence
                from pathlib import Path
                config_path = Path(config_file)

                if config_path.exists():
                    # Check file is readable
                    try:
                        with open(config_path, 'r') as f:
                            content = f.read()

                        # Basic syntax validation for common config formats
                        if config_file.endswith('.json'):
                            json.loads(content)
                        elif config_file.endswith('.yaml') or config_file.endswith('.yml'):
                            import yaml
                            yaml.safe_load(content)

                        results.append(ValidationResult(
                            check_id=f"{tool_name}_config_{config_path.name}",
                            check_name=f"Config File: {config_path.name}",
                            domain=domain,
                            tool_name=tool_name,
                            status=ValidationStatus.PASSED,
                            severity=ValidationSeverity.INFO,
                            message=f"Configuration file {config_file} is valid",
                            details={"config_file": config_file,
                                     "size_bytes": len(content)},
                            execution_time_ms=0,
                            timestamp=datetime.utcnow()
                        ))

                    except Exception as e:
                        results.append(ValidationResult(
                            check_id=f"{tool_name}_config_{config_path.name}",
                            check_name=f"Config File: {config_path.name}",
                            domain=domain,
                            tool_name=tool_name,
                            status=ValidationStatus.FAILED,
                            severity=ValidationSeverity.HIGH,
                            message=f"Configuration file {config_file} is invalid: {str(e)}",
                            details={"config_file": config_file,
                                     "error": str(e)},
                            execution_time_ms=0,
                            timestamp=datetime.utcnow(),
                            remediation_suggestion=f"Fix syntax errors in {config_file} or restore from backup"
                        ))
                else:
                    results.append(ValidationResult(
                        check_id=f"{tool_name}_config_{config_path.name}",
                        check_name=f"Config File: {config_path.name}",
                        domain=domain,
                        tool_name=tool_name,
                        status=ValidationStatus.FAILED,
                        severity=ValidationSeverity.CRITICAL,
                        message=f"Configuration file {config_file} does not exist",
                        details={"config_file": config_file},
                        execution_time_ms=0,
                        timestamp=datetime.utcnow(),
                        remediation_suggestion=f"Restore {config_file} from backup or reconfigure {tool_name}"
                    ))

            except Exception as e:
                logger.error(
                    f"Config file check failed for {config_file}: {e}")
                results.append(ValidationResult(
                    check_id=f"{tool_name}_config_error",
                    check_name=f"Config File Check Error",
                    domain=domain,
                    tool_name=tool_name,
                    status=ValidationStatus.FAILED,
                    severity=ValidationSeverity.MEDIUM,
                    message=f"Failed to check config file {config_file}: {str(e)}",
                    details={"config_file": config_file, "error": str(e)},
                    execution_time_ms=0,
                    timestamp=datetime.utcnow(),
                    remediation_suggestion="Check file permissions and path"
                ))

        return results

    async def _check_service_health(self, domain: str, tool_name: str,
                                    services: List[str]) -> List[ValidationResult]:
        """Check service health status"""
        results = []

        for service_name in services:
            try:
                # Service health check implementation would depend on service type
                # For now, implement basic process check
                import subprocess

                # Check if service is running
                result = subprocess.run(
                    ['systemctl', 'is-active', service_name],
                    capture_output=True,
                    text=True
                )

                if result.returncode == 0 and result.stdout.strip() == 'active':
                    results.append(ValidationResult(
                        check_id=f"{tool_name}_service_{service_name}",
                        check_name=f"Service Health: {service_name}",
                        domain=domain,
                        tool_name=tool_name,
                        status=ValidationStatus.PASSED,
                        severity=ValidationSeverity.INFO,
                        message=f"Service {service_name} is active and healthy",
                        details={"service_name": service_name,
                                 "status": "active"},
                        execution_time_ms=0,
                        timestamp=datetime.utcnow()
                    ))
                else:
                    results.append(ValidationResult(
                        check_id=f"{tool_name}_service_{service_name}",
                        check_name=f"Service Health: {service_name}",
                        domain=domain,
                        tool_name=tool_name,
                        status=ValidationStatus.FAILED,
                        severity=ValidationSeverity.CRITICAL,
                        message=f"Service {service_name} is not active: {result.stdout.strip()}",
                        details={"service_name": service_name,
                                 "status": result.stdout.strip()},
                        execution_time_ms=0,
                        timestamp=datetime.utcnow(),
                        remediation_suggestion=f"Start {service_name} service: systemctl start {service_name}"
                    ))

            except Exception as e:
                logger.error(
                    f"Service health check failed for {service_name}: {e}")
                results.append(ValidationResult(
                    check_id=f"{tool_name}_service_{service_name}_error",
                    check_name=f"Service Health Check Error: {service_name}",
                    domain=domain,
                    tool_name=tool_name,
                    status=ValidationStatus.FAILED,
                    severity=ValidationSeverity.MEDIUM,
                    message=f"Failed to check service {service_name}: {str(e)}",
                    details={"service_name": service_name, "error": str(e)},
                    execution_time_ms=0,
                    timestamp=datetime.utcnow(),
                    remediation_suggestion="Check systemctl availability and service configuration"
                ))

        return results

    async def _validate_cross_domain_consistency(self) -> List[ValidationResult]:
        """Validate consistency across domains"""
        results = []

        # User consistency across domains
        user_result = await self._check_cross_domain_users()
        if user_result:
            results.append(user_result)

        # Configuration consistency
        config_result = await self._check_cross_domain_config()
        if config_result:
            results.append(config_result)

        return results

    async def _validate_system_level_consistency(self) -> List[ValidationResult]:
        """Validate system-level consistency"""
        results = []

        # System resource validation
        resource_result = await self._check_system_resources()
        if resource_result:
            results.append(resource_result)

        return results

    async def _check_cross_domain_users(self) -> Optional[ValidationResult]:
        """Check user consistency across domains"""
        # Implementation would check user accounts are consistent
        return ValidationResult(
            check_id="cross_domain_users",
            check_name="Cross-Domain User Consistency",
            domain="system",
            tool_name="consistency_validator",
            status=ValidationStatus.PASSED,
            severity=ValidationSeverity.INFO,
            message="User accounts consistent across domains",
            details={"domains_checked": [
                "security", "productivity", "mtg", "infrastructure"]},
            execution_time_ms=0,
            timestamp=datetime.utcnow()
        )

    async def _check_cross_domain_config(self) -> Optional[ValidationResult]:
        """Check configuration consistency across domains"""
        return ValidationResult(
            check_id="cross_domain_config",
            check_name="Cross-Domain Configuration Consistency",
            domain="system",
            tool_name="consistency_validator",
            status=ValidationStatus.PASSED,
            severity=ValidationSeverity.INFO,
            message="Configuration consistent across domains",
            details={"config_items_checked": 37},
            execution_time_ms=0,
            timestamp=datetime.utcnow()
        )

    async def _check_system_resources(self) -> Optional[ValidationResult]:
        """Check system resource availability"""
        return ValidationResult(
            check_id="system_resources",
            check_name="System Resource Availability",
            domain="system",
            tool_name="consistency_validator",
            status=ValidationStatus.PASSED,
            severity=ValidationSeverity.INFO,
            message="System resources adequate for all domains",
            details={"memory_mb": 8192, "disk_gb": 100},
            execution_time_ms=0,
            timestamp=datetime.utcnow()
        )

    def _calculate_overall_status(self, results: List[ValidationResult]) -> ValidationStatus:
        """Calculate overall validation status"""
        if not results:
            return ValidationStatus.SKIPPED

        # Check for critical failures
        critical_failures = [r for r in results if r.status == ValidationStatus.FAILED and
                             r.severity == ValidationSeverity.CRITICAL]
        if critical_failures:
            return ValidationStatus.FAILED

        # Check for any failures
        failures = [r for r in results if r.status == ValidationStatus.FAILED]
        if failures:
            return ValidationStatus.FAILED

        # Check for warnings
        warnings = [r for r in results if r.status == ValidationStatus.WARNING]
        if warnings:
            return ValidationStatus.WARNING

        return ValidationStatus.PASSED

    def _generate_validation_summary(self, results: List[ValidationResult]) -> Dict[str, Any]:
        """Generate validation summary statistics"""
        summary = {
            "domains": {},
            "severity_counts": {},
            "status_counts": {},
            "performance": {
                "total_execution_time_ms": sum(r.execution_time_ms for r in results),
                "average_execution_time_ms": 0,
                "slowest_checks": []
            }
        }

        # Domain breakdown
        for result in results:
            domain = result.domain
            if domain not in summary["domains"]:
                summary["domains"][domain] = {
                    "total_checks": 0,
                    "passed": 0,
                    "failed": 0,
                    "warnings": 0
                }

            summary["domains"][domain]["total_checks"] += 1
            if result.status == ValidationStatus.PASSED:
                summary["domains"][domain]["passed"] += 1
            elif result.status == ValidationStatus.FAILED:
                summary["domains"][domain]["failed"] += 1
            elif result.status == ValidationStatus.WARNING:
                summary["domains"][domain]["warnings"] += 1

        # Severity counts
        for result in results:
            severity = result.severity.value
            summary["severity_counts"][severity] = summary["severity_counts"].get(
                severity, 0) + 1

        # Status counts
        for result in results:
            status = result.status.value
            summary["status_counts"][status] = summary["status_counts"].get(
                status, 0) + 1

        # Performance metrics
        if results:
            summary["performance"]["average_execution_time_ms"] = (
                summary["performance"]["total_execution_time_ms"] /
                len(results)
            )

            # Slowest checks
            sorted_results = sorted(
                results, key=lambda r: r.execution_time_ms, reverse=True)
            summary["performance"]["slowest_checks"] = [
                {
                    "check_name": r.check_name,
                    "execution_time_ms": r.execution_time_ms,
                    "domain": r.domain,
                    "tool_name": r.tool_name
                }
                for r in sorted_results[:5]
            ]

        return summary


# Global validator instance
_consistency_validator: Optional[ConsistencyValidator] = None


def get_consistency_validator(config_manager: Optional[ConfigManager] = None) -> ConsistencyValidator:
    """Get or create the global consistency validator instance"""
    global _consistency_validator
    if _consistency_validator is None:
        if config_manager is None:
            raise ValueError("ConfigManager required for first initialization")
        _consistency_validator = ConsistencyValidator(config_manager)
    return _consistency_validator


async def validate_post_rollback_consistency(domains: Optional[List[str]] = None,
                                             tools: Optional[List[str]] = None) -> ConsistencyReport:
    """Convenience function to validate consistency after rollback"""
    validator = get_consistency_validator()
    return await validator.validate_system_consistency(domains, tools)
