#!/usr/bin/env python3
"""
MISP Functional Tests - Component Integration and Workflows

Purpose: Functional tests for MISP component integration and end-to-end workflows
Requirements: Section 8.2 Functional Tests from misp-analysis.md
Location: tests/TestCase/Api/ equivalent for integrated MISP

Coverage:
- End-to-end event creation and modification workflows
- Multi-component integration testing
- Business workflow validation
- Cross-component data flow testing
- Component boundary validation
"""

from services.security_tools_service import SecurityToolsService
from libs.service_adapters.security.misp_adapter import MISPAdapter
from api.main import app
import asyncio
import json
# Import system under test
import sys
from datetime import datetime, timedelta
from typing import Any, Dict, List
from unittest.mock import AsyncMock, Mock, patch

import pytest
from httpx import AsyncClient
# Import test fixtures
from test_fixtures import (Analysis, Distribution, MISPTestAttribute,
                           MISPTestDataFactory, MISPTestEvent,
                           MISPTestOrganisation, MISPTestUser, ThreatLevel)

sys.path.append('/workspaces/modular-monolith-2/apps/jane-orchestrator/src')


class TestMISPEventWorkflows:
    """Functional tests for complete MISP event workflows"""

    @pytest.fixture
    async def client(self):
        """Async test client for FastAPI application"""
        async with AsyncClient(app=app, base_url="http://test") as ac:
            yield ac

    @pytest.fixture
    def mock_misp_service(self):
        """Mock MISP service for functional testing"""
        return Mock(spec=SecurityToolsService)

    @pytest.fixture
    def sample_event_workflow_data(self):
        """Complete event workflow test data"""
        return {
            'event': MISPTestDataFactory.create_complete_event(
                "Functional Test APT Campaign",
                num_attributes=5
            ),
            'attributes': [
                {'category': 'Network activity', 'type': 'domain',
                    'value': 'apt-c2.malicious.com'},
                {'category': 'Network activity',
                    'type': 'ip-src', 'value': '192.168.100.50'},
                {'category': 'Payload delivery', 'type': 'md5',
                    'value': 'e99a18c428cb38d5f260853678922e03'},
                {'category': 'Artifacts dropped',
                    'type': 'filename', 'value': 'backdoor.exe'},
                {'category': 'Network activity', 'type': 'url',
                    'value': 'https://apt-c2.malicious.com/payload'}
            ],
            'tags': ['APT', 'targeted-attack', 'financial-sector'],
            'sharing_groups': [1, 2]  # Test sharing groups
        }

    async def test_complete_event_creation_workflow(self, client, sample_event_workflow_data):
        """
        Test: Complete event creation workflow end-to-end
        Coverage: Event creation API workflow from Section 8.2
        Requirement: End-to-end workflow validation
        """
        workflow_data = sample_event_workflow_data
        event_data = workflow_data['event']

        # Step 1: Create event via API
        create_response = await client.post('/api/v1/events', json={
            'info': event_data.info,
            'threat_level_id': event_data.threat_level_id,
            'analysis': event_data.analysis,
            'distribution': event_data.distribution,
            'org_id': event_data.org_id,
            'orgc_id': event_data.orgc_id
        })

        assert create_response.status_code == 201
        created_event = create_response.json()

        # Validate created event structure
        assert created_event['info'] == event_data.info
        assert created_event['threat_level_id'] == event_data.threat_level_id
        assert created_event['analysis'] == event_data.analysis
        assert created_event['distribution'] == event_data.distribution
        assert 'uuid' in created_event
        assert 'id' in created_event

        event_id = created_event['id']

        # Step 2: Add attributes to event
        for attr_data in workflow_data['attributes']:
            attr_response = await client.post(f'/api/v1/events/{event_id}/attributes', json={
                'category': attr_data['category'],
                'type': attr_data['type'],
                'value': attr_data['value'],
                'to_ids': True,
                'distribution': Distribution.THIS_COMMUNITY_ONLY
            })

            assert attr_response.status_code == 201
            created_attr = attr_response.json()
            assert created_attr['category'] == attr_data['category']
            assert created_attr['type'] == attr_data['type']
            assert created_attr['value'] == attr_data['value']

        # Step 3: Add tags to event
        for tag in workflow_data['tags']:
            tag_response = await client.post(f'/api/v1/events/{event_id}/tags', json={
                'name': tag
            })
            assert tag_response.status_code == 201

        # Step 4: Verify complete event structure
        final_response = await client.get(f'/api/v1/events/{event_id}')
        assert final_response.status_code == 200
        final_event = final_response.json()

        # Comprehensive workflow validation
        assert final_event['info'] == event_data.info
        assert len(final_event['attributes']) == len(
            workflow_data['attributes'])
        assert len(final_event['tags']) == len(workflow_data['tags'])

        # Validate attribute preservation
        for i, attr in enumerate(final_event['attributes']):
            expected_attr = workflow_data['attributes'][i]
            assert attr['category'] == expected_attr['category']
            assert attr['type'] == expected_attr['type']
            assert attr['value'] == expected_attr['value']

    async def test_event_modification_workflow(self, client):
        """
        Test: Event modification workflow with validation
        Coverage: Event modification API workflow
        Requirement: Modification workflow integrity
        """
        # Create initial event
        initial_event = MISPTestDataFactory.create_complete_event(
            "Initial Event", num_attributes=2
        )

        create_response = await client.post('/api/v1/events', json={
            'info': initial_event.info,
            'threat_level_id': initial_event.threat_level_id,
            'analysis': initial_event.analysis,
            'distribution': initial_event.distribution
        })

        assert create_response.status_code == 201
        event_id = create_response.json()['id']

        # Step 1: Modify event information
        modify_response = await client.put(f'/api/v1/events/{event_id}', json={
            'info': 'Modified Event Information',
            'threat_level_id': ThreatLevel.HIGH,
            'analysis': Analysis.COMPLETED
        })

        assert modify_response.status_code == 200
        modified_event = modify_response.json()
        assert modified_event['info'] == 'Modified Event Information'
        assert modified_event['threat_level_id'] == ThreatLevel.HIGH
        assert modified_event['analysis'] == Analysis.COMPLETED

        # Step 2: Add new attributes
        new_attr_response = await client.post(f'/api/v1/events/{event_id}/attributes', json={
            'category': 'Network activity',
            'type': 'domain',
            'value': 'new-malicious.com',
            'to_ids': True
        })

        assert new_attr_response.status_code == 201

        # Step 3: Modify existing attribute
        attributes_response = await client.get(f'/api/v1/events/{event_id}/attributes')
        attributes = attributes_response.json()
        first_attr_id = attributes[0]['id']

        modify_attr_response = await client.put(
            f'/api/v1/events/{event_id}/attributes/{first_attr_id}',
            json={'value': 'modified-value.com'}
        )

        assert modify_attr_response.status_code == 200

        # Step 4: Validate final state
        final_response = await client.get(f'/api/v1/events/{event_id}')
        final_event = final_response.json()

        assert final_event['info'] == 'Modified Event Information'
        assert final_event['threat_level_id'] == ThreatLevel.HIGH
        assert any(
            attr['value'] == 'modified-value.com' for attr in final_event['attributes'])
        assert any(
            attr['value'] == 'new-malicious.com' for attr in final_event['attributes'])

    async def test_event_publishing_workflow(self, client):
        """
        Test: Event publishing workflow with distribution validation
        Coverage: Event publishing and distribution workflow
        Requirement: Publishing workflow validation
        """
        # Create event for publishing
        event_data = MISPTestDataFactory.create_complete_event(
            "Event for Publishing", num_attributes=3
        )

        create_response = await client.post('/api/v1/events', json={
            'info': event_data.info,
            'threat_level_id': event_data.threat_level_id,
            'analysis': Analysis.COMPLETED,  # Must be completed for publishing
            'distribution': Distribution.CONNECTED_COMMUNITIES
        })

        event_id = create_response.json()['id']

        # Step 1: Validate event is ready for publishing
        validate_response = await client.get(f'/api/v1/events/{event_id}/validate-publish')
        assert validate_response.status_code == 200
        validation = validate_response.json()
        assert validation['can_publish'] is True
        assert validation['analysis_complete'] is True

        # Step 2: Publish event
        publish_response = await client.post(f'/api/v1/events/{event_id}/publish')
        assert publish_response.status_code == 200
        published_event = publish_response.json()

        # Validate publishing state
        assert published_event['published'] is True
        assert published_event['publish_timestamp'] is not None

        # Step 3: Verify distribution notification (mock check)
        # In real implementation, this would verify notification systems
        notifications_response = await client.get(f'/api/v1/events/{event_id}/notifications')
        assert notifications_response.status_code == 200

    async def test_event_sharing_workflow(self, client):
        """
        Test: Event sharing workflow with sharing groups
        Coverage: Event sharing and access control workflow
        Requirement: Sharing workflow validation
        """
        # Create sharing group first
        sharing_group_response = await client.post('/api/v1/sharing-groups', json={
            'name': 'Test Sharing Group',
            'description': 'Functional test sharing group',
            'releasability': 'Test Organisation Only'
        })

        assert sharing_group_response.status_code == 201
        sharing_group_id = sharing_group_response.json()['id']

        # Create event with sharing group distribution
        event_data = MISPTestDataFactory.create_complete_event(
            "Shared Event", num_attributes=2
        )

        create_response = await client.post('/api/v1/events', json={
            'info': event_data.info,
            'threat_level_id': event_data.threat_level_id,
            'analysis': event_data.analysis,
            'distribution': Distribution.SHARING_GROUP,
            'sharing_group_id': sharing_group_id
        })

        assert create_response.status_code == 201
        shared_event = create_response.json()
        assert shared_event['distribution'] == Distribution.SHARING_GROUP
        assert shared_event['sharing_group_id'] == sharing_group_id

        # Validate sharing group access
        event_id = shared_event['id']
        access_response = await client.get(f'/api/v1/events/{event_id}/sharing-access')
        assert access_response.status_code == 200
        access_info = access_response.json()
        assert access_info['sharing_group_id'] == sharing_group_id


class TestMISPMultiComponentIntegration:
    """Functional tests for multi-component MISP integration"""

    @pytest.fixture
    async def client(self):
        """Async test client for integration testing"""
        async with AsyncClient(app=app, base_url="http://test") as ac:
            yield ac

    @pytest.fixture
    def integration_test_data(self):
        """Test data for multi-component integration"""
        return {
            'organisations': [
                MISPTestDataFactory.create_organisation("Security Org Alpha"),
                MISPTestDataFactory.create_organisation("Threat Intel Beta"),
                MISPTestDataFactory.create_organisation("Research Gamma")
            ],
            'users': [
                MISPTestDataFactory.create_user(
                    "admin@alpha.com", role_id=1, org_id=1),
                MISPTestDataFactory.create_user(
                    "analyst@beta.com", role_id=2, org_id=2),
                MISPTestDataFactory.create_user(
                    "researcher@gamma.com", role_id=3, org_id=3)
            ],
            'events': MISPTestDataFactory.create_correlation_test_events()
        }

    async def test_cross_organisation_event_sharing(self, client, integration_test_data):
        """
        Test: Cross-organisation event sharing integration
        Coverage: Multi-organisation integration from Section 8.2
        Requirement: Cross-component data flow
        """
        orgs = integration_test_data['organisations']
        users = integration_test_data['users']

        # Create organisations
        org_ids = []
        for org in orgs:
            org_response = await client.post('/api/v1/organisations', json={
                'name': org.name,
                'description': f'Test organisation {org.name}',
                'type': 'CSIRT',
                'sector': 'Government'
            })
            assert org_response.status_code == 201
            org_ids.append(org_response.json()['id'])

        # Create users in different organisations
        user_ids = []
        for i, user in enumerate(users):
            user_response = await client.post('/api/v1/users', json={
                'email': user.email,
                'org_id': org_ids[i],
                'role_id': user.role_id,
                'autoalert': True,
                'contactalert': True
            })
            assert user_response.status_code == 201
            user_ids.append(user_response.json()['id'])

        # Create event as first organisation
        event_data = integration_test_data['events'][0]
        create_response = await client.post('/api/v1/events', json={
            'info': event_data.info,
            'threat_level_id': event_data.threat_level_id,
            'analysis': event_data.analysis,
            'distribution': Distribution.CONNECTED_COMMUNITIES,
            'org_id': org_ids[0],
            'orgc_id': org_ids[0]
        }, headers={'X-User-ID': str(user_ids[0])})

        assert create_response.status_code == 201
        event_id = create_response.json()['id']

        # Verify event visibility to connected organisations
        for i in range(1, len(user_ids)):
            visibility_response = await client.get(
                f'/api/v1/events/{event_id}',
                headers={'X-User-ID': str(user_ids[i])}
            )
            # Should be visible due to CONNECTED_COMMUNITIES distribution
            assert visibility_response.status_code == 200
            visible_event = visibility_response.json()
            assert visible_event['info'] == event_data.info

    async def test_correlation_engine_integration(self, client, integration_test_data):
        """
        Test: Correlation engine multi-component integration
        Coverage: Correlation engine integration
        Requirement: Component boundary validation
        """
        events = integration_test_data['events']

        # Create multiple events with correlatable attributes
        event_ids = []
        for event_data in events:
            create_response = await client.post('/api/v1/events', json={
                'info': event_data.info,
                'threat_level_id': event_data.threat_level_id,
                'analysis': event_data.analysis,
                'distribution': Distribution.ALL_COMMUNITIES
            })

            assert create_response.status_code == 201
            event_id = create_response.json()['id']
            event_ids.append(event_id)

            # Add attributes to each event
            for attr in event_data.attributes:
                attr_response = await client.post(f'/api/v1/events/{event_id}/attributes', json={
                    'category': attr.category,
                    'type': attr.type,
                    'value': attr.value,
                    'to_ids': attr.to_ids,
                    'distribution': Distribution.ALL_COMMUNITIES
                })
                assert attr_response.status_code == 201

        # Trigger correlation analysis
        correlation_response = await client.post('/api/v1/correlations/analyze', json={
            'event_ids': event_ids
        })

        assert correlation_response.status_code == 200
        correlations = correlation_response.json()

        # Validate correlation results
        assert 'correlations' in correlations
        assert len(correlations['correlations']) > 0

        # Verify correlation details
        for correlation in correlations['correlations']:
            assert 'source_event_id' in correlation
            assert 'target_event_id' in correlation
            assert 'attribute_type' in correlation
            assert 'correlation_value' in correlation
            assert 'confidence_score' in correlation
            # High confidence correlations
            assert correlation['confidence_score'] >= 0.7

    async def test_notification_system_integration(self, client):
        """
        Test: Notification system multi-component integration
        Coverage: Notification system integration
        Requirement: System-wide notification validation
        """
        # Create user with notification preferences
        user_response = await client.post('/api/v1/users', json={
            'email': 'notified@test.com',
            'org_id': 1,
            'role_id': 2,
            'autoalert': True,
            'contactalert': True,
            'gpgkey': None,
            'notification_preferences': {
                'event_created': True,
                'event_published': True,
                'attribute_added': True,
                'correlation_found': True
            }
        })

        assert user_response.status_code == 201
        user_id = user_response.json()['id']

        # Create event that should trigger notifications
        event_response = await client.post('/api/v1/events', json={
            'info': 'Notification Test Event',
            'threat_level_id': ThreatLevel.HIGH,
            'analysis': Analysis.COMPLETED,
            'distribution': Distribution.ALL_COMMUNITIES
        })

        assert event_response.status_code == 201
        event_id = event_response.json()['id']

        # Publish event to trigger publication notifications
        publish_response = await client.post(f'/api/v1/events/{event_id}/publish')
        assert publish_response.status_code == 200

        # Check notification queue
        notifications_response = await client.get(f'/api/v1/users/{user_id}/notifications')
        assert notifications_response.status_code == 200
        notifications = notifications_response.json()

        # Validate notification creation
        # Event creation + publication notifications
        assert len(notifications) >= 2

        event_created_notification = next(
            (n for n in notifications if n['type'] == 'event_created'), None
        )
        assert event_created_notification is not None
        assert event_created_notification['event_id'] == event_id

        event_published_notification = next(
            (n for n in notifications if n['type'] == 'event_published'), None
        )
        assert event_published_notification is not None
        assert event_published_notification['event_id'] == event_id


class TestMISPBusinessWorkflows:
    """Functional tests for complete business workflows"""

    @pytest.fixture
    async def client(self):
        """Async test client for business workflow testing"""
        async with AsyncClient(app=app, base_url="http://test") as ac:
            yield ac

    async def test_incident_response_workflow(self, client):
        """
        Test: Complete incident response workflow
        Coverage: End-to-end incident response business workflow
        Requirement: Business workflow validation from Section 8.2
        """
        # Step 1: Initial incident report
        incident_event = await client.post('/api/v1/events', json={
            'info': 'Security Incident - Suspicious Network Activity',
            'threat_level_id': ThreatLevel.HIGH,
            'analysis': Analysis.INITIAL,
            'distribution': Distribution.YOUR_ORGANISATION_ONLY
        })

        assert incident_event.status_code == 201
        event_id = incident_event.json()['id']

        # Step 2: Add initial indicators
        initial_indicators = [
            {'category': 'Network activity', 'type': 'ip-src', 'value': '10.0.0.100'},
            {'category': 'Network activity', 'type': 'domain',
                'value': 'suspicious.domain.com'},
            {'category': 'Artifacts dropped',
                'type': 'filename', 'value': 'malware.exe'}
        ]

        for indicator in initial_indicators:
            attr_response = await client.post(f'/api/v1/events/{event_id}/attributes', json={
                **indicator,
                'to_ids': True,
                'distribution': Distribution.YOUR_ORGANISATION_ONLY
            })
            assert attr_response.status_code == 201

        # Step 3: Analysis progression
        analysis_update = await client.put(f'/api/v1/events/{event_id}', json={
            'analysis': Analysis.ONGOING
        })
        assert analysis_update.status_code == 200

        # Step 4: Add more detailed analysis
        detailed_indicators = [
            {'category': 'Payload delivery', 'type': 'md5',
                'value': 'a1b2c3d4e5f6789012345678901234567'},
            {'category': 'Network activity', 'type': 'url',
                'value': 'http://suspicious.domain.com/payload'},
            {'category': 'Attribution', 'type': 'threat-actor',
                'value': 'APT-Test-Group'}
        ]

        for indicator in detailed_indicators:
            attr_response = await client.post(f'/api/v1/events/{event_id}/attributes', json={
                **indicator,
                'to_ids': indicator['category'] == 'Network activity',
                'distribution': Distribution.THIS_COMMUNITY_ONLY
            })
            assert attr_response.status_code == 201

        # Step 5: Complete analysis and share
        completion_update = await client.put(f'/api/v1/events/{event_id}', json={
            'analysis': Analysis.COMPLETED,
            'distribution': Distribution.CONNECTED_COMMUNITIES
        })
        assert completion_update.status_code == 200

        # Step 6: Publish for sharing
        publish_response = await client.post(f'/api/v1/events/{event_id}/publish')
        assert publish_response.status_code == 200

        # Step 7: Validate complete workflow state
        final_event = await client.get(f'/api/v1/events/{event_id}')
        event_data = final_event.json()

        assert event_data['analysis'] == Analysis.COMPLETED
        assert event_data['distribution'] == Distribution.CONNECTED_COMMUNITIES
        assert event_data['published'] is True
        assert len(event_data['attributes']) == 6  # 3 initial + 3 detailed

        # Validate attribute progression (some private, some shared)
        private_attrs = [attr for attr in event_data['attributes']
                         if attr['distribution'] == Distribution.YOUR_ORGANISATION_ONLY]
        shared_attrs = [attr for attr in event_data['attributes']
                        if attr['distribution'] == Distribution.THIS_COMMUNITY_ONLY]

        assert len(private_attrs) == 3  # Initial indicators
        assert len(shared_attrs) == 3   # Detailed analysis

    async def test_threat_intelligence_sharing_workflow(self, client):
        """
        Test: Complete threat intelligence sharing workflow
        Coverage: Threat intelligence sharing business workflow
        Requirement: Intelligence sharing workflow validation
        """
        # Step 1: Create threat intelligence event
        intel_event = await client.post('/api/v1/events', json={
            'info': 'APT Campaign - Financial Sector Targeting',
            'threat_level_id': ThreatLevel.HIGH,
            'analysis': Analysis.COMPLETED,
            'distribution': Distribution.ALL_COMMUNITIES
        })

        event_id = intel_event.json()['id']

        # Step 2: Add comprehensive threat indicators
        threat_indicators = [
            # Network indicators
            {'category': 'Network activity', 'type': 'domain',
                'value': 'apt-finance-c2.malicious.com'},
            {'category': 'Network activity',
                'type': 'ip-src', 'value': '203.0.113.100'},
            {'category': 'Network activity', 'type': 'url',
                'value': 'https://apt-finance-c2.malicious.com/banking'},

            # File indicators
            {'category': 'Payload delivery', 'type': 'md5',
                'value': 'f1d2d2f924e986ac86fdf7b36c94bcdf32beec15'},
            {'category': 'Payload delivery', 'type': 'sha256',
                'value': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'},
            {'category': 'Artifacts dropped', 'type': 'filename',
                'value': 'banking_trojan.exe'},

            # Attack pattern indicators
            {'category': 'External analysis', 'type': 'link',
                'value': 'https://security-blog.example.com/apt-finance-analysis'},
            {'category': 'Attribution', 'type': 'threat-actor',
                'value': 'APT-Finance-Group'},
            {'category': 'Targeting data', 'type': 'target-org',
                'value': 'Financial Services Sector'}
        ]

        for indicator in threat_indicators:
            attr_response = await client.post(f'/api/v1/events/{event_id}/attributes', json={
                **indicator,
                'to_ids': indicator['category'] in ['Network activity', 'Payload delivery', 'Artifacts dropped'],
                'distribution': Distribution.ALL_COMMUNITIES
            })
            assert attr_response.status_code == 201

        # Step 3: Add threat intelligence tags
        intelligence_tags = [
            'financial-sector', 'apt', 'banking-trojan', 'targeted-attack',
            'credential-theft', 'high-confidence'
        ]

        for tag in intelligence_tags:
            tag_response = await client.post(f'/api/v1/events/{event_id}/tags', json={
                'name': tag
            })
            assert tag_response.status_code == 201

        # Step 4: Publish threat intelligence
        publish_response = await client.post(f'/api/v1/events/{event_id}/publish')
        assert publish_response.status_code == 200

        # Step 5: Validate sharing distribution
        shared_event = await client.get(f'/api/v1/events/{event_id}')
        event_data = shared_event.json()

        assert event_data['published'] is True
        assert event_data['distribution'] == Distribution.ALL_COMMUNITIES
        assert len(event_data['attributes']) == 9
        assert len(event_data['tags']) == 6

        # Step 6: Validate IDS integration preparation
        ids_attributes = [
            attr for attr in event_data['attributes'] if attr['to_ids'] is True]
        # Network, payload, and artifact indicators
        assert len(ids_attributes) == 6

        # Step 7: Export for external systems
        export_response = await client.get(f'/api/v1/events/{event_id}/export/stix')
        assert export_response.status_code == 200

        json_export_response = await client.get(f'/api/v1/events/{event_id}/export/json')
        assert json_export_response.status_code == 200

    async def test_collaborative_analysis_workflow(self, client):
        """
        Test: Collaborative analysis workflow with multiple analysts
        Coverage: Multi-user collaborative analysis workflow
        Requirement: Collaborative workflow validation
        """
        # Step 1: Create initial analysis event by first analyst
        initial_event = await client.post('/api/v1/events', json={
            'info': 'Unknown Malware Sample - Collaborative Analysis',
            'threat_level_id': ThreatLevel.MEDIUM,
            'analysis': Analysis.ONGOING,
            'distribution': Distribution.THIS_COMMUNITY_ONLY
        })

        event_id = initial_event.json()['id']

        # Step 2: First analyst adds initial observations
        initial_findings = [
            {'category': 'Payload delivery', 'type': 'md5',
                'value': 'c99c8cd9cdf62a24ba11b82c8b6b8d74'},
            {'category': 'Artifacts dropped', 'type': 'filename',
                'value': 'unknown_sample.exe'},
            {'category': 'External analysis', 'type': 'comment',
                'value': 'Initial triage: Packed executable, suspicious behavior observed'}
        ]

        for finding in initial_findings:
            attr_response = await client.post(f'/api/v1/events/{event_id}/attributes', json={
                **finding,
                'to_ids': finding['type'] != 'comment',
                'distribution': Distribution.THIS_COMMUNITY_ONLY
            }, headers={'X-User-ID': '1', 'X-User-Role': 'analyst'})
            assert attr_response.status_code == 201

        # Step 3: Second analyst adds network analysis
        network_findings = [
            {'category': 'Network activity', 'type': 'domain',
                'value': 'analysis-c2.suspicious.net'},
            {'category': 'Network activity',
                'type': 'ip-dst', 'value': '198.51.100.50'},
            {'category': 'External analysis', 'type': 'comment',
                'value': 'Network analysis: Connects to suspicious C2 infrastructure'}
        ]

        for finding in network_findings:
            attr_response = await client.post(f'/api/v1/events/{event_id}/attributes', json={
                **finding,
                'to_ids': finding['type'] != 'comment',
                'distribution': Distribution.THIS_COMMUNITY_ONLY
            }, headers={'X-User-ID': '2', 'X-User-Role': 'analyst'})
            assert attr_response.status_code == 201

        # Step 4: Third analyst adds behavioral analysis
        behavioral_findings = [
            {'category': 'Persistence mechanism', 'type': 'regkey',
                'value': 'HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run\\malware'},
            {'category': 'External analysis', 'type': 'comment',
                'value': 'Behavioral analysis: Establishes persistence, encrypts files'},
            {'category': 'Attribution', 'type': 'threat-actor',
                'value': 'Ransomware-Group-X'}
        ]

        for finding in behavioral_findings:
            attr_response = await client.post(f'/api/v1/events/{event_id}/attributes', json={
                **finding,
                'to_ids': finding['type'] != 'comment',
                'distribution': Distribution.THIS_COMMUNITY_ONLY
            }, headers={'X-User-ID': '3', 'X-User-Role': 'senior_analyst'})
            assert attr_response.status_code == 201

        # Step 5: Senior analyst completes analysis and escalates
        completion_update = await client.put(f'/api/v1/events/{event_id}', json={
            'analysis': Analysis.COMPLETED,
            'threat_level_id': ThreatLevel.HIGH,
            'distribution': Distribution.CONNECTED_COMMUNITIES,
            'info': 'Ransomware Sample - Collaborative Analysis Complete'
        }, headers={'X-User-ID': '3', 'X-User-Role': 'senior_analyst'})
        assert completion_update.status_code == 200

        # Step 6: Validate collaborative workflow results
        final_event = await client.get(f'/api/v1/events/{event_id}')
        event_data = final_event.json()

        # Verify analysis progression
        assert event_data['analysis'] == Analysis.COMPLETED
        assert event_data['threat_level_id'] == ThreatLevel.HIGH
        assert event_data['distribution'] == Distribution.CONNECTED_COMMUNITIES

        # Verify collaborative contributions
        assert len(event_data['attributes']) == 9  # 3 per analyst

        # Verify attribution and classification
        attribution_attrs = [attr for attr in event_data['attributes']
                             if attr['category'] == 'Attribution']
        assert len(attribution_attrs) == 1
        assert attribution_attrs[0]['value'] == 'Ransomware-Group-X'

        # Verify analysis comments from different analysts
        comment_attrs = [attr for attr in event_data['attributes']
                         if attr['type'] == 'comment']
        assert len(comment_attrs) == 3  # One comment per analyst


if __name__ == '__main__':
    # Run functional tests
    pytest.main([
        __file__,
        '-v',
        '--tb=short',
        '--asyncio-mode=auto',
        '--cov=api',
        '--cov=services',
        '--cov=libs.service_adapters.security.misp_adapter',
        '--cov-report=term-missing'
    ])
