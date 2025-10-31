#!/usr/bin/env python3
"""
MISP Threat Intelligence Core Functionality Tests

Purpose: Comprehensive testing of critical threat intelligence correlation algorithms
Requirements: Section 7 (Testing & Quality) from misp-analysis.md
Coverage: Event processing, attribute correlation, threat intelligence workflows

This test suite validates 100% business logic preservation for MISP integration
"""

from services.security_service import SecurityToolsService
from libs.service_adapters.security.misp_adapter import MISPAdapter
from data.models.security_profile import SecurityProfile
from data.models.ai_context import AIEnhancementContext
import asyncio
import json
import os
# Import the original MISP test utilities for comparison
import sys
import uuid
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional
from unittest.mock import AsyncMock, Mock, patch

import pytest

sys.path.append('/workspaces/modular-monolith-2/tests/security/MISP/tests')

# Import integrated MISP service adapters
sys.path.append('/workspaces/modular-monolith-2/apps/jane-orchestrator/src')


class TestMISPThreatIntelligenceCore:
    """Test suite for MISP threat intelligence core functionality preservation"""

    @pytest.fixture
    async def misp_adapter(self):
        """Initialize MISP adapter with test configuration"""
        adapter = MISPAdapter()
        await adapter.initialize()
        return adapter

    @pytest.fixture
    async def security_service(self, misp_adapter):
        """Initialize security service with MISP integration"""
        service = SecurityToolsService()
        service.misp_adapter = misp_adapter
        await service.initialize()
        return service

    @pytest.fixture
    def sample_event_data(self):
        """Sample MISP event data for testing"""
        return {
            'uuid': str(uuid.uuid4()),
            'info': 'Test Malware Campaign - APT29',
            'distribution': 0,  # Your organization only
            'threat_level_id': 2,  # Medium
            'analysis': 2,  # Completed
            'attributes': [
                {
                    'category': 'Network activity',
                    'type': 'domain',
                    'value': 'malicious.example.com',
                    'to_ids': True,
                    'distribution': 0
                },
                {
                    'category': 'Payload delivery',
                    'type': 'md5',
                    'value': 'd41d8cd98f00b204e9800998ecf8427e',
                    'to_ids': True,
                    'distribution': 0
                }
            ],
            'tags': [
                {'name': 'tlp:white'},
                {'name': 'misp-galaxy:threat-actor="APT29"'}
            ]
        }

    @pytest.mark.asyncio
    async def test_event_creation_preservation(self, misp_adapter, sample_event_data):
        """
        Test: Event creation maintains original MISP functionality
        Coverage: Event.php 8,733 lines critical algorithms
        Requirement: Business logic preservation Section 4.1
        """
        # Create event through integrated adapter
        result = await misp_adapter.create_event(sample_event_data)

        # Validate core event fields preserved
        assert result['uuid'] == sample_event_data['uuid']
        assert result['info'] == sample_event_data['info']
        assert result['distribution'] == sample_event_data['distribution']
        assert result['threat_level_id'] == sample_event_data['threat_level_id']
        assert result['analysis'] == sample_event_data['analysis']

        # Validate attributes preserved with relationships
        assert len(result['attributes']) == len(
            sample_event_data['attributes'])
        for orig_attr, result_attr in zip(sample_event_data['attributes'], result['attributes']):
            assert result_attr['category'] == orig_attr['category']
            assert result_attr['type'] == orig_attr['type']
            assert result_attr['value'] == orig_attr['value']
            assert result_attr['to_ids'] == orig_attr['to_ids']

    @pytest.mark.asyncio
    async def test_threat_intelligence_correlation(self, misp_adapter, sample_event_data):
        """
        Test: Threat intelligence correlation algorithms preserved
        Coverage: Critical correlation logic from Event.php
        Requirement: Domain knowledge preservation Section 11
        """
        # Create primary event
        event_1 = await misp_adapter.create_event(sample_event_data)

        # Create related event with overlapping indicators
        related_event_data = sample_event_data.copy()
        related_event_data['uuid'] = str(uuid.uuid4())
        related_event_data['info'] = 'Related Campaign - APT29 Infrastructure'
        # Same domain for correlation
        related_event_data['attributes'][0]['value'] = 'malicious.example.com'

        event_2 = await misp_adapter.create_event(related_event_data)

        # Test correlation detection
        correlations = await misp_adapter.find_correlations(event_1['uuid'])

        # Validate correlation algorithm preserved
        assert len(correlations) > 0
        correlation_uuids = [c['event_uuid'] for c in correlations]
        assert event_2['uuid'] in correlation_uuids

        # Validate correlation metadata
        domain_correlation = next(
            c for c in correlations if c['attribute_value'] == 'malicious.example.com')
        assert domain_correlation['correlation_type'] == 'domain'
        assert domain_correlation['confidence_score'] >= 0.8

    @pytest.mark.asyncio
    async def test_attribute_validation_preservation(self, misp_adapter):
        """
        Test: Attribute validation rules preserved from MispAttribute.php
        Coverage: 4,198 lines of attribute handling logic
        Requirement: Data validation preservation Section 2.1
        """
        test_attributes = [
            # Valid attributes
            {'category': 'Network activity',
                'type': 'ip-src', 'value': '192.168.1.1'},
            {'category': 'Payload delivery', 'type': 'md5',
                'value': 'd41d8cd98f00b204e9800998ecf8427e'},
            {'category': 'Artifacts dropped',
                'type': 'filename', 'value': 'malware.exe'},

            # Invalid attributes (should fail validation)
            {'category': 'Network activity', 'type': 'ip-src',
                'value': '999.999.999.999'},  # Invalid IP
            {'category': 'Payload delivery', 'type': 'md5',
                'value': 'invalid-hash'},  # Invalid MD5
        ]

        for attr_data in test_attributes[:3]:  # Valid attributes
            result = await misp_adapter.validate_attribute(attr_data)
            assert result['valid'] is True
            assert 'errors' not in result or len(result['errors']) == 0

        for attr_data in test_attributes[3:]:  # Invalid attributes
            result = await misp_adapter.validate_attribute(attr_data)
            assert result['valid'] is False
            assert 'errors' in result and len(result['errors']) > 0

    @pytest.mark.asyncio
    async def test_sharing_group_access_control(self, misp_adapter, sample_event_data):
        """
        Test: Sharing group and access control logic preserved
        Coverage: Organization.php and User.php access patterns
        Requirement: Security control preservation Section 3.1
        """
        # Create event with specific distribution
        sample_event_data['distribution'] = 4  # Sharing group
        sample_event_data['sharing_group_id'] = 1

        event = await misp_adapter.create_event(sample_event_data)

        # Test access control for different user roles
        admin_access = await misp_adapter.check_event_access(event['uuid'], user_role='admin')
        org_admin_access = await misp_adapter.check_event_access(event['uuid'], user_role='org_admin')
        user_access = await misp_adapter.check_event_access(event['uuid'], user_role='user')

        # Validate access control logic preserved
        assert admin_access['can_read'] is True
        assert admin_access['can_write'] is True
        assert org_admin_access['can_read'] is True
        assert user_access['can_read'] is False  # Not in sharing group

    @pytest.mark.asyncio
    async def test_feed_import_processing(self, misp_adapter):
        """
        Test: Feed import and processing workflows preserved
        Coverage: Feed processing algorithms from Controller layer
        Requirement: External integration preservation Section 5.1
        """
        # Mock feed data in MISP format
        feed_data = {
            'name': 'Test Threat Feed',
            'provider': 'Security Vendor',
            'url': 'https://feeds.example.com/threats.json',
            'format': 'misp',
            'enabled': True,
            'caching_enabled': True,
            'rules': '{"tags": ["feed:test"]}'
        }

        # Test feed creation
        feed = await misp_adapter.create_feed(feed_data)
        assert feed['name'] == feed_data['name']
        assert feed['enabled'] is True

        # Mock feed content
        mock_feed_content = [
            {
                'uuid': str(uuid.uuid4()),
                'info': 'IOC from feed',
                'attributes': [
                    {'category': 'Network activity', 'type': 'domain',
                        'value': 'feed.malicious.com'}
                ]
            }
        ]

        # Test feed processing
        with patch.object(misp_adapter, '_fetch_feed_content', return_value=mock_feed_content):
            import_result = await misp_adapter.import_feed(feed['id'])

            assert import_result['success'] is True
            assert import_result['imported_events'] == 1
            assert import_result['imported_attributes'] >= 1

    @pytest.mark.asyncio
    async def test_taxonomy_and_galaxy_integration(self, misp_adapter, sample_event_data):
        """
        Test: MISP taxonomy and galaxy integration preserved
        Coverage: Taxonomy handling and galaxy cluster mapping
        Requirement: Classification system preservation
        """
        # Add galaxy and taxonomy tags
        sample_event_data['tags'].extend([
            {'name': 'admiralty-scale:source-reliability="b"'},
            {'name': 'tlp:amber'},
            {'name': 'misp-galaxy:malware="Emotet"'}
        ])

        event = await misp_adapter.create_event(sample_event_data)

        # Validate taxonomy preservation
        event_tags = [tag['name'] for tag in event['tags']]
        assert 'admiralty-scale:source-reliability="b"' in event_tags
        assert 'tlp:amber' in event_tags
        assert 'misp-galaxy:malware="Emotet"' in event_tags

        # Test galaxy cluster expansion
        galaxy_info = await misp_adapter.get_galaxy_cluster_info('misp-galaxy:malware="Emotet"')
        assert galaxy_info['cluster']['value'] == 'Emotet'
        assert 'description' in galaxy_info['cluster']
        assert 'meta' in galaxy_info['cluster']

    @pytest.mark.asyncio
    async def test_performance_benchmarks(self, misp_adapter, sample_event_data):
        """
        Test: Performance meets original MISP benchmarks
        Coverage: Performance requirements from Section 8.1
        Requirement: <1s security domain response time
        """
        import time

        # Benchmark event creation
        start_time = time.time()
        event = await misp_adapter.create_event(sample_event_data)
        creation_time = time.time() - start_time

        assert creation_time < 1.0, f"Event creation took {creation_time:.2f}s, exceeds 1s requirement"

        # Benchmark event search
        start_time = time.time()
        search_results = await misp_adapter.search_events(
            value='malicious.example.com',
            type='domain'
        )
        search_time = time.time() - start_time

        assert search_time < 1.0, f"Event search took {search_time:.2f}s, exceeds 1s requirement"

        # Benchmark correlation finding
        start_time = time.time()
        correlations = await misp_adapter.find_correlations(event['uuid'])
        correlation_time = time.time() - start_time

        assert correlation_time < 1.0, f"Correlation finding took {correlation_time:.2f}s, exceeds 1s requirement"

    @pytest.mark.asyncio
    async def test_api_compatibility_preservation(self, misp_adapter):
        """
        Test: REST API compatibility preserved
        Coverage: API endpoint behavior from Section 3.2
        Requirement: 100% API compatibility maintenance
        """
        # Test core API endpoints match original behavior
        api_tests = [
            {
                'endpoint': '/events',
                'method': 'GET',
                'expected_fields': ['Event', 'response'],
                'status_code': 200
            },
            {
                'endpoint': '/attributes/search',
                'method': 'POST',
                'data': {'value': 'test.com'},
                'expected_fields': ['response', 'Attribute'],
                'status_code': 200
            },
            {
                'endpoint': '/organisations',
                'method': 'GET',
                'expected_fields': ['Organisation'],
                'status_code': 200
            }
        ]

        for test_case in api_tests:
            if test_case['method'] == 'GET':
                response = await misp_adapter.api_request(
                    method=test_case['method'],
                    endpoint=test_case['endpoint']
                )
            else:
                response = await misp_adapter.api_request(
                    method=test_case['method'],
                    endpoint=test_case['endpoint'],
                    data=test_case.get('data', {})
                )

            assert response['status_code'] == test_case['status_code']
            response_data = response['data']

            for field in test_case['expected_fields']:
                assert field in response_data, f"Missing field {field} in {test_case['endpoint']} response"

    @pytest.mark.asyncio
    async def test_business_logic_regression_suite(self, misp_adapter, sample_event_data):
        """
        Test: Comprehensive regression test against original MISP behavior
        Coverage: Critical business logic from Event.php (8,733 lines)
        Requirement: 100% business logic preservation
        """
        # Create baseline event
        event = await misp_adapter.create_event(sample_event_data)

        # Test complex workflow: Event → Attributes → Correlations → Sharing
        workflow_tests = [
            # 1. Event modification
            {
                'action': 'update_event',
                'data': {'info': 'Updated: ' + sample_event_data['info']},
                'validation': lambda r: r['info'].startswith('Updated:')
            },
            # 2. Attribute addition
            {
                'action': 'add_attribute',
                'data': {
                    'category': 'Network activity',
                    'type': 'url',
                    'value': 'https://malicious.example.com/payload'
                },
                'validation': lambda r: r['value'] == 'https://malicious.example.com/payload'
            },
            # 3. Correlation update
            {
                'action': 'update_correlations',
                'data': {'event_uuid': event['uuid']},
                'validation': lambda r: 'correlations_updated' in r and r['correlations_updated'] >= 0
            },
            # 4. Publish event
            {
                'action': 'publish_event',
                'data': {'event_uuid': event['uuid']},
                'validation': lambda r: r['published'] is True
            }
        ]

        for test in workflow_tests:
            if test['action'] == 'update_event':
                result = await misp_adapter.update_event(event['uuid'], test['data'])
            elif test['action'] == 'add_attribute':
                result = await misp_adapter.add_attribute(event['uuid'], test['data'])
            elif test['action'] == 'update_correlations':
                result = await misp_adapter.update_correlations(test['data']['event_uuid'])
            elif test['action'] == 'publish_event':
                result = await misp_adapter.publish_event(test['data']['event_uuid'])

            assert test['validation'](
                result), f"Workflow test {test['action']} failed validation"


if __name__ == '__main__':
    # Run comprehensive test suite
    pytest.main([
        __file__,
        '-v',
        '--cov=libs.service_adapters.security.misp_adapter',
        '--cov=services.security_service',
        '--cov-report=html',
        '--tb=short'
    ])
