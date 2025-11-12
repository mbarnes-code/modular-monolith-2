"""Tests for cross-tool interaction sequence detection (T101).

This test validates the InteractionAnalyzer implementation for detecting
cross-tool patterns that can be automated through n8n workflows.
"""

from datetime import datetime, timedelta

import pytest
from apps.jane_orchestrator.src.services.n8n.interaction_analyzer import (
    DomainType, InteractionAnalyzer, InteractionType, ToolInteraction,
    analyze_user_workflow_patterns, create_tool_interaction)


class TestInteractionAnalyzer:
    """Test cross-tool interaction analysis capabilities."""

    def setup_method(self):
        """Set up test environment."""
        self.analyzer = InteractionAnalyzer()
        self.user_id = "test_user_001"

    def test_domain_classification(self):
        """Test that tools are correctly classified into domains."""
        # Security domain tools
        assert self.analyzer._classify_tool_domain(
            "misp") == DomainType.SECURITY
        assert self.analyzer._classify_tool_domain(
            "helk") == DomainType.SECURITY
        assert self.analyzer._classify_tool_domain(
            "cyberchef") == DomainType.SECURITY

        # Productivity domain tools
        assert self.analyzer._classify_tool_domain(
            "n8n") == DomainType.PRODUCTIVITY
        assert self.analyzer._classify_tool_domain(
            "mealie") == DomainType.PRODUCTIVITY
        assert self.analyzer._classify_tool_domain(
            "dispatch") == DomainType.PRODUCTIVITY

        # MTG domain tools
        assert self.analyzer._classify_tool_domain(
            "commander-spellbook") == DomainType.MTG
        assert self.analyzer._classify_tool_domain(
            "mtg-commander-map") == DomainType.MTG

        # Infrastructure domain tools
        assert self.analyzer._classify_tool_domain(
            "kong") == DomainType.INFRASTRUCTURE
        assert self.analyzer._classify_tool_domain(
            "ghostwriter") == DomainType.INFRASTRUCTURE

        # Unknown tool defaults to infrastructure
        assert self.analyzer._classify_tool_domain(
            "unknown_tool") == DomainType.INFRASTRUCTURE

    def test_single_interaction_recording(self):
        """Test recording of single tool interactions."""
        interaction = create_tool_interaction(
            user_id=self.user_id,
            tool_name="misp",
            interaction_type=InteractionType.QUERY_EXECUTION,
            data_payload={"query": "malware analysis"},
            success=True,
            duration_ms=2000,
            context_tags=["security", "threat-analysis"]
        )

        self.analyzer.record_interaction(interaction)

        # Verify interaction was recorded
        assert len(self.analyzer.interaction_buffer) == 1
        recorded = self.analyzer.interaction_buffer[0]
        assert recorded.user_id == self.user_id
        assert recorded.tool_name == "misp"
        assert recorded.domain == DomainType.SECURITY
        assert recorded.interaction_type == InteractionType.QUERY_EXECUTION

    def test_cross_domain_sequence_detection(self):
        """Test detection of meaningful cross-domain sequences."""
        # Create a sequence: Security -> Productivity -> Infrastructure
        interactions = [
            create_tool_interaction(
                user_id=self.user_id,
                tool_name="misp",
                interaction_type=InteractionType.QUERY_EXECUTION,
                data_payload={"query": "apt29 indicators"},
                output_data={"indicators": ["hash1", "hash2", "ip1"]},
                context_tags=["threat-hunt"]
            ),
            create_tool_interaction(
                user_id=self.user_id,
                tool_name="dispatch",
                interaction_type=InteractionType.REPORT_GENERATION,
                data_payload={"indicators": ["hash1", "hash2", "ip1"]},
                output_data={"incident_id": "INC-001", "priority": "high"},
                context_tags=["threat-hunt", "incident"]
            ),
            create_tool_interaction(
                user_id=self.user_id,
                tool_name="kong",
                interaction_type=InteractionType.CONFIGURATION_CHANGE,
                data_payload={"block_ips": ["ip1"], "incident_id": "INC-001"},
                context_tags=["incident", "blocking"]
            )
        ]

        # Add small time gaps between interactions
        base_time = datetime.utcnow()
        for i, interaction in enumerate(interactions):
            interaction.timestamp = base_time + timedelta(minutes=i * 5)
            self.analyzer.record_interaction(interaction)

        # Analyze sequences
        sequences = self.analyzer.analyze_interaction_sequences(self.user_id)

        # Verify sequence detection
        assert len(sequences) == 1
        sequence = sequences[0]
        assert len(sequence.interactions) == 3
        # Security, Productivity, Infrastructure
        assert len(sequence.domains_involved) == 3
        assert sequence.success_rate == 1.0  # All successful

        # Verify data flow detection
        # Should detect data dependencies
        assert len(sequence.data_flow_chain) >= 1

    def test_pattern_detection_from_sequences(self):
        """Test detection of recurring patterns from multiple sequences."""
        # Create multiple similar sequences
        for seq_num in range(4):  # Create 4 similar sequences
            base_time = datetime.utcnow() - timedelta(days=seq_num * 2)

            interactions = [
                create_tool_interaction(
                    user_id=self.user_id,
                    tool_name="misp",
                    interaction_type=InteractionType.QUERY_EXECUTION,
                    data_payload={"query": f"threat_hunt_{seq_num}"},
                    output_data={"indicators": [f"hash_{seq_num}"]},
                    context_tags=["security", "hunting"]
                ),
                create_tool_interaction(
                    user_id=self.user_id,
                    tool_name="dispatch",
                    interaction_type=InteractionType.REPORT_GENERATION,
                    data_payload={"indicators": [f"hash_{seq_num}"]},
                    output_data={"incident_id": f"INC-{seq_num:03d}"},
                    context_tags=["security", "incident"]
                )
            ]

            for i, interaction in enumerate(interactions):
                interaction.timestamp = base_time + timedelta(minutes=i * 10)
                self.analyzer.record_interaction(interaction)

        # Analyze sequences and patterns
        sequences = self.analyzer.analyze_interaction_sequences(
            self.user_id, time_window=timedelta(days=30)
        )
        patterns = self.analyzer.detect_cross_tool_patterns(sequences)

        # Verify pattern detection
        assert len(patterns) >= 1
        pattern = patterns[0]
        assert pattern.frequency >= 3  # Should find the recurring pattern
        assert "misp" in pattern.tool_sequence
        assert "dispatch" in pattern.tool_sequence
        assert pattern.automation_potential > 0.5  # Should be automatable

    def test_automation_opportunity_identification(self):
        """Test identification of high-value automation opportunities."""
        # Create a high-frequency, high-success pattern
        for seq_num in range(6):  # 6 occurrences for high frequency
            base_time = datetime.utcnow() - timedelta(hours=seq_num * 4)

            interactions = [
                create_tool_interaction(
                    user_id=self.user_id,
                    tool_name="cyberchef",
                    interaction_type=InteractionType.DATA_TRANSFORM,
                    data_payload={
                        "input": f"encoded_data_{seq_num}", "recipe": "base64_decode"},
                    output_data={"decoded": f"malware_sample_{seq_num}"},
                    success=True,
                    duration_ms=1500,
                    context_tags=["analysis", "decoding"]
                ),
                create_tool_interaction(
                    user_id=self.user_id,
                    tool_name="yara-x",
                    interaction_type=InteractionType.ANALYSIS_REQUEST,
                    data_payload={"sample": f"malware_sample_{seq_num}"},
                    output_data={"matches": [
                        f"rule_{seq_num}"], "threat_level": "high"},
                    success=True,
                    duration_ms=3000,
                    context_tags=["analysis", "detection"]
                ),
                create_tool_interaction(
                    user_id=self.user_id,
                    tool_name="misp",
                    interaction_type=InteractionType.DATA_IMPORT,
                    data_payload={"indicators": [
                        f"rule_{seq_num}"], "threat_level": "high"},
                    success=True,
                    duration_ms=2000,
                    context_tags=["analysis", "threat-intel"]
                )
            ]

            for i, interaction in enumerate(interactions):
                interaction.timestamp = base_time + timedelta(minutes=i * 2)
                self.analyzer.record_interaction(interaction)

        # Analyze for automation opportunities
        sequences = self.analyzer.analyze_interaction_sequences(self.user_id)
        patterns = self.analyzer.detect_cross_tool_patterns(sequences)
        opportunities = self.analyzer.identify_automation_opportunities(
            patterns)

        # Verify high-value opportunity detected
        assert len(opportunities) >= 1
        opportunity = opportunities[0]
        assert opportunity['success_probability'] > 0.7
        assert opportunity['estimated_time_savings']['savings_per_execution_minutes'] > 0
        assert 'n8n_workflow_template' in opportunity
        assert len(opportunity['required_integrations']) >= 3

    def test_domain_transition_analysis(self):
        """Test analysis of domain transition patterns."""
        # Create sequences with various domain transitions
        transition_sequences = [
            # Security -> Productivity
            [("misp", DomainType.SECURITY), ("dispatch", DomainType.PRODUCTIVITY)],
            # Productivity -> Infrastructure
            [("n8n", DomainType.PRODUCTIVITY),
             ("kong", DomainType.INFRASTRUCTURE)],
            # Security -> Infrastructure
            [("helk", DomainType.SECURITY),
             ("ghostwriter", DomainType.INFRASTRUCTURE)],
            # MTG -> Productivity (unusual transition)
            [("commander-spellbook", DomainType.MTG),
             ("mealie", DomainType.PRODUCTIVITY)]
        ]

        for seq_idx, seq_tools in enumerate(transition_sequences):
            base_time = datetime.utcnow() - timedelta(hours=seq_idx * 2)

            for tool_idx, (tool_name, expected_domain) in enumerate(seq_tools):
                interaction = create_tool_interaction(
                    user_id=self.user_id,
                    tool_name=tool_name,
                    interaction_type=InteractionType.QUERY_EXECUTION,
                    data_payload={"action": f"test_{seq_idx}_{tool_idx}"},
                    success=True
                )
                interaction.timestamp = base_time + \
                    timedelta(minutes=tool_idx * 15)
                interaction.domain = expected_domain
                self.analyzer.record_interaction(interaction)

        # Analyze domain transitions
        sequences = self.analyzer.analyze_interaction_sequences(self.user_id)
        domain_analysis = self.analyzer.analyze_domain_transitions(sequences)

        # Verify transition analysis
        assert 'transition_frequencies' in domain_analysis
        assert 'transition_timings' in domain_analysis
        assert 'domain_efficiency' in domain_analysis

        # Check for expected transitions
        frequencies = domain_analysis['transition_frequencies']
        assert any('security->productivity' in key.lower()
                   for key in frequencies.keys())
        assert any('productivity->infrastructure' in key.lower()
                   for key in frequencies.keys())

    def test_data_dependency_detection(self):
        """Test detection of data dependencies between tool interactions."""
        # Create interactions with clear data dependencies
        interaction1 = create_tool_interaction(
            user_id=self.user_id,
            tool_name="cyberchef",
            interaction_type=InteractionType.DATA_TRANSFORM,
            data_payload={"input": "suspicious_file.exe"},
            output_data={"file_hash": "abc123def456",
                         "entropy": 7.8, "file_id": "file_001"}
        )

        interaction2 = create_tool_interaction(
            user_id=self.user_id,
            tool_name="misp",
            interaction_type=InteractionType.QUERY_EXECUTION,
            data_payload={"hash": "abc123def456",
                          "source_file_id": "file_001"},
            output_data={"threat_intel": "known_malware", "confidence": "high"}
        )

        # Test data dependency detection
        has_dependency = self.analyzer._has_data_dependency(
            interaction1.output_data, interaction2.data_payload
        )

        assert has_dependency is True

        # Test with unrelated data
        interaction3 = create_tool_interaction(
            user_id=self.user_id,
            tool_name="mealie",
            interaction_type=InteractionType.DATA_IMPORT,
            data_payload={"recipe": "pasta", "servings": 4}
        )

        has_dependency_unrelated = self.analyzer._has_data_dependency(
            interaction1.output_data, interaction3.data_payload
        )

        assert has_dependency_unrelated is False

    def test_workflow_pattern_analysis_integration(self):
        """Test the high-level workflow pattern analysis function."""
        # Create a comprehensive interaction history
        interaction_history = []

        # Security analysis workflow
        security_workflow = [
            ("misp", InteractionType.QUERY_EXECUTION, {"query": "apt29"}),
            ("helk", InteractionType.ANALYSIS_REQUEST,
             {"logs": "network_traffic"}),
            ("cyberchef", InteractionType.DATA_TRANSFORM,
             {"data": "encoded_payload"}),
            ("dispatch", InteractionType.REPORT_GENERATION,
             {"findings": "threat_detected"})
        ]

        for i, (tool, int_type, payload) in enumerate(security_workflow):
            interaction = create_tool_interaction(
                user_id=self.user_id,
                tool_name=tool,
                interaction_type=int_type,
                data_payload=payload,
                success=True
            )
            interaction.timestamp = datetime.utcnow(
            ) - timedelta(minutes=(len(security_workflow) - i) * 10)
            interaction_history.append(interaction)

        # Analyze workflow patterns
        analysis_result = analyze_user_workflow_patterns(
            self.user_id, interaction_history)

        # Verify comprehensive analysis
        assert 'sequences_detected' in analysis_result
        assert 'patterns_found' in analysis_result
        assert 'automation_opportunities' in analysis_result
        assert 'domain_analysis' in analysis_result
        assert 'top_opportunities' in analysis_result
        assert 'summary' in analysis_result

        # Verify analysis quality
        assert analysis_result['sequences_detected'] >= 1
        summary = analysis_result['summary']
        assert 'most_common_tools' in summary
        assert 'cross_domain_frequency' in summary
        assert 'high_potential_automations' in summary

    def test_n8n_workflow_template_generation(self):
        """Test generation of n8n workflow templates from patterns."""
        # Create a pattern for template generation
        from apps.jane_orchestrator.src.services.n8n.interaction_analyzer import \
            CrossToolPattern

        pattern = CrossToolPattern(
            pattern_id="test_pattern_001",
            pattern_name="Security Analysis Workflow",
            tool_sequence=["misp", "cyberchef", "dispatch"],
            domain_transitions=[
                (DomainType.SECURITY, DomainType.PRODUCTIVITY)],
            interaction_types=[InteractionType.QUERY_EXECUTION,
                               InteractionType.DATA_TRANSFORM],
            data_dependencies=[{"type": "hash_lookup"}],
            timing_constraints={"max_step_duration": timedelta(minutes=5)},
            success_criteria={"min_success_rate": 0.8},
            frequency=5,
            automation_potential=0.85
        )

        # Generate n8n template
        template = self.analyzer._generate_n8n_template_outline(pattern)

        # Verify template structure
        assert 'name' in template
        assert 'description' in template
        assert 'nodes' in template
        assert 'connections' in template
        assert 'settings' in template

        # Verify nodes include trigger and tool nodes
        nodes = template['nodes']
        assert len(nodes) >= 4  # trigger + 3 tool nodes
        assert any(node['type'] ==
                   'n8n-nodes-base.manualTrigger' for node in nodes)

        # Verify connections link nodes properly
        connections = template['connections']
        assert len(connections) >= 3  # At least 3 connections for 4 nodes


@pytest.fixture
def sample_interactions():
    """Provide sample interactions for testing."""
    user_id = "test_user"
    base_time = datetime.utcnow()

    return [
        create_tool_interaction(
            user_id=user_id,
            tool_name="misp",
            interaction_type=InteractionType.QUERY_EXECUTION,
            data_payload={"query": "malware_sample"},
            output_data={"results": ["hash123", "ip456"]},
            context_tags=["threat-intel"]
        ),
        create_tool_interaction(
            user_id=user_id,
            tool_name="dispatch",
            interaction_type=InteractionType.REPORT_GENERATION,
            data_payload={"threats": ["hash123", "ip456"]},
            output_data={"incident_id": "INC-001"},
            context_tags=["incident-response"]
        )
    ]


def test_performance_requirements():
    """Test that interaction analysis meets performance requirements."""
    analyzer = InteractionAnalyzer()
    user_id = "perf_test_user"

    # Create large interaction dataset
    interactions = []
    for i in range(100):  # 100 interactions
        interaction = create_tool_interaction(
            user_id=user_id,
            tool_name=f"tool_{i % 10}",  # Cycle through 10 tools
            interaction_type=InteractionType.QUERY_EXECUTION,
            data_payload={"query": f"test_query_{i}"},
            success=True
        )
        interactions.append(interaction)
        analyzer.record_interaction(interaction)

    # Measure analysis performance
    import time
    start_time = time.time()

    sequences = analyzer.analyze_interaction_sequences(user_id)
    patterns = analyzer.detect_cross_tool_patterns(sequences)
    opportunities = analyzer.identify_automation_opportunities(patterns)

    end_time = time.time()
    analysis_time = end_time - start_time

    # Verify performance (should complete in reasonable time)
    assert analysis_time < 5.0  # Less than 5 seconds for 100 interactions

    # Verify analysis completeness
    assert len(sequences) > 0
    print(
        f"Performance test: Analyzed {len(interactions)} interactions in {analysis_time:.2f}s")
    print(
        f"Found {len(sequences)} sequences, {len(patterns)} patterns, {len(opportunities)} opportunities")


if __name__ == "__main__":
    # Run basic functionality test
    test = TestInteractionAnalyzer()
    test.setup_method()

    print("Testing T101 Cross-Tool Interaction Sequence Detection...")

    try:
        test.test_domain_classification()
        print("✅ Domain classification: PASSED")

        test.test_single_interaction_recording()
        print("✅ Interaction recording: PASSED")

        test.test_cross_domain_sequence_detection()
        print("✅ Cross-domain sequence detection: PASSED")

        test.test_pattern_detection_from_sequences()
        print("✅ Pattern detection from sequences: PASSED")

        test.test_automation_opportunity_identification()
        print("✅ Automation opportunity identification: PASSED")

        test.test_domain_transition_analysis()
        print("✅ Domain transition analysis: PASSED")

        test.test_data_dependency_detection()
        print("✅ Data dependency detection: PASSED")

        test.test_workflow_pattern_analysis_integration()
        print("✅ Workflow pattern analysis integration: PASSED")

        test.test_n8n_workflow_template_generation()
        print("✅ n8n workflow template generation: PASSED")

        test_performance_requirements()
        print("✅ Performance requirements: PASSED")

        print("\n🎉 T101 Cross-Tool Interaction Sequence Detection: ALL TESTS PASSED")
        print("✅ Ready for integration with n8n adaptive workflow system")

    except Exception as e:
        print(f"❌ Test failed: {e}")
        raise
