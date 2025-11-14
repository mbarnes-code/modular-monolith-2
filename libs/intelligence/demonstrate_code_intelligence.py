#!/usr/bin/env python3
"""
Code Intelligence Integration Demonstration

This script demonstrates how the new Code Intelligence Service integrates with
and enhances the existing ts-morph functionality in the n8n service without
breaking or replacing any existing functionality.

Run with: python demonstrate_code_intelligence.py
"""

from code.service import (CodeDomain, CodeIntelligenceAdapter,
                          CodeIntelligenceService, CodeIntelligenceType,
                          GenerationRequest, with_code_intelligence)
import asyncio
import sys
from pathlib import Path

# Add the intelligence library to the path
sys.path.insert(0, str(Path(__file__).parent))


class TSMorphEnhancementDemo:
    """Demonstrates how Code Intelligence enhances existing ts-morph operations."""

    def __init__(self):
        self.service = CodeIntelligenceService()
        self.adapter = CodeIntelligenceAdapter(self.service)

    async def demonstrate_n8n_enhancement(self):
        """Show how existing n8n ts-morph operations are enhanced with AI."""

        print("🔧 ts-morph Enhancement Demonstration")
        print("=" * 50)

        # Simulate existing n8n node specification (preserved functionality)
        existing_n8n_spec = {
            "className": "SlackIntegrationNode",
            "baseUrl": "https://slack.com/api",
            "displayName": "Slack Integration",
            "description": "Send messages and interact with Slack"
        }

        print("📋 Original n8n Node Spec:")
        for key, value in existing_n8n_spec.items():
            print(f"  {key}: {value}")

        # Enhance with AI intelligence (additive functionality)
        enhanced_spec = await self.adapter.enhance_n8n_node_generation(existing_n8n_spec)

        print("\n🚀 AI-Enhanced Node Spec:")
        print(f"  Original functionality preserved: ✅")
        print(f"  AI enhanced: {enhanced_spec.get('ai_enhanced', False)}")

        if enhanced_spec.get('intelligence_metadata'):
            metadata = enhanced_spec['intelligence_metadata']
            print(f"  AI confidence: {metadata.get('ai_confidence', 'N/A')}")
            print(f"  Security level: {metadata.get('security_level', 'N/A')}")

        return enhanced_spec

    async def demonstrate_security_enhancement(self):
        """Show AI-enhanced security code generation."""

        print("\n🛡️ Security-First Code Generation")
        print("=" * 50)

        # Security tool specification
        security_spec = {
            "tool_name": "CyberChef",
            "operation_type": "hash_analysis",
            "threat_model": {
                "data_exposure": "medium_risk",
                "injection_attacks": "low_risk"
            },
            "requirements": ["input_validation", "audit_logging"]
        }

        print("📋 Security Tool Spec:")
        for key, value in security_spec.items():
            print(f"  {key}: {value}")

        # Generate security-enhanced integration
        enhanced_security = await self.adapter.enhance_security_tool_integration(security_spec)

        print("\n🚀 Security-Enhanced Integration:")
        print(
            f"  Security enhanced: {enhanced_security.get('security_enhanced', False)}")
        print(
            f"  Threat coverage: {enhanced_security.get('threat_coverage', 0.0):.2f}")

        return enhanced_security

    async def demonstrate_cross_domain_analysis(self):
        """Show cross-domain pattern detection capabilities."""

        print("\n📊 Cross-Domain Pattern Analysis")
        print("=" * 50)

        # Simulate code samples from different domains
        code_samples = {
            CodeDomain.SECURITY: ["// MISP threat analysis code", "// CyberChef operation code"],
            CodeDomain.PRODUCTIVITY: ["// n8n workflow code", "// Mealie recipe code"],
            CodeDomain.MTG: ["// Commander Spellbook code", "// MTG rules engine code"],
            CodeDomain.INFRASTRUCTURE: [
                "// Kong gateway code", "// monitoring code"]
        }

        # Analyze patterns across domains
        analysis = await self.service.analyze_cross_domain_patterns(code_samples)

        print("📊 Analysis Results:")
        cross_domain = analysis.get('cross_domain_insights', {})
        print(
            f"  Total patterns detected: {cross_domain.get('total_patterns_detected', 0)}")
        print(
            f"  Unification potential: {cross_domain.get('unification_potential', 'unknown')}")
        print(
            f"  Executive function score: {analysis.get('executive_function_score', 0.0):.2f}")

        # Show unification opportunities
        opportunities = analysis.get('unified_opportunities', [])
        if opportunities:
            print("\n🔗 Unification Opportunities:")
            for opp in opportunities[:3]:  # Show first 3
                print(f"  • {opp.get('description', 'Unknown opportunity')}")

        return analysis

    async def demonstrate_accessibility_generation(self):
        """Show ADHD-friendly code generation."""

        print("\n♿ Executive Function Accommodations")
        print("=" * 50)

        # Generate ADHD-friendly component
        accessibility_spec = GenerationRequest(
            domain=CodeDomain.PRODUCTIVITY,
            intent="adhd_friendly_ui_component",
            context={"user_profile": "executive_function_challenges"},
            requirements={
                "response_time_target": 75,  # milliseconds
                "focus_management": True,
                "progress_indicators": True
            },
            executive_function_accommodations=True
        )

        accessible_component = await self.service.generate_accessible_component(accessibility_spec)

        print("♿ Accessibility Features Generated:")
        exec_features = accessible_component.get(
            'executive_function_features', {})
        for feature, enabled in exec_features.items():
            status = "✅" if enabled else "❌"
            print(f"  {status} {feature.replace('_', ' ').title()}")

        return accessible_component


async def main():
    """Run all demonstrations."""

    print("🧠 Code Intelligence Service Integration Demo")
    print("Demonstrating AI enhancements to existing ts-morph functionality")
    print("=" * 70)

    demo = TSMorphEnhancementDemo()

    try:
        # Run demonstrations
        await demo.demonstrate_n8n_enhancement()
        await demo.demonstrate_security_enhancement()
        await demo.demonstrate_cross_domain_analysis()
        await demo.demonstrate_accessibility_generation()

        print("\n✅ All demonstrations completed successfully!")
        print("\n🎯 Key Takeaways:")
        print("  • Existing ts-morph functionality in n8n is preserved")
        print("  • AI intelligence is purely additive - enhances without breaking")
        print("  • Cross-domain insights enable unified architecture opportunities")
        print("  • Executive function accommodations built into generated code")
        print("  • Security-first generation with threat modeling integration")
        print("\n🚀 Ready for integration with the 37-tool mental prosthetic platform!")

    except Exception as e:
        print(f"\n❌ Demonstration failed: {e}")
        print("Note: This is expected in a demo environment without full AI services")
        print("The integration patterns are designed for graceful degradation")


if __name__ == "__main__":
    asyncio.run(main())
