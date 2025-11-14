"""
Code Intelligence Module

AI-Enhanced TypeScript AST manipulation and code generation capabilities
that extend and enhance existing functionality without replacing core features.

This module provides:
1. AI-driven code generation with domain expertise
2. Cross-domain pattern analysis and unification
3. Executive function accommodations for ADHD-friendly development
4. Security-first code generation with threat modeling
5. Enhanced refactoring suggestions with modernization
6. **NEW: Generalized TypeScript AST tools from n8n Node CLI**

Key Integration Points:
- n8n Node CLI Enhancement (extends existing ts-morph functionality)
- Security Tool Code Generation (AI-driven secure coding)
- Cross-Domain Pattern Detection (unified architecture insights)
- Accessibility Code Generation (executive function support)
- **Enhanced TypeScript AST Manipulation (generalized from n8n CLI)**
- **Template-based Code Generation with AI enhancement**
- **Batch Processing with parallel execution and rollback**

Zero Dependencies Promise:
All existing applications continue working without this service.
Code intelligence is purely additive and enhances capabilities when available.

TypeScript Tools:
The following TypeScript files provide enhanced AST manipulation:
- ast-utils.ts: Core AST manipulation functions (generalized from n8n)
- domain-operations.ts: Domain-specific operations for all project types
- types.ts: Comprehensive type definitions
- index.ts: Main entry point for TypeScript tools
- package.json: Dependencies including ts-morph ^26.0.0
"""

from pathlib import Path
from typing import Any, Dict

from .service import (AccessibilityFeatures, CodeDomain,
                      CodeIntelligenceAdapter, CodeIntelligenceService,
                      CodeIntelligenceType, GenerationRequest, RefactoringPlan,
                      with_code_intelligence)


def typescript_tools_available() -> bool:
    """Check if TypeScript AST manipulation tools are available."""
    try:
        import subprocess
        result = subprocess.run(
            ['node', '--version'], capture_output=True, text=True, check=False
        )
        return result.returncode == 0
    except (FileNotFoundError, subprocess.SubprocessError):
        return False


class TypeScriptToolsBridge:
    """
    Bridge between Python AI service and TypeScript AST tools.

    Provides Python interface to TypeScript AST manipulation tools,
    allowing seamless integration between AI analysis and AST operations.
    """

    @staticmethod
    def run_ast_operation(
        operation: str, file_path: str, **kwargs
    ) -> Dict[str, Any]:
        """Run TypeScript AST operation from Python."""
        if not typescript_tools_available():
            return {
                "success": False,
                "error": "TypeScript tools not available - Node.js required",
                "fallback": "Use CodeIntelligenceService for analysis"
            }

        try:
            import json
            import subprocess

            # Run TypeScript AST operation
            cmd = ['node', '-e', f"""
                const tools = require('./index.ts');
                const result = tools.{operation}(
                    '{file_path}', {json.dumps(kwargs)}
                );
                console.log(JSON.stringify(result));
            """]

            result = subprocess.run(
                cmd, capture_output=True, text=True, check=False,
                cwd=Path(__file__).parent
            )

            if result.returncode == 0:
                return json.loads(result.stdout)
            else:
                return {"success": False, "error": result.stderr}

        except (subprocess.SubprocessError, json.JSONDecodeError) as e:
            return {"success": False, "error": str(e)}


__all__ = [
    # Python AI Service
    "CodeIntelligenceService",
    "CodeIntelligenceAdapter",
    "CodeDomain",
    "CodeIntelligenceType",
    "GenerationRequest",
    "RefactoringPlan",
    "AccessibilityFeatures",
    "with_code_intelligence",

    # TypeScript Integration
    "TypeScriptToolsBridge",
    "typescript_tools_available",
]

__version__ = "1.0.0"
__author__ = "Mental Prosthetic Platform Team"
__description__ = "AI-Enhanced Code Intelligence for TypeScript AST"
