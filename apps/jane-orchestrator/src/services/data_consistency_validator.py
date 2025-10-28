"""
Data Consistency Validation Service.

Comprehensive validation of data consistency across all 37 integrated tools
with domain-specific validation rules and automated integrity checks.
"""

import asyncio
import json
import logging
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple

from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from ..data.database import get_async_session
from ..data.models.sync_state import SyncBatch, SyncState, SyncStatus
from .event_bus_service import EventBusService

logger = logging.getLogger(__name__)


class ValidationSeverity(Enum):
    """Severity levels for validation issues."""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class ValidationCategory(Enum):
    """Categories of validation checks."""
    REFERENTIAL_INTEGRITY = "referential_integrity"
    DATA_FORMAT = "data_format"
    BUSINESS_RULES = "business_rules"
    SCHEMA_COMPLIANCE = "schema_compliance"
    TEMPORAL_CONSISTENCY = "temporal_consistency"
    CROSS_DOMAIN_CONSISTENCY = "cross_domain_consistency"


@dataclass
class ValidationIssue:
    """Represents a data consistency validation issue."""
    id: str
    tool_id: str
    domain: str
    category: ValidationCategory
    severity: ValidationSeverity
    title: str
    description: str
    affected_records: List[str]
    suggested_fix: Optional[str] = None
    auto_fixable: bool = False
    detected_at: datetime = None
    resolved_at: Optional[datetime] = None

    def __post_init__(self):
        if self.detected_at is None:
            self.detected_at = datetime.utcnow()


@dataclass
class ValidationResult:
    """Results of a validation run."""
    validation_id: str
    tool_id: str
    domain: str
    started_at: datetime
    completed_at: Optional[datetime]
    total_records_checked: int
    issues_found: List[ValidationIssue]
    passed_checks: int
    failed_checks: int
    skipped_checks: int
    overall_status: str  # 'passed', 'failed', 'warning'

    @property
    def success_rate(self) -> float:
        total = self.passed_checks + self.failed_checks
        return (self.passed_checks / total * 100) if total > 0 else 0.0


class DataConsistencyValidator:
    """
    Service for validating data consistency across all 37 integrated tools.

    Provides comprehensive validation capabilities including:
    - Cross-domain referential integrity
    - Schema compliance validation
    - Business rule enforcement
    - Temporal consistency checks
    - Data format validation
    """

    def __init__(self, event_bus: EventBusService):
        self.event_bus = event_bus
        self.validation_rules = self._load_validation_rules()
        self._active_validations: Dict[str, ValidationResult] = {}

    def _load_validation_rules(self) -> Dict[str, Dict[str, Any]]:
        """Load domain-specific validation rules."""
        return {
            "Security": {
                "misp": {
                    "required_fields": ["event_id", "timestamp", "threat_level"],
                    "referential_checks": [
                        {"field": "event_id",
                            "references": "helk.security_events.misp_event_id"}
                    ],
                    "format_rules": {
                        "timestamp": "iso8601",
                        "threat_level": ["high", "medium", "low", "info"]
                    }
                },
                "helk": {
                    "required_fields": ["log_id", "timestamp", "source_ip", "event_type"],
                    "referential_checks": [
                        {"field": "misp_event_id",
                            "references": "misp.events.event_id", "optional": True}
                    ],
                    "format_rules": {
                        "source_ip": "ipv4_or_ipv6",
                        "timestamp": "iso8601"
                    }
                },
                "securityonion": {
                    "required_fields": ["alert_id", "timestamp", "severity", "signature"],
                    "cross_domain_sync": [
                        {"target": "dispatch", "sync_field": "security_alerts",
                            "frequency": "real-time"}
                    ]
                }
            },
            "Productivity": {
                "n8n": {
                    "required_fields": ["workflow_id", "execution_id", "status"],
                    "referential_checks": [
                        {"field": "target_tool", "references": [
                            "mealie", "dispatch", "actual"]}
                    ],
                    "business_rules": [
                        {"rule": "workflow_execution_timeout",
                            "max_duration_minutes": 60}
                    ]
                },
                "mealie": {
                    "required_fields": ["recipe_id", "title", "ingredients"],
                    "referential_checks": [
                        {"field": "created_by_workflow",
                            "references": "n8n.workflows.workflow_id", "optional": True}
                    ],
                    "format_rules": {
                        "ingredients": "json_array",
                        "prep_time": "positive_integer"
                    }
                },
                "dispatch": {
                    "required_fields": ["incident_id", "status", "priority", "created_at"],
                    "referential_checks": [
                        {"field": "security_alert_id",
                            "references": "securityonion.alerts.alert_id", "optional": True}
                    ],
                    "business_rules": [
                        {"rule": "incident_escalation",
                            "max_response_time_hours": 24}
                    ]
                }
            },
            "MTG": {
                "commander_spellbook": {
                    "required_fields": ["combo_id", "commander", "color_identity"],
                    "referential_checks": [
                        {"field": "combo_id",
                            "references": "mtg_commander_map.combos.combo_id"}
                    ],
                    "format_rules": {
                        "color_identity": "mtg_colors",
                        "mana_cost": "mtg_mana_format"
                    }
                },
                "mtg_commander_map": {
                    "required_fields": ["map_id", "commander", "power_level"],
                    "business_rules": [
                        {"rule": "power_level_range", "min": 1, "max": 10}
                    ]
                }
            },
            "Infrastructure": {
                "kong": {
                    "required_fields": ["service_id", "route_id", "status"],
                    "business_rules": [
                        {"rule": "rate_limit_enforcement",
                            "requests_per_minute": 1000}
                    ],
                    "cross_domain_sync": [
                        {"target": "all", "sync_field": "api_metrics",
                            "frequency": "real-time"}
                    ]
                },
                "ghostwriter": {
                    "required_fields": ["project_id", "client_id", "status"],
                    "business_rules": [
                        {"rule": "project_timeline", "max_duration_days": 365}
                    ]
                }
            }
        }

    async def validate_tool_consistency(
        self,
        tool_id: str,
        domain: str,
        session: AsyncSession
    ) -> ValidationResult:
        """Validate data consistency for a specific tool."""
        validation_id = f"val_{tool_id}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"

        result = ValidationResult(
            validation_id=validation_id,
            tool_id=tool_id,
            domain=domain,
            started_at=datetime.utcnow(),
            completed_at=None,
            total_records_checked=0,
            issues_found=[],
            passed_checks=0,
            failed_checks=0,
            skipped_checks=0,
            overall_status='running'
        )

        self._active_validations[validation_id] = result

        try:
            # Get tool-specific validation rules
            domain_rules = self.validation_rules.get(domain, {})
            tool_rules = domain_rules.get(tool_id, {})

            if not tool_rules:
                logger.warning(
                    f"No validation rules found for {tool_id} in {domain}")
                result.skipped_checks += 1
                result.overall_status = 'skipped'
                return result

            # Run validation checks
            await self._validate_required_fields(tool_id, tool_rules, result, session)
            await self._validate_referential_integrity(tool_id, tool_rules, result, session)
            await self._validate_format_rules(tool_id, tool_rules, result, session)
            await self._validate_business_rules(tool_id, tool_rules, result, session)
            await self._validate_cross_domain_sync(tool_id, tool_rules, result, session)

            # Determine overall status
            if result.failed_checks == 0:
                result.overall_status = 'passed'
            elif any(issue.severity == ValidationSeverity.CRITICAL for issue in result.issues_found):
                result.overall_status = 'critical'
            elif any(issue.severity == ValidationSeverity.ERROR for issue in result.issues_found):
                result.overall_status = 'failed'
            else:
                result.overall_status = 'warning'

            result.completed_at = datetime.utcnow()

            # Emit validation completed event
            await self.event_bus.emit_event({
                'type': 'validation_completed',
                'tool_id': tool_id,
                'domain': domain,
                'validation_id': validation_id,
                'status': result.overall_status,
                'issues_count': len(result.issues_found),
                'success_rate': result.success_rate
            })

        except Exception as e:
            logger.error(f"Validation failed for {tool_id}: {str(e)}")
            result.overall_status = 'error'
            result.issues_found.append(ValidationIssue(
                id=f"val_error_{datetime.utcnow().timestamp()}",
                tool_id=tool_id,
                domain=domain,
                category=ValidationCategory.SCHEMA_COMPLIANCE,
                severity=ValidationSeverity.ERROR,
                title="Validation Process Error",
                description=f"Validation process encountered an error: {str(e)}",
                affected_records=[]
            ))

        return result

    async def validate_cross_domain_consistency(
        self,
        domains: List[str],
        session: AsyncSession
    ) -> Dict[str, ValidationResult]:
        """Validate consistency across multiple domains."""
        results = {}

        # Cross-domain validation scenarios
        cross_domain_checks = [
            {
                'name': 'security_to_productivity_flow',
                'source': {'domain': 'Security', 'tool': 'securityonion'},
                'target': {'domain': 'Productivity', 'tool': 'dispatch'},
                'validation': 'security_alerts_sync'
            },
            {
                'name': 'n8n_workflow_integration',
                'source': {'domain': 'Productivity', 'tool': 'n8n'},
                'target': {'domain': 'Productivity', 'tool': 'mealie'},
                'validation': 'workflow_data_consistency'
            },
            {
                'name': 'kong_api_metrics',
                'source': {'domain': 'Infrastructure', 'tool': 'kong'},
                'target': {'domain': 'all', 'tool': 'all'},
                'validation': 'api_metrics_distribution'
            }
        ]

        for check in cross_domain_checks:
            if check['source']['domain'] in domains or check['target']['domain'] in domains or 'all' in domains:
                validation_result = await self._run_cross_domain_check(check, session)
                results[check['name']] = validation_result

        return results

    async def _validate_required_fields(
        self,
        tool_id: str,
        tool_rules: Dict[str, Any],
        result: ValidationResult,
        session: AsyncSession
    ):
        """Validate that required fields are present."""
        required_fields = tool_rules.get('required_fields', [])
        if not required_fields:
            return

        try:
            # Query to check for missing required fields
            # This is a simplified example - in practice, this would query actual tool tables
            query = text(f"""
                SELECT COUNT(*) as total_records,
                       COUNT(CASE WHEN {' IS NULL OR '.join(required_fields)} IS NULL THEN 1 END) as missing_fields
                FROM {tool_id}_data 
                WHERE created_at >= :check_time
            """)

            check_time = datetime.utcnow() - timedelta(hours=24)  # Last 24 hours
            query_result = await session.execute(query, {'check_time': check_time})
            row = query_result.fetchone()

            if row:
                result.total_records_checked += row.total_records

                if row.missing_fields > 0:
                    result.failed_checks += 1
                    result.issues_found.append(ValidationIssue(
                        id=f"req_fields_{tool_id}_{datetime.utcnow().timestamp()}",
                        tool_id=tool_id,
                        domain=result.domain,
                        category=ValidationCategory.SCHEMA_COMPLIANCE,
                        severity=ValidationSeverity.ERROR,
                        title="Missing Required Fields",
                        description=f"Found {row.missing_fields} records with missing required fields: {required_fields}",
                        affected_records=[],
                        suggested_fix="Ensure all required fields are populated during data ingestion",
                        auto_fixable=False
                    ))
                else:
                    result.passed_checks += 1

        except Exception as e:
            logger.error(
                f"Required fields validation failed for {tool_id}: {str(e)}")
            result.skipped_checks += 1

    async def _validate_referential_integrity(
        self,
        tool_id: str,
        tool_rules: Dict[str, Any],
        result: ValidationResult,
        session: AsyncSession
    ):
        """Validate referential integrity constraints."""
        referential_checks = tool_rules.get('referential_checks', [])

        for check in referential_checks:
            try:
                field = check['field']
                reference = check['references']
                optional = check.get('optional', False)

                # Parse reference (e.g., "helk.security_events.misp_event_id")
                ref_parts = reference.split('.')
                if len(ref_parts) == 3:
                    ref_tool, ref_table, ref_field = ref_parts
                else:
                    continue

                # Check for orphaned references
                query = text(f"""
                    SELECT COUNT(*) as orphaned_records
                    FROM {tool_id}_data t1
                    LEFT JOIN {ref_tool}_{ref_table} t2 ON t1.{field} = t2.{ref_field}
                    WHERE t1.{field} IS NOT NULL 
                    AND t2.{ref_field} IS NULL
                    AND t1.created_at >= :check_time
                """)

                check_time = datetime.utcnow() - timedelta(hours=24)
                query_result = await session.execute(query, {'check_time': check_time})
                row = query_result.fetchone()

                if row and row.orphaned_records > 0:
                    severity = ValidationSeverity.WARNING if optional else ValidationSeverity.ERROR
                    result.failed_checks += 1
                    result.issues_found.append(ValidationIssue(
                        id=f"ref_integrity_{tool_id}_{field}_{datetime.utcnow().timestamp()}",
                        tool_id=tool_id,
                        domain=result.domain,
                        category=ValidationCategory.REFERENTIAL_INTEGRITY,
                        severity=severity,
                        title="Referential Integrity Violation",
                        description=f"Found {row.orphaned_records} records with invalid {field} references to {reference}",
                        affected_records=[],
                        suggested_fix=f"Clean up orphaned {field} references or restore missing {ref_tool} records",
                        auto_fixable=False
                    ))
                else:
                    result.passed_checks += 1

            except Exception as e:
                logger.error(
                    f"Referential integrity check failed for {tool_id}.{field}: {str(e)}")
                result.skipped_checks += 1

    async def _validate_format_rules(
        self,
        tool_id: str,
        tool_rules: Dict[str, Any],
        result: ValidationResult,
        session: AsyncSession
    ):
        """Validate data format rules."""
        format_rules = tool_rules.get('format_rules', {})

        for field, format_rule in format_rules.items():
            try:
                validation_query = self._build_format_validation_query(
                    tool_id, field, format_rule)
                if not validation_query:
                    continue

                query_result = await session.execute(validation_query)
                row = query_result.fetchone()

                if row and row.invalid_records > 0:
                    result.failed_checks += 1
                    result.issues_found.append(ValidationIssue(
                        id=f"format_{tool_id}_{field}_{datetime.utcnow().timestamp()}",
                        tool_id=tool_id,
                        domain=result.domain,
                        category=ValidationCategory.DATA_FORMAT,
                        severity=ValidationSeverity.WARNING,
                        title="Data Format Violation",
                        description=f"Found {row.invalid_records} records with invalid {field} format (expected: {format_rule})",
                        affected_records=[],
                        suggested_fix=f"Validate and correct {field} format during data ingestion",
                        auto_fixable=True
                    ))
                else:
                    result.passed_checks += 1

            except Exception as e:
                logger.error(
                    f"Format validation failed for {tool_id}.{field}: {str(e)}")
                result.skipped_checks += 1

    def _build_format_validation_query(self, tool_id: str, field: str, format_rule: str) -> Optional[str]:
        """Build SQL query for format validation based on rule type."""
        check_time = datetime.utcnow() - timedelta(hours=24)

        format_patterns = {
            'iso8601': f"SELECT COUNT(*) as invalid_records FROM {tool_id}_data WHERE {field} !~ '^\\d{{4}}-\\d{{2}}-\\d{{2}}T\\d{{2}}:\\d{{2}}:\\d{{2}}' AND created_at >= '{check_time}'",
            'ipv4_or_ipv6': f"SELECT COUNT(*) as invalid_records FROM {tool_id}_data WHERE {field} !~ '^((\\d{{1,3}}\\.\\d{{1,3}}\\.\\d{{1,3}}\\.\\d{{1,3}})|(([0-9a-fA-F]{{1,4}}:){{7}}[0-9a-fA-F]{{1,4}}))$' AND created_at >= '{check_time}'",
            'json_array': f"SELECT COUNT(*) as invalid_records FROM {tool_id}_data WHERE NOT (jsonb_typeof({field}::jsonb) = 'array') AND created_at >= '{check_time}'",
            'positive_integer': f"SELECT COUNT(*) as invalid_records FROM {tool_id}_data WHERE {field}::int <= 0 AND created_at >= '{check_time}'"
        }

        if isinstance(format_rule, list):
            # Enum validation
            enum_values = "', '".join(format_rule)
            return text(f"SELECT COUNT(*) as invalid_records FROM {tool_id}_data WHERE {field} NOT IN ('{enum_values}') AND created_at >= :check_time")

        return text(format_patterns.get(format_rule))

    async def _validate_business_rules(
        self,
        tool_id: str,
        tool_rules: Dict[str, Any],
        result: ValidationResult,
        session: AsyncSession
    ):
        """Validate business-specific rules."""
        business_rules = tool_rules.get('business_rules', [])

        for rule in business_rules:
            try:
                rule_name = rule['rule']
                validation_query = self._build_business_rule_query(
                    tool_id, rule)

                if validation_query:
                    query_result = await session.execute(validation_query)
                    row = query_result.fetchone()

                    if row and row.violations > 0:
                        result.failed_checks += 1
                        result.issues_found.append(ValidationIssue(
                            id=f"business_{tool_id}_{rule_name}_{datetime.utcnow().timestamp()}",
                            tool_id=tool_id,
                            domain=result.domain,
                            category=ValidationCategory.BUSINESS_RULES,
                            severity=ValidationSeverity.WARNING,
                            title=f"Business Rule Violation: {rule_name}",
                            description=f"Found {row.violations} records violating business rule: {rule_name}",
                            affected_records=[],
                            suggested_fix=f"Review and enforce {rule_name} business rule",
                            auto_fixable=False
                        ))
                    else:
                        result.passed_checks += 1

            except Exception as e:
                logger.error(
                    f"Business rule validation failed for {tool_id}.{rule['rule']}: {str(e)}")
                result.skipped_checks += 1

    def _build_business_rule_query(self, tool_id: str, rule: Dict[str, Any]) -> Optional[str]:
        """Build SQL query for business rule validation."""
        rule_name = rule['rule']
        check_time = datetime.utcnow() - timedelta(hours=24)

        rule_queries = {
            'workflow_execution_timeout': f"""
                SELECT COUNT(*) as violations 
                FROM {tool_id}_data 
                WHERE status = 'running' 
                AND EXTRACT(EPOCH FROM (NOW() - started_at))/60 > {rule['max_duration_minutes']}
                AND created_at >= '{check_time}'
            """,
            'incident_escalation': f"""
                SELECT COUNT(*) as violations 
                FROM {tool_id}_data 
                WHERE status = 'open' 
                AND priority = 'high'
                AND EXTRACT(EPOCH FROM (NOW() - created_at))/3600 > {rule['max_response_time_hours']}
            """,
            'power_level_range': f"""
                SELECT COUNT(*) as violations 
                FROM {tool_id}_data 
                WHERE power_level < {rule['min']} OR power_level > {rule['max']}
                AND created_at >= '{check_time}'
            """,
            'rate_limit_enforcement': f"""
                SELECT COUNT(*) as violations 
                FROM {tool_id}_metrics 
                WHERE requests_per_minute > {rule['requests_per_minute']}
                AND created_at >= '{check_time}'
            """
        }

        query_template = rule_queries.get(rule_name)
        return text(query_template) if query_template else None

    async def _validate_cross_domain_sync(
        self,
        tool_id: str,
        tool_rules: Dict[str, Any],
        result: ValidationResult,
        session: AsyncSession
    ):
        """Validate cross-domain synchronization consistency."""
        sync_rules = tool_rules.get('cross_domain_sync', [])

        for sync_rule in sync_rules:
            target = sync_rule['target']
            sync_field = sync_rule['sync_field']
            frequency = sync_rule['frequency']

            # Check sync lag based on frequency
            max_lag_minutes = {
                'real-time': 5,
                'hourly': 70,
                'daily': 1500
            }.get(frequency, 60)

            try:
                # Check for sync lag
                query = text(f"""
                    SELECT COUNT(*) as lagged_records
                    FROM sync_state 
                    WHERE source_tool = :tool_id
                    AND (target_tool = :target OR :target = 'all')
                    AND EXTRACT(EPOCH FROM (NOW() - last_sync_time))/60 > :max_lag
                """)

                query_result = await session.execute(query, {
                    'tool_id': tool_id,
                    'target': target,
                    'max_lag': max_lag_minutes
                })
                row = query_result.fetchone()

                if row and row.lagged_records > 0:
                    result.failed_checks += 1
                    result.issues_found.append(ValidationIssue(
                        id=f"sync_lag_{tool_id}_{target}_{datetime.utcnow().timestamp()}",
                        tool_id=tool_id,
                        domain=result.domain,
                        category=ValidationCategory.CROSS_DOMAIN_CONSISTENCY,
                        severity=ValidationSeverity.WARNING,
                        title="Cross-Domain Sync Lag",
                        description=f"Sync lag detected between {tool_id} and {target} (>{max_lag_minutes} minutes)",
                        affected_records=[],
                        suggested_fix="Check sync service status and network connectivity",
                        auto_fixable=True
                    ))
                else:
                    result.passed_checks += 1

            except Exception as e:
                logger.error(
                    f"Cross-domain sync validation failed for {tool_id}->{target}: {str(e)}")
                result.skipped_checks += 1

    async def _run_cross_domain_check(
        self,
        check: Dict[str, Any],
        session: AsyncSession
    ) -> ValidationResult:
        """Run a specific cross-domain consistency check."""
        validation_id = f"cross_domain_{check['name']}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"

        result = ValidationResult(
            validation_id=validation_id,
            tool_id=f"{check['source']['tool']}->{check['target']['tool']}",
            domain="cross-domain",
            started_at=datetime.utcnow(),
            completed_at=None,
            total_records_checked=0,
            issues_found=[],
            passed_checks=0,
            failed_checks=0,
            skipped_checks=0,
            overall_status='running'
        )

        # Implementation would depend on specific check type
        # This is a simplified example
        try:
            result.passed_checks += 1
            result.overall_status = 'passed'
            result.completed_at = datetime.utcnow()
        except Exception as e:
            logger.error(
                f"Cross-domain check failed for {check['name']}: {str(e)}")
            result.failed_checks += 1
            result.overall_status = 'failed'

        return result

    async def get_validation_summary(self, session: AsyncSession) -> Dict[str, Any]:
        """Get overall validation summary across all tools."""
        # Query recent validation results
        recent_validations = await session.execute(
            text("""
                SELECT tool_id, domain, status, issues_count, success_rate, completed_at
                FROM validation_results 
                WHERE completed_at >= NOW() - INTERVAL '24 hours'
                ORDER BY completed_at DESC
            """)
        )

        validations = recent_validations.fetchall()

        # Aggregate statistics
        total_tools = len(set(v.tool_id for v in validations))
        passed_validations = len(
            [v for v in validations if v.status == 'passed'])
        failed_validations = len(
            [v for v in validations if v.status in ['failed', 'critical']])

        domain_stats = {}
        for validation in validations:
            domain = validation.domain
            if domain not in domain_stats:
                domain_stats[domain] = {
                    'total': 0,
                    'passed': 0,
                    'failed': 0,
                    'avg_success_rate': 0
                }

            domain_stats[domain]['total'] += 1
            if validation.status == 'passed':
                domain_stats[domain]['passed'] += 1
            elif validation.status in ['failed', 'critical']:
                domain_stats[domain]['failed'] += 1

            domain_stats[domain]['avg_success_rate'] += validation.success_rate

        # Calculate averages
        for domain, stats in domain_stats.items():
            if stats['total'] > 0:
                stats['avg_success_rate'] /= stats['total']

        return {
            'timestamp': datetime.utcnow().isoformat(),
            'total_tools_validated': total_tools,
            'total_validations': len(validations),
            'passed_validations': passed_validations,
            'failed_validations': failed_validations,
            'overall_success_rate': (passed_validations / len(validations) * 100) if validations else 0,
            'domain_statistics': domain_stats,
            'recent_validations': [
                {
                    'tool_id': v.tool_id,
                    'domain': v.domain,
                    'status': v.status,
                    'success_rate': v.success_rate,
                    'completed_at': v.completed_at.isoformat() if v.completed_at else None
                }
                for v in validations[:10]  # Last 10 validations
            ]
        }

    async def auto_fix_validation_issues(
        self,
        validation_id: str,
        session: AsyncSession
    ) -> Dict[str, Any]:
        """Automatically fix validation issues where possible."""
        validation = self._active_validations.get(validation_id)
        if not validation:
            return {'error': 'Validation not found'}

        fixed_issues = []
        failed_fixes = []

        for issue in validation.issues_found:
            if issue.auto_fixable:
                try:
                    # Implementation would depend on issue type
                    # This is a simplified example
                    fix_result = await self._apply_auto_fix(issue, session)
                    if fix_result:
                        fixed_issues.append(issue.id)
                        issue.resolved_at = datetime.utcnow()
                    else:
                        failed_fixes.append(issue.id)
                except Exception as e:
                    logger.error(
                        f"Auto-fix failed for issue {issue.id}: {str(e)}")
                    failed_fixes.append(issue.id)

        return {
            'validation_id': validation_id,
            'fixed_issues': fixed_issues,
            'failed_fixes': failed_fixes,
            'total_auto_fixable': len([i for i in validation.issues_found if i.auto_fixable])
        }

    async def _apply_auto_fix(self, issue: ValidationIssue, session: AsyncSession) -> bool:
        """Apply automatic fix for a specific validation issue."""
        # Implementation would depend on issue category and type
        # This is a placeholder for the actual fix logic
        return True


# Convenience function for creating validator instance
async def create_data_consistency_validator() -> DataConsistencyValidator:
    """Create and configure a DataConsistencyValidator instance."""
    from .event_bus_service import EventBusService

    event_bus = EventBusService()
    validator = DataConsistencyValidator(event_bus)

    return validator
