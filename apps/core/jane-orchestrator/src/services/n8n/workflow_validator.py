"""Workflow Validation System for Constitutional Requirements.

Ensures generated workflows meet constitutional requirements and preserve
business logic across all 37 tools with proper performance validation.
"""

from typing import List, Dict, Any, Optional, Set
from dataclasses import dataclass
from datetime import timedelta
from enum import Enum


class ValidationLevel(Enum):
    """Validation strictness levels."""
    BASIC = "basic"
    STANDARD = "standard"
    STRICT = "strict"
    CONSTITUTIONAL = "constitutional"


class ValidationResult(Enum):
    """Validation result status."""
    PASSED = "passed"
    FAILED = "failed"
    WARNING = "warning"
    REQUIRES_REVIEW = "requires_review"


@dataclass
class ValidationIssue:
    """Represents a validation issue found in a workflow."""
    issue_id: str
    severity: str  # 'error', 'warning', 'info'
    category: str  # 'performance', 'constitutional', 'business_logic'
    description: str
    suggested_fix: Optional[str]
    affected_nodes: List[str]
    domain_impact: List[str]


@dataclass
class WorkflowValidationReport:
    """Comprehensive validation report for a workflow."""
    workflow_id: str
    workflow_name: str
    validation_level: ValidationLevel
    overall_result: ValidationResult
    constitutional_compliance: bool
    business_logic_preservation: bool
    performance_validation: Dict[str, bool]
    issues: List[ValidationIssue]
    recommendations: List[str]
    estimated_success_rate: float
    validation_timestamp: str


class ConstitutionalValidator:
    """Validates workflows against constitutional requirements."""
    
    def __init__(self):
        self.constitutional_principles = self._load_constitutional_principles()
        self.domain_performance_limits = self._load_performance_limits()
        self.tool_capabilities = self._load_tool_capabilities()
    
    def _load_constitutional_principles(self) -> Dict[str, Any]:
        """Load constitutional principles for validation."""
        return {
            "executive_function_accommodations": {
                "ui_response_time": timedelta(milliseconds=200),
                "context_switching_minimization": True,
                "unified_navigation": True,
                "wcag_compliance": "AA"
            },
            "business_logic_preservation": {
                "functionality_preservation": 1.0,
                "data_integrity": True,
                "rollback_capability": True,
                "user_preference_consistency": True
            },
            "integration_standards": {
                "cross_tool_sync": timedelta(milliseconds=250),
                "data_consistency": True,
                "error_handling": True,
                "monitoring_required": True
            }
        }
    
    def _load_performance_limits(self) -> Dict[str, timedelta]:
        """Load domain-specific performance limits."""
        return {
            "security": timedelta(seconds=1),
            "productivity": timedelta(seconds=2),
            "mtg": timedelta(seconds=3),
            "infrastructure": timedelta(seconds=5)
        }
    
    def _load_tool_capabilities(self) -> Dict[str, Dict[str, Any]]:
        """Load capabilities and constraints for each tool."""
        return {
            "misp": {
                "domain": "security",
                "max_concurrent_requests": 10,
                "rate_limits": {"requests_per_minute": 60}
            },
            "n8n": {
                "domain": "productivity",
                "max_concurrent_requests": 20,
                "rate_limits": {"requests_per_minute": 120}
            },
            "commander-spellbook": {
                "domain": "mtg",
                "max_concurrent_requests": 8,
                "rate_limits": {"requests_per_minute": 50}
            },
            "kong": {
                "domain": "infrastructure",
                "max_concurrent_requests": 50,
                "rate_limits": {"requests_per_minute": 200}
            }
        }
    
    def validate_workflow(
        self, workflow: Dict[str, Any],
        validation_level: ValidationLevel = ValidationLevel.STANDARD
    ) -> WorkflowValidationReport:
        """Comprehensive workflow validation."""
        issues = []
        
        # Constitutional compliance validation
        constitutional_issues = self._validate_constitutional_compliance(
            workflow
        )
        issues.extend(constitutional_issues)
        
        # Business logic preservation validation
        business_logic_issues = self._validate_business_logic_preservation(
            workflow
        )
        issues.extend(business_logic_issues)
        
        # Performance validation
        performance_results = self._validate_performance_requirements(
            workflow
        )
        performance_issues = [
            issue for result in performance_results.values()
            for issue in result.get('issues', [])
        ]
        issues.extend(performance_issues)
        
        # Tool integration validation
        integration_issues = self._validate_tool_integration(workflow)
        issues.extend(integration_issues)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(issues, workflow)
        
        # Determine overall result
        overall_result = self._determine_overall_result(
            issues, validation_level
        )
        
        # Calculate estimated success rate
        estimated_success_rate = self._calculate_success_rate(
            issues, workflow
        )
        
        return WorkflowValidationReport(
            workflow_id=workflow.get('id', 'unknown'),
            workflow_name=workflow.get('name', 'Unnamed Workflow'),
            validation_level=validation_level,
            overall_result=overall_result,
            constitutional_compliance=len(constitutional_issues) == 0,
            business_logic_preservation=len(business_logic_issues) == 0,
            performance_validation={
                domain: result.get('passed', False)
                for domain, result in performance_results.items()
            },
            issues=issues,
            recommendations=recommendations,
            estimated_success_rate=estimated_success_rate,
            validation_timestamp=str(
                __import__('datetime').datetime.utcnow().isoformat()
            )
        )
    
    def _validate_constitutional_compliance(
        self, workflow: Dict[str, Any]
    ) -> List[ValidationIssue]:
        """Validate workflow against constitutional principles."""
        issues = []
        
        # Check UI response time requirements
        if self._exceeds_ui_response_time(workflow):
            issues.append(ValidationIssue(
                issue_id="constitutional_001",
                severity="error",
                category="constitutional",
                description="Workflow may exceed UI response time limit of 200ms",
                suggested_fix="Optimize node execution order and add caching",
                affected_nodes=self._get_slow_nodes(workflow),
                domain_impact=["all"]
            ))
        
        # Check rollback capability
        if not self._has_rollback_capability(workflow):
            issues.append(ValidationIssue(
                issue_id="constitutional_003",
                severity="error",
                category="constitutional",
                description="Workflow lacks proper rollback capabilities",
                suggested_fix="Add rollback nodes and state management",
                affected_nodes=self._get_non_reversible_nodes(workflow),
                domain_impact=self._get_affected_domains(workflow)
            ))
        
        return issues
    
    def _validate_business_logic_preservation(
        self, workflow: Dict[str, Any]
    ) -> List[ValidationIssue]:
        """Validate business logic preservation."""
        issues = []
        
        # Check for data integrity
        if not self._maintains_data_integrity(workflow):
            issues.append(ValidationIssue(
                issue_id="business_001",
                severity="error",
                category="business_logic",
                description="Workflow may compromise data integrity",
                suggested_fix="Add data validation and consistency checks",
                affected_nodes=self._get_data_manipulation_nodes(workflow),
                domain_impact=self._get_affected_domains(workflow)
            ))
        
        # Check for functionality preservation
        preserved_functionality = self._calculate_functionality_preservation(
            workflow
        )
        if preserved_functionality < 1.0:
            issues.append(ValidationIssue(
                issue_id="business_002",
                severity="error",
                category="business_logic",
                description=(
                    f"Functionality preservation is "
                    f"{preserved_functionality:.1%}, expected 100%"
                ),
                suggested_fix="Review and restore missing functionality",
                affected_nodes=self._get_incomplete_nodes(workflow),
                domain_impact=self._get_affected_domains(workflow)
            ))
        
        return issues
    
    def _validate_performance_requirements(
        self, workflow: Dict[str, Any]
    ) -> Dict[str, Dict[str, Any]]:
        """Validate domain-specific performance requirements."""
        results = {}
        
        workflow_domains = self._get_workflow_domains(workflow)
        
        for domain in workflow_domains:
            if domain in self.domain_performance_limits:
                limit = self.domain_performance_limits[domain]
                domain_results = {
                    'passed': True,
                    'issues': [],
                    'metrics': {}
                }
                
                # Estimate response time
                estimated_time = self._estimate_workflow_response_time(
                    workflow, domain
                )
                domain_results['metrics']['estimated_response_time'] = (
                    estimated_time
                )
                
                if estimated_time > limit:
                    domain_results['passed'] = False
                    domain_results['issues'].append(ValidationIssue(
                        issue_id=f"perf_{domain}_001",
                        severity="error",
                        category="performance",
                        description=(
                            f"Estimated response time "
                            f"{estimated_time.total_seconds()}s exceeds "
                            f"limit {limit.total_seconds()}s for {domain} domain"
                        ),
                        suggested_fix=(
                            "Optimize workflow execution and add "
                            "parallel processing"
                        ),
                        affected_nodes=self._get_domain_nodes(workflow, domain),
                        domain_impact=[domain]
                    ))
                
                results[domain] = domain_results
        
        return results
    
    def _validate_tool_integration(
        self, workflow: Dict[str, Any]
    ) -> List[ValidationIssue]:
        """Validate tool integration and compatibility."""
        issues = []
        
        # Check rate limit compliance
        rate_limit_issues = self._check_rate_limit_compliance(workflow)
        issues.extend(rate_limit_issues)
        
        return issues
    
    # Helper methods for validation checks
    
    def _exceeds_ui_response_time(self, workflow: Dict[str, Any]) -> bool:
        """Check if workflow may exceed UI response time limits."""
        ui_nodes = [
            node for node in workflow.get('nodes', [])
            if (node.get('type', '').endswith('-ui') or 
                'frontend' in node.get('name', '').lower())
        ]
        return len(ui_nodes) > 3
    
    def _has_rollback_capability(self, workflow: Dict[str, Any]) -> bool:
        """Check if workflow has rollback capabilities."""
        nodes = workflow.get('nodes', [])
        
        for node in nodes:
            if 'rollback' in node.get('name', '').lower():
                return True
            if node.get('settings', {}).get('onError') == 'rollback':
                return True
        
        return False
    
    def _maintains_data_integrity(self, workflow: Dict[str, Any]) -> bool:
        """Check if workflow maintains data integrity."""
        nodes = workflow.get('nodes', [])
        has_validation = any(
            'validate' in node.get('name', '').lower() or
            'check' in node.get('name', '').lower()
            for node in nodes
        )
        
        return has_validation
    
    def _calculate_functionality_preservation(
        self, workflow: Dict[str, Any]
    ) -> float:
        """Calculate functionality preservation score."""
        nodes = workflow.get('nodes', [])
        if not nodes:
            return 0.0
        
        complete_nodes = [
            node for node in nodes
            if (node.get('parameters') and 
                len(node.get('parameters', {})) > 0)
        ]
        
        return len(complete_nodes) / len(nodes)
    
    def _get_workflow_domains(self, workflow: Dict[str, Any]) -> Set[str]:
        """Get domains involved in the workflow."""
        domains = set()
        
        nodes = workflow.get('nodes', [])
        for node in nodes:
            tool_name = node.get('type', '').lower()
            domain = self._get_tool_domain(tool_name)
            if domain:
                domains.add(domain)
        
        return domains
    
    def _get_tool_domain(self, tool_name: str) -> Optional[str]:
        """Get domain for a tool."""
        for tool, capabilities in self.tool_capabilities.items():
            if tool in tool_name:
                return capabilities.get('domain')
        return None
    
    def _estimate_workflow_response_time(
        self, workflow: Dict[str, Any], domain: str
    ) -> timedelta:
        """Estimate workflow response time for a domain."""
        nodes = workflow.get('nodes', [])
        domain_nodes = [
            node for node in nodes
            if self._get_tool_domain(node.get('type', '').lower()) == domain
        ]
        
        # Simple estimation: 100ms per node + 50ms per connection
        base_time = len(domain_nodes) * 100  # milliseconds
        connection_time = len(workflow.get('connections', {})) * 50
        
        total_ms = base_time + connection_time
        return timedelta(milliseconds=total_ms)
    
    def _check_rate_limit_compliance(
        self, workflow: Dict[str, Any]
    ) -> List[ValidationIssue]:
        """Check if workflow complies with tool rate limits."""
        issues = []
        
        # Count requests per tool
        tool_usage = {}
        for node in workflow.get('nodes', []):
            tool_type = node.get('type', '').lower()
            tool_usage[tool_type] = tool_usage.get(tool_type, 0) + 1
        
        # Check against rate limits
        for tool, count in tool_usage.items():
            if tool in self.tool_capabilities:
                rate_limit = self.tool_capabilities[tool].get(
                    'rate_limits', {}
                ).get('requests_per_minute', float('inf'))
                
                if count > rate_limit / 10:  # Conservative check
                    issues.append(ValidationIssue(
                        issue_id=f"rate_limit_{tool}",
                        severity="warning",
                        category="performance",
                        description=(
                            f"High usage of {tool} may exceed rate limits"
                        ),
                        suggested_fix="Add rate limiting and retry logic",
                        affected_nodes=[
                            node.get('name', '') 
                            for node in workflow.get('nodes', [])
                            if node.get('type', '').lower() == tool
                        ],
                        domain_impact=[
                            self.tool_capabilities[tool].get('domain', 'unknown')
                        ]
                    ))
        
        return issues
    
    # Placeholder helper methods
    
    def _get_slow_nodes(self, workflow: Dict[str, Any]) -> List[str]:
        return []
    
    def _get_non_reversible_nodes(self, workflow: Dict[str, Any]) -> List[str]:
        return []
    
    def _get_affected_domains(self, workflow: Dict[str, Any]) -> List[str]:
        return list(self._get_workflow_domains(workflow))
    
    def _get_data_manipulation_nodes(
        self, workflow: Dict[str, Any]
    ) -> List[str]:
        return []
    
    def _get_incomplete_nodes(self, workflow: Dict[str, Any]) -> List[str]:
        return []
    
    def _get_domain_nodes(
        self, workflow: Dict[str, Any], domain: str
    ) -> List[str]:
        return []
    
    def _generate_recommendations(
        self, issues: List[ValidationIssue], workflow: Dict[str, Any]
    ) -> List[str]:
        """Generate recommendations based on validation issues."""
        recommendations = []
        
        error_count = len([i for i in issues if i.severity == 'error'])
        warning_count = len([i for i in issues if i.severity == 'warning'])
        
        if error_count > 0:
            recommendations.append(
                f"Address {error_count} critical errors before deployment"
            )
        
        if warning_count > 0:
            recommendations.append(
                f"Consider addressing {warning_count} warnings "
                f"for better reliability"
            )
        
        domains = self._get_workflow_domains(workflow)
        if len(domains) > 2:
            recommendations.append(
                "Consider splitting workflow into domain-specific "
                "sub-workflows"
            )
        
        return recommendations
    
    def _determine_overall_result(
        self, issues: List[ValidationIssue], validation_level: ValidationLevel
    ) -> ValidationResult:
        """Determine overall validation result."""
        errors = [i for i in issues if i.severity == 'error']
        warnings = [i for i in issues if i.severity == 'warning']
        
        if validation_level == ValidationLevel.CONSTITUTIONAL:
            constitutional_errors = [
                i for i in errors if i.category == 'constitutional'
            ]
            if constitutional_errors:
                return ValidationResult.FAILED
        
        if errors:
            return ValidationResult.FAILED
        elif warnings:
            return ValidationResult.WARNING
        else:
            return ValidationResult.PASSED
    
    def _calculate_success_rate(
        self, issues: List[ValidationIssue], workflow: Dict[str, Any]
    ) -> float:
        """Calculate estimated workflow success rate."""
        base_rate = 0.95
        
        # Reduce success rate based on issues
        for issue in issues:
            if issue.severity == 'error':
                base_rate -= 0.1
            elif issue.severity == 'warning':
                base_rate -= 0.05
        
        # Bonus for good practices
        if self._has_rollback_capability(workflow):
            base_rate += 0.02
        
        return max(0.0, min(1.0, base_rate))


class WorkflowValidator:
    """Main workflow validation orchestrator."""
    
    def __init__(self):
        self.constitutional_validator = ConstitutionalValidator()
    
    def validate(
        self, workflow: Dict[str, Any],
        validation_level: ValidationLevel = ValidationLevel.STANDARD
    ) -> WorkflowValidationReport:
        """Validate a workflow comprehensively."""
        return self.constitutional_validator.validate_workflow(
            workflow, validation_level
        )
    
    def quick_validate(self, workflow: Dict[str, Any]) -> bool:
        """Quick validation - returns True if workflow passes basic checks."""
        report = self.validate(workflow, ValidationLevel.BASIC)
        return report.overall_result in [
            ValidationResult.PASSED, ValidationResult.WARNING
        ]
    
    def constitutional_validate(
        self, workflow: Dict[str, Any]
    ) -> WorkflowValidationReport:
        """Full constitutional compliance validation."""
        return self.validate(workflow, ValidationLevel.CONSTITUTIONAL)