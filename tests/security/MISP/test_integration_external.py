#!/usr/bin/env python3
"""
MISP Integration Tests - External System Integration

Purpose: Integration tests for MISP external system integration and data flow
Requirements: Section 8.3 Integration Tests from misp-analysis.md
Location: Equivalent to tests/TestCase/Api/RestResponse* for integrated MISP

Coverage:
- External API compatibility testing
- Database integration with PostgreSQL
- Service layer integration validation
- Cross-system data synchronization
- Real integration scenarios with mocked external dependencies
"""

from services.security_tools_service import SecurityToolsService
from libs.service_adapters.security.misp_adapter import MISPAdapter
from data.database import get_database
from api.main import app
import asyncio
import json
# System imports
import sys
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional
from unittest.mock import AsyncMock, Mock, patch

import psycopg2
import pytest
import requests_mock
from httpx import AsyncClient
from psycopg2.extras import RealDictCursor
# Import test fixtures
from test_fixtures import (Analysis, Distribution, MISPTestDataFactory,
                           ThreatLevel)

sys.path.append('/workspaces/modular-monolith-2/apps/jane-orchestrator/src')


class TestMISPDatabaseIntegration:
    """Integration tests for MISP database operations with PostgreSQL"""

    @pytest.fixture
    async def db_connection(self):
        """Test database connection"""
        # Use test database configuration
        connection = psycopg2.connect(
            host="localhost",
            database="misp_test",
            user="test_user",
            password="test_pass",
            cursor_factory=RealDictCursor
        )
        yield connection
        connection.close()

    @pytest.fixture
    async def client(self):
        """Test client with database integration"""
        async with AsyncClient(app=app, base_url="http://test") as ac:
            yield ac

    async def test_event_database_persistence(self, client, db_connection):
        """
        Test: Event persistence in PostgreSQL database
        Coverage: Database integration from Section 8.3
        Requirement: Database operation validation
        """
        # Create event via API
        event_data = MISPTestDataFactory.create_complete_event(
            "Database Integration Test", num_attributes=3
        )

        create_response = await client.post('/api/v1/events', json={
            'info': event_data.info,
            'threat_level_id': event_data.threat_level_id,
            'analysis': event_data.analysis,
            'distribution': event_data.distribution,
            'org_id': 1,
            'orgc_id': 1
        })

        assert create_response.status_code == 201
        created_event = create_response.json()
        event_id = created_event['id']

        # Verify database persistence
        with db_connection.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM misp_events WHERE id = %s",
                (event_id,)
            )
            db_event = cursor.fetchone()

            assert db_event is not None
            assert db_event['info'] == event_data.info
            assert db_event['threat_level_id'] == event_data.threat_level_id
            assert db_event['analysis'] == event_data.analysis
            assert db_event['distribution'] == event_data.distribution
            assert db_event['uuid'] is not None
            assert db_event['timestamp'] is not None

    async def test_attribute_database_relationships(self, client, db_connection):
        """
        Test: Attribute-Event relationship integrity in database
        Coverage: Relational integrity testing
        Requirement: Data relationship validation
        """
        # Create event with attributes
        event_response = await client.post('/api/v1/events', json={
            'info': 'Relationship Test Event',
            'threat_level_id': ThreatLevel.MEDIUM,
            'analysis': Analysis.ONGOING,
            'distribution': Distribution.THIS_COMMUNITY_ONLY
        })

        event_id = event_response.json()['id']

        # Add multiple attributes
        attribute_data = [
            {'category': 'Network activity', 'type': 'domain', 'value': 'test1.com'},
            {'category': 'Network activity',
                'type': 'ip-src', 'value': '192.168.1.1'},
            {'category': 'Payload delivery', 'type': 'md5',
                'value': 'a1b2c3d4e5f67890123456789abcdef0'}
        ]

        attribute_ids = []
        for attr in attribute_data:
            attr_response = await client.post(f'/api/v1/events/{event_id}/attributes', json={
                **attr,
                'to_ids': True,
                'distribution': Distribution.THIS_COMMUNITY_ONLY
            })
            assert attr_response.status_code == 201
            attribute_ids.append(attr_response.json()['id'])

        # Verify database relationships
        with db_connection.cursor() as cursor:
            # Check event exists
            cursor.execute(
                "SELECT id FROM misp_events WHERE id = %s", (event_id,))
            assert cursor.fetchone() is not None

            # Check all attributes exist and reference correct event
            cursor.execute(
                "SELECT id, event_id, category, type, value FROM misp_attributes WHERE event_id = %s",
                (event_id,)
            )
            db_attributes = cursor.fetchall()

            assert len(db_attributes) == 3
            for db_attr in db_attributes:
                assert db_attr['event_id'] == event_id
                assert db_attr['id'] in attribute_ids

                # Find matching original attribute
                original_attr = next(
                    (attr for attr in attribute_data
                     if attr['category'] == db_attr['category'] and
                        attr['type'] == db_attr['type'] and
                        attr['value'] == db_attr['value']),
                    None
                )
                assert original_attr is not None

    async def test_database_transaction_integrity(self, client, db_connection):
        """
        Test: Database transaction integrity and rollback
        Coverage: Transaction management
        Requirement: Data consistency validation
        """
        # Attempt to create event with invalid data that should trigger rollback
        with pytest.raises(Exception):
            async with client.post('/api/v1/events', json={
                'info': 'Transaction Test Event',
                'threat_level_id': 999,  # Invalid threat level
                'analysis': Analysis.ONGOING,
                'distribution': Distribution.THIS_COMMUNITY_ONLY,
                'org_id': 999  # Non-existent organisation
            }) as response:
                # Should fail and rollback
                assert response.status_code != 201

        # Verify no partial data was inserted
        with db_connection.cursor() as cursor:
            cursor.execute(
                "SELECT COUNT(*) as count FROM misp_events WHERE info = %s",
                ('Transaction Test Event',)
            )
            result = cursor.fetchone()
            assert result['count'] == 0

    async def test_database_performance_constraints(self, client, db_connection):
        """
        Test: Database performance under load
        Coverage: Performance constraint validation
        Requirement: Database performance requirements
        """
        import time

        # Create multiple events concurrently to test performance
        start_time = time.time()

        tasks = []
        for i in range(10):
            task = client.post('/api/v1/events', json={
                'info': f'Performance Test Event {i}',
                'threat_level_id': ThreatLevel.LOW,
                'analysis': Analysis.INITIAL,
                'distribution': Distribution.YOUR_ORGANISATION_ONLY
            })
            tasks.append(task)

        # Wait for all requests to complete
        responses = await asyncio.gather(*tasks)
        end_time = time.time()

        # Verify all events were created successfully
        for response in responses:
            assert response.status_code == 201

        # Verify performance constraint (<1s for security domain)
        total_time = end_time - start_time
        assert total_time < 1.0, f"Database operations took {total_time}s, should be <1s"

        # Verify database consistency
        with db_connection.cursor() as cursor:
            cursor.execute(
                "SELECT COUNT(*) as count FROM misp_events WHERE info LIKE %s",
                ('Performance Test Event%',)
            )
            result = cursor.fetchone()
            assert result['count'] == 10


class TestMISPExternalAPIIntegration:
    """Integration tests for external API compatibility and integration"""

    @pytest.fixture
    async def client(self):
        """Test client for API integration testing"""
        async with AsyncClient(app=app, base_url="http://test") as ac:
            yield ac

    @pytest.fixture
    def mock_external_misp(self):
        """Mock external MISP instance for integration testing"""
        return Mock()

    async def test_misp_rest_api_compatibility(self, client):
        """
        Test: REST API compatibility with standard MISP API
        Coverage: External API compatibility from Section 8.3
        Requirement: API compatibility validation
        """
        # Test Events API compatibility

        # GET /events - List events
        events_response = await client.get('/api/v1/events')
        assert events_response.status_code == 200
        events_data = events_response.json()
        assert 'events' in events_data or isinstance(events_data, list)

        # POST /events - Create event (MISP-compatible format)
        misp_event_data = {
            'Event': {
                'info': 'API Compatibility Test',
                'threat_level_id': ThreatLevel.MEDIUM,
                'analysis': Analysis.ONGOING,
                'distribution': Distribution.ALL_COMMUNITIES,
                'published': False
            }
        }

        create_response = await client.post('/api/v1/events', json=misp_event_data)
        assert create_response.status_code == 201
        created_event = create_response.json()

        # Verify MISP-compatible response format
        assert 'Event' in created_event or 'id' in created_event
        event_id = created_event.get('Event', {}).get(
            'id') or created_event.get('id')
        assert event_id is not None

        # GET /events/{id} - Get specific event
        get_response = await client.get(f'/api/v1/events/{event_id}')
        assert get_response.status_code == 200
        event_data = get_response.json()

        # Verify MISP-compatible structure
        event_info = event_data.get('Event', event_data)
        assert event_info['info'] == 'API Compatibility Test'
        assert event_info['threat_level_id'] == ThreatLevel.MEDIUM

    async def test_misp_attribute_api_integration(self, client):
        """
        Test: Attribute API integration and compatibility
        Coverage: Attribute API integration
        Requirement: MISP attribute API compliance
        """
        # Create event first
        event_response = await client.post('/api/v1/events', json={
            'info': 'Attribute API Test',
            'threat_level_id': ThreatLevel.LOW,
            'analysis': Analysis.INITIAL,
            'distribution': Distribution.YOUR_ORGANISATION_ONLY
        })

        event_id = event_response.json()['id']

        # Test attribute creation via API
        attribute_data = {
            'Attribute': {
                'category': 'Network activity',
                'type': 'domain',
                'value': 'api-test.malicious.com',
                'to_ids': True,
                'distribution': Distribution.YOUR_ORGANISATION_ONLY,
                'event_id': event_id
            }
        }

        attr_response = await client.post(
            f'/api/v1/events/{event_id}/attributes',
            json=attribute_data
        )
        assert attr_response.status_code == 201
        created_attr = attr_response.json()

        # Verify MISP-compatible attribute format
        attr_info = created_attr.get('Attribute', created_attr)
        assert attr_info['category'] == 'Network activity'
        assert attr_info['type'] == 'domain'
        assert attr_info['value'] == 'api-test.malicious.com'

        # Test attribute retrieval
        attr_id = attr_info['id']
        get_attr_response = await client.get(f'/api/v1/attributes/{attr_id}')
        assert get_attr_response.status_code == 200

        # Test attribute search
        search_response = await client.post('/api/v1/attributes/search', json={
            'type': 'domain',
            'value': 'api-test.malicious.com'
        })
        assert search_response.status_code == 200
        search_results = search_response.json()
        assert len(search_results) >= 1

    @requests_mock.Mocker()
    async def test_external_misp_synchronization(self, client, m):
        """
        Test: External MISP instance synchronization
        Coverage: External system synchronization
        Requirement: Cross-system integration validation
        """
        # Mock external MISP instance
        external_misp_url = "https://external-misp.test.com"

        # Mock external MISP API responses
        m.get(f"{external_misp_url}/events", json={
            'response': [{
                'Event': {
                    'id': '1',
                    'uuid': '123e4567-e89b-12d3-a456-426614174000',
                    'info': 'External Event Test',
                    'threat_level_id': ThreatLevel.HIGH,
                    'analysis': Analysis.COMPLETED,
                    'distribution': Distribution.ALL_COMMUNITIES,
                    'published': True,
                    'Attribute': [
                        {
                            'id': '1',
                            'category': 'Network activity',
                            'type': 'domain',
                            'value': 'external-malicious.com',
                            'to_ids': True
                        }
                    ]
                }
            }]
        })

        # Test synchronization endpoint
        sync_response = await client.post('/api/v1/sync/pull', json={
            'server_url': external_misp_url,
            'authkey': 'test-auth-key',
            'sync_user_id': 1
        })

        assert sync_response.status_code == 200
        sync_result = sync_response.json()

        # Verify synchronization results
        assert 'events_synced' in sync_result
        assert sync_result['events_synced'] >= 1

        # Verify event was imported
        imported_events = await client.get('/api/v1/events')
        events_data = imported_events.json()

        # Look for the synchronized event
        external_event = None
        for event in (events_data.get('events', events_data) if isinstance(events_data, dict) else events_data):
            if event.get('info') == 'External Event Test':
                external_event = event
                break

        assert external_event is not None
        assert external_event['threat_level_id'] == ThreatLevel.HIGH
        assert external_event['published'] is True

    async def test_export_format_integration(self, client):
        """
        Test: Export format integration (STIX, JSON, XML)
        Coverage: Export format compatibility
        Requirement: Standards compliance validation
        """
        # Create event with comprehensive data for export
        event_response = await client.post('/api/v1/events', json={
            'info': 'Export Format Test Event',
            'threat_level_id': ThreatLevel.HIGH,
            'analysis': Analysis.COMPLETED,
            'distribution': Distribution.ALL_COMMUNITIES
        })

        event_id = event_response.json()['id']

        # Add attributes for richer export data
        attributes = [
            {'category': 'Network activity', 'type': 'domain',
                'value': 'export-test.malicious.com'},
            {'category': 'Network activity',
                'type': 'ip-src', 'value': '203.0.113.200'},
            {'category': 'Payload delivery', 'type': 'sha256',
                'value': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'}
        ]

        for attr in attributes:
            await client.post(f'/api/v1/events/{event_id}/attributes', json={
                **attr,
                'to_ids': True,
                'distribution': Distribution.ALL_COMMUNITIES
            })

        # Test JSON export
        json_export = await client.get(f'/api/v1/events/{event_id}/export/json')
        assert json_export.status_code == 200
        json_data = json_export.json()
        assert 'Event' in json_data
        assert json_data['Event']['info'] == 'Export Format Test Event'

        # Test STIX export
        stix_export = await client.get(f'/api/v1/events/{event_id}/export/stix')
        assert stix_export.status_code == 200
        # STIX should be valid JSON or XML
        assert stix_export.headers.get('content-type') in [
            'application/json', 'application/xml', 'text/xml'
        ]

        # Test XML export
        xml_export = await client.get(f'/api/v1/events/{event_id}/export/xml')
        assert xml_export.status_code == 200
        assert xml_export.headers.get('content-type') == 'application/xml'

        # Test IDS export (Snort rules)
        ids_export = await client.get(f'/api/v1/events/{event_id}/export/snort')
        assert ids_export.status_code == 200
        ids_content = ids_export.text
        assert 'alert' in ids_content.lower() or 'rule' in ids_content.lower()


class TestMISPServiceLayerIntegration:
    """Integration tests for service layer and adapter integration"""

    @pytest.fixture
    def misp_adapter(self):
        """MISP adapter for service integration testing"""
        return MISPAdapter()

    @pytest.fixture
    def security_service(self, misp_adapter):
        """Security tools service with MISP adapter"""
        service = SecurityToolsService()
        service.misp_adapter = misp_adapter
        return service

    async def test_service_adapter_integration(self, security_service):
        """
        Test: Service layer and adapter integration
        Coverage: Service integration from Section 8.3
        Requirement: Service layer validation
        """
        # Test event creation through service layer
        event_data = {
            'info': 'Service Integration Test',
            'threat_level_id': ThreatLevel.MEDIUM,
            'analysis': Analysis.ONGOING,
            'distribution': Distribution.THIS_COMMUNITY_ONLY,
            'org_id': 1,
            'orgc_id': 1
        }

        # Create event through service
        created_event = await security_service.create_misp_event(event_data)

        assert created_event is not None
        assert created_event['info'] == event_data['info']
        assert created_event['threat_level_id'] == event_data['threat_level_id']
        assert 'id' in created_event
        assert 'uuid' in created_event

        event_id = created_event['id']

        # Test attribute creation through service
        attribute_data = {
            'category': 'Network activity',
            'type': 'domain',
            'value': 'service-test.malicious.com',
            'to_ids': True,
            'distribution': Distribution.THIS_COMMUNITY_ONLY,
            'event_id': event_id
        }

        created_attribute = await security_service.create_misp_attribute(attribute_data)

        assert created_attribute is not None
        assert created_attribute['category'] == attribute_data['category']
        assert created_attribute['type'] == attribute_data['type']
        assert created_attribute['value'] == attribute_data['value']
        assert created_attribute['event_id'] == event_id

    async def test_correlation_service_integration(self, security_service):
        """
        Test: Correlation service integration
        Coverage: Correlation service integration
        Requirement: Cross-service correlation validation
        """
        # Create multiple events with correlatable attributes
        event1_data = {
            'info': 'Correlation Test Event 1',
            'threat_level_id': ThreatLevel.HIGH,
            'analysis': Analysis.COMPLETED,
            'distribution': Distribution.ALL_COMMUNITIES
        }

        event2_data = {
            'info': 'Correlation Test Event 2',
            'threat_level_id': ThreatLevel.HIGH,
            'analysis': Analysis.COMPLETED,
            'distribution': Distribution.ALL_COMMUNITIES
        }

        event1 = await security_service.create_misp_event(event1_data)
        event2 = await security_service.create_misp_event(event2_data)

        # Add correlatable attributes (same domain)
        common_domain = 'correlation-test.malicious.com'

        attr1_data = {
            'category': 'Network activity',
            'type': 'domain',
            'value': common_domain,
            'to_ids': True,
            'distribution': Distribution.ALL_COMMUNITIES,
            'event_id': event1['id']
        }

        attr2_data = {
            'category': 'Network activity',
            'type': 'domain',
            'value': common_domain,
            'to_ids': True,
            'distribution': Distribution.ALL_COMMUNITIES,
            'event_id': event2['id']
        }

        await security_service.create_misp_attribute(attr1_data)
        await security_service.create_misp_attribute(attr2_data)

        # Test correlation detection through service
        correlations = await security_service.find_correlations([event1['id'], event2['id']])

        assert correlations is not None
        assert len(correlations) >= 1

        # Verify correlation details
        correlation = correlations[0]
        assert correlation['attribute_value'] == common_domain
        assert correlation['event_1_id'] in [event1['id'], event2['id']]
        assert correlation['event_2_id'] in [event1['id'], event2['id']]
        assert correlation['event_1_id'] != correlation['event_2_id']

    async def test_notification_service_integration(self, security_service):
        """
        Test: Notification service integration
        Coverage: Notification system integration
        Requirement: Service notification validation
        """
        # Create user with notification preferences
        user_data = {
            'email': 'integration-test@example.com',
            'org_id': 1,
            'role_id': 2,
            'autoalert': True,
            'contactalert': True
        }

        user = await security_service.create_user(user_data)
        user_id = user['id']

        # Create event that should trigger notifications
        event_data = {
            'info': 'Notification Integration Test',
            'threat_level_id': ThreatLevel.HIGH,
            'analysis': Analysis.COMPLETED,
            'distribution': Distribution.ALL_COMMUNITIES,
            'org_id': 1,
            'orgc_id': 1
        }

        created_event = await security_service.create_misp_event(event_data)

        # Publish event to trigger notifications
        published_event = await security_service.publish_event(created_event['id'])
        assert published_event['published'] is True

        # Check notification generation
        notifications = await security_service.get_user_notifications(user_id)

        assert notifications is not None
        assert len(notifications) >= 1

        # Verify notification details
        event_notification = next(
            (n for n in notifications if n['event_id'] == created_event['id']),
            None
        )
        assert event_notification is not None
        assert event_notification['type'] in [
            'event_created', 'event_published']
        assert event_notification['user_id'] == user_id


class TestMISPRealWorldIntegration:
    """Integration tests simulating real-world usage scenarios"""

    @pytest.fixture
    async def client(self):
        """Test client for real-world integration testing"""
        async with AsyncClient(app=app, base_url="http://test") as ac:
            yield ac

    async def test_incident_response_integration_scenario(self, client):
        """
        Test: Complete incident response integration scenario
        Coverage: Real-world integration scenario
        Requirement: End-to-end integration validation
        """
        # Scenario: Security incident with multiple IOCs and analysis phases

        # Phase 1: Initial incident report
        incident_data = {
            'info': 'Security Incident - Suspicious Email Campaign',
            'threat_level_id': ThreatLevel.HIGH,
            'analysis': Analysis.INITIAL,
            'distribution': Distribution.YOUR_ORGANISATION_ONLY,
            'org_id': 1,
            'orgc_id': 1
        }

        incident_response = await client.post('/api/v1/events', json=incident_data)
        assert incident_response.status_code == 201
        incident_id = incident_response.json()['id']

        # Phase 2: Add initial indicators from email analysis
        email_indicators = [
            {'category': 'Network activity', 'type': 'domain',
                'value': 'phishing-campaign.suspicious.net'},
            {'category': 'Network activity',
                'type': 'ip-src', 'value': '198.51.100.100'},
            {'category': 'Payload delivery', 'type': 'email-src',
                'value': 'attacker@suspicious.net'},
            {'category': 'Payload delivery', 'type': 'email-subject',
                'value': 'Urgent: Account Verification Required'}
        ]

        for indicator in email_indicators:
            attr_response = await client.post(f'/api/v1/events/{incident_id}/attributes', json={
                **indicator,
                'to_ids': True,
                'distribution': Distribution.YOUR_ORGANISATION_ONLY
            })
            assert attr_response.status_code == 201

        # Phase 3: Progress analysis and add file indicators
        await client.put(f'/api/v1/events/{incident_id}', json={
            'analysis': Analysis.ONGOING
        })

        file_indicators = [
            {'category': 'Payload delivery', 'type': 'md5',
                'value': 'c99a4c8d9f62a24ba11b82c8b6b8d74a'},
            {'category': 'Payload delivery', 'type': 'sha256',
                'value': 'f2ca1bb6c7e907d06dafe4687e579fce76b37e4e93b7605022da52e6ccc26fe2'},
            {'category': 'Artifacts dropped', 'type': 'filename',
                'value': 'account_verification.exe'}
        ]

        for indicator in file_indicators:
            attr_response = await client.post(f'/api/v1/events/{incident_id}/attributes', json={
                **indicator,
                'to_ids': True,
                'distribution': Distribution.THIS_COMMUNITY_ONLY
            })
            assert attr_response.status_code == 201

        # Phase 4: Complete analysis and share with community
        await client.put(f'/api/v1/events/{incident_id}', json={
            'analysis': Analysis.COMPLETED,
            'distribution': Distribution.CONNECTED_COMMUNITIES,
            'info': 'Security Incident - Email Phishing Campaign [ANALYZED]'
        })

        # Phase 5: Publish for sharing
        publish_response = await client.post(f'/api/v1/events/{incident_id}/publish')
        assert publish_response.status_code == 200

        # Phase 6: Validate final incident state
        final_response = await client.get(f'/api/v1/events/{incident_id}')
        final_incident = final_response.json()

        assert final_incident['analysis'] == Analysis.COMPLETED
        assert final_incident['distribution'] == Distribution.CONNECTED_COMMUNITIES
        assert final_incident['published'] is True
        # 4 email + 3 file indicators
        assert len(final_incident['attributes']) == 7

        # Phase 7: Test correlation with other incidents
        correlation_response = await client.post('/api/v1/correlations/analyze', json={
            'event_ids': [incident_id]
        })
        assert correlation_response.status_code == 200

    async def test_threat_intelligence_feed_integration(self, client):
        """
        Test: Threat intelligence feed integration scenario
        Coverage: Feed integration workflow
        Requirement: Intelligence feed processing validation
        """
        # Simulate threat intelligence feed import
        feed_events = [
            {
                'info': 'APT Group Alpha - Infrastructure Update',
                'threat_level_id': ThreatLevel.HIGH,
                'analysis': Analysis.COMPLETED,
                'distribution': Distribution.ALL_COMMUNITIES,
                'published': True,
                'attributes': [
                    {'category': 'Network activity', 'type': 'domain',
                        'value': 'apt-alpha-c2.malicious.net'},
                    {'category': 'Network activity',
                        'type': 'ip-src', 'value': '203.0.113.50'},
                    {'category': 'Attribution',
                        'type': 'threat-actor', 'value': 'APT-Alpha'},
                ]
            },
            {
                'info': 'Ransomware Campaign - Beta Group IOCs',
                'threat_level_id': ThreatLevel.HIGH,
                'analysis': Analysis.COMPLETED,
                'distribution': Distribution.ALL_COMMUNITIES,
                'published': True,
                'attributes': [
                    {'category': 'Payload delivery', 'type': 'sha256',
                        'value': 'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3'},
                    {'category': 'Network activity', 'type': 'domain',
                        'value': 'ransom-beta-payment.onion'},
                    {'category': 'Attribution', 'type': 'threat-actor',
                        'value': 'Ransomware-Beta'},
                ]
            }
        ]

        # Import feed events
        imported_event_ids = []
        for feed_event in feed_events:
            # Create event
            event_response = await client.post('/api/v1/events', json={
                'info': feed_event['info'],
                'threat_level_id': feed_event['threat_level_id'],
                'analysis': feed_event['analysis'],
                'distribution': feed_event['distribution']
            })

            assert event_response.status_code == 201
            event_id = event_response.json()['id']
            imported_event_ids.append(event_id)

            # Add attributes
            for attr in feed_event['attributes']:
                attr_response = await client.post(f'/api/v1/events/{event_id}/attributes', json={
                    **attr,
                    'to_ids': attr['category'] in ['Network activity', 'Payload delivery'],
                    'distribution': Distribution.ALL_COMMUNITIES
                })
                assert attr_response.status_code == 201

            # Publish if specified
            if feed_event.get('published'):
                publish_response = await client.post(f'/api/v1/events/{event_id}/publish')
                assert publish_response.status_code == 200

        # Validate feed import results
        assert len(imported_event_ids) == 2

        # Test feed data querying
        search_response = await client.post('/api/v1/events/search', json={
            'info': 'APT Group Alpha'
        })
        assert search_response.status_code == 200
        search_results = search_response.json()
        assert len(search_results) >= 1

        # Test correlation across feed events
        correlation_response = await client.post('/api/v1/correlations/analyze', json={
            'event_ids': imported_event_ids
        })
        assert correlation_response.status_code == 200


if __name__ == '__main__':
    # Run integration tests
    pytest.main([
        __file__,
        '-v',
        '--tb=short',
        '--asyncio-mode=auto',
        '--cov=api',
        '--cov=services',
        '--cov=libs.service_adapters.security.misp_adapter',
        '--cov=data',
        '--cov-report=term-missing'
    ])
